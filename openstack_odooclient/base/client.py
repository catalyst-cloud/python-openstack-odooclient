# Copyright (C) 2024 Catalyst Cloud Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import json
import random

from pathlib import Path
from typing import TYPE_CHECKING, Any, Type

import httpx

from packaging.version import Version
from typing_extensions import get_type_hints  # 3.11 and later

from ..util import JSONDecoder, JSONEncoder, is_subclass
from .record import RecordBase
from .record_manager import RecordManagerBase

if TYPE_CHECKING:
    from collections.abc import Mapping


class ClientBase:
    """The client base class for managing the OpenStack Odoo ERP.

    No managers are included on this base class.
    This class should be inherited, and manager classes defined
    on the subclass using type hints, as shown below.

    The manager class will be instantiated and added to the
    client object when the client is created.

    >>> from openstack_odooclient import ClientBase, UserManager
    >>> class Client(ClientBase):
    ...     users: UserManager
    >>> Client(...).users
    <openstack_odooclient.managers.user.UserManager object at 0x7f3c31ed4b80>

    Connect to an Odoo server by either passing the required
    connection and authentication information,
    or passing in a pre-existing OdooRPC ``ODOO`` object.

    When connecting to an Odoo server using SSL, set ``protocol``
    to ``jsonrpc+ssl``. SSL certificate verification can be disabled
    by setting ``verify`` to ``False``. If a custom CA certificate
    is required to verify the Odoo server's host certificate,
    this can be configured by passing the certificate path to ``verify``.

    All parameters must be specified as keyword arguments.

    :param hostname: Server hostname, required if ``odoo`` is not set
    :type hostname: str | None, optional
    :param database: Database name, required if ``odoo`` is not set
    :type database: str | None, optional
    :param username: Username, required if ``odoo`` is not set
    :type username: str | None, optional
    :param password: Password (or API key), required if ``odoo`` is not set
    :type password: str | None, optional
    :param protocol: Communication protocol, defaults to ``jsonrpc``
    :type protocol: str, optional
    :param port: Access port, defaults to ``8069``
    :type port: int, optional
    :param verify: Configure SSL cert verification, defaults to ``True``
    :type verify: bool | str | Path
    :param version: Server version, defaults to ``None`` (auto-detect)
    :type version: str | None, optional
    """

    def __init__(
        self,
        *,
        base_url: str,
        database: str,
        username: str,
        password: str,
        verify: bool | str | Path = True,
        timeout: int | None = None,
    ) -> None:
        self._base_url = base_url
        self._database = database
        self._username = username
        self._password = password
        self._verify = str(verify) if isinstance(verify, Path) else verify
        self._timeout = timeout
        self._env_manager_mapping: dict[str, RecordManagerBase] = {}
        """An internal mapping between env (model) names and their managers.

        This is populated by the manager classes themselves when created,
        and used by the ``Attachment.res_model_manager`` field.

        *Added in version 0.2.0.*
        """
        self._record_manager_mapping: dict[
            Type[RecordBase],
            RecordManagerBase,
        ] = {}
        """An internal mapping between record classes and their managers.

        This is populated by the manager classes themselves when created,
        and used when converting model references on record objects into
        new record objects.
        """
        # Create record managers defined in the type hints.
        for attr_name, attr_type in get_type_hints(type(self)).items():
            if is_subclass(attr_type, RecordManagerBase):
                setattr(self, attr_name, attr_type(self))
        self.login()

    @property
    def user_id(self) -> int:
        """The ID for the currently logged in user."""
        return self._user_id

    @property
    def version(self) -> Version:
        """The version of the server,
        as a comparable ``packaging.version.Version`` object.
        """
        return self._odoo_version

    @property
    def version_str(self) -> str:
        """The version of the server, as a string."""
        return self._odoo_version_str

    def _jsonrpc(
        self,
        *,
        params: Mapping[str, Any] | None = None,
        url: str = "/jsonrpc",
    ) -> httpx.Response:
        return self._http_client.post(
            url,
            headers={"Content-Type": "application/json"},
            content=json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "call",
                    "params": dict(params) if params else {},
                    "id": random.randint(0, 1000000000),  # noqa: S311
                },
                cls=JSONEncoder,
                separators=(",", ":"),
            ),
        )

    def login(self) -> None:
        """Login to the Odoo database with the configured
        username and password.

        Fetches and stores a new session cookie, usable until
        it expires after a pre-determined amount of time.

        If a request is made to Odoo after the session cookie
        has expired, the Odoo client will automatically run this
        method to refresh the session cookie.
        """
        # Set up the HTTP client session that will be used
        # for all requests.
        self._http_client = httpx.Client(
            base_url=self._base_url,
            verify=self._verify,
            timeout=self._timeout,
        )
        # Login, and set up the user context.
        response = self._jsonrpc(
            params={
                "service": "common",
                "method": "login",
                "args": [self._database, self._username, self._password],
            },
        )
        # TODO(callumdickinson): Handle HTTP 401.
        user_id: int | None = response.json()["result"]
        if not user_id:
            # TODO(callumdickinson): Custom exception class.
            raise ValueError("Incorrect username or password")
        response = self._jsonrpc(
            params={
                "service": "object",
                "method": "execute",
                "args": [
                    self._database,
                    self._username,
                    self._password,
                    "res.users",
                    "context_get",
                ],
            },
        )
        context: dict[str, Any] = response.json()["result"]
        context["uid"] = user_id
        self._user_id = user_id
        self._context = context
        # Discover the Odoo server's version.
        response = self._jsonrpc(url="/web/webclient/version_info")
        self._odoo_version_str: str = response.json()["server_version"]
        self._odoo_version = Version(self._odoo_version_str)

    def close(self) -> None:
        self._http_client.close()

    def execute(
        self,
        model: str,
        method: str,
        /,
        *args: Any,
    ) -> Any:
        """Invoke a method on the given model,
        passing all other positional arguments
        as parameters, and return the result.

        :param model: The model to run the method on
        :type model: str
        :param method: The method to invoke
        :type method: str
        :return: The return value of the method
        :rtype: Any
        """
        response = self._jsonrpc(
            params={
                "service": "object",
                "method": "execute",
                "args": [
                    self._database,
                    self._user_id,
                    self._password,
                    model,
                    method,
                    *args,
                ],
            },
        )
        data: dict[str, Any] = json.loads(response.text, cls=JSONDecoder)
        return data.get("result")

    def execute_kw(
        self,
        model: str,
        method: str,
        /,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Invoke a method on the given model,
        passing all other positional arguments
        and all keyword arguments as parameters,
        and return the result.

        :param model: The model to run the method on
        :type model: str
        :param method: The method to invoke
        :type method: str
        :return: The return value of the method
        :rtype: Any
        """
        response = self._jsonrpc(
            params={
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self._database,
                    self._user_id,
                    self._password,
                    model,
                    method,
                    [args, kwargs],
                ],
            },
        )
        data: dict[str, Any] = json.loads(response.text, cls=JSONDecoder)
        return data.get("result")
