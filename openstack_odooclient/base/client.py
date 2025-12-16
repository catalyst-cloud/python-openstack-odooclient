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

import ssl
import urllib.request

from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Type, overload

from odoorpc import ODOO  # type: ignore[import]
from packaging.version import Version
from typing_extensions import get_type_hints  # 3.11 and later

from ..util import is_subclass
from .record.base import RecordBase
from .record_manager.base import RecordManagerBase

if TYPE_CHECKING:
    from odoorpc.db import DB  # type: ignore[import]
    from odoorpc.env import Environment  # type: ignore[import]
    from odoorpc.report import Report  # type: ignore[import]


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

    @overload
    def __init__(
        self,
        *,
        hostname: str | None = ...,
        database: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        protocol: str = "jsonrpc",
        port: int = 8069,
        verify: bool | str | Path = ...,
        version: str | None = ...,
        odoo: ODOO,
    ) -> None: ...

    @overload
    def __init__(
        self,
        *,
        hostname: str,
        database: str,
        username: str,
        password: str,
        protocol: str = "jsonrpc",
        port: int = 8069,
        verify: bool | str | Path = ...,
        version: str | None = ...,
        odoo: Literal[None] = ...,
    ) -> None: ...

    @overload
    def __init__(
        self,
        *,
        hostname: str | None = ...,
        database: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        protocol: str = "jsonrpc",
        port: int = 8069,
        verify: bool | str | Path = ...,
        version: str | None = ...,
        odoo: ODOO | None = ...,
    ) -> None: ...

    def __init__(
        self,
        *,
        hostname: str | None = None,
        database: str | None = None,
        username: str | None = None,
        password: str | None = None,
        protocol: str = "jsonrpc",
        port: int = 8069,
        verify: bool | str | Path = True,
        version: str | None = None,
        odoo: ODOO | None = None,
    ) -> None:
        # If an OdooRPC object is provided, use that directly.
        # Otherwise, make a new one with the provided settings.
        if odoo:
            self._odoo = odoo
        else:
            opener = None
            if protocol.endswith("+ssl"):
                ssl_verify = verify is not False
                ssl_cafile = (
                    str(verify) if isinstance(verify, (Path, str)) else None
                )
                if not ssl_verify or ssl_cafile:
                    ssl_context = ssl.create_default_context(cafile=ssl_cafile)
                    if not ssl_verify:
                        ssl_context.check_hostname = False
                        ssl_context.verify_mode = ssl.CERT_NONE
                    opener = urllib.request.build_opener(
                        urllib.request.HTTPSHandler(context=ssl_context),
                        urllib.request.HTTPCookieProcessor(),
                    )
            self._odoo = ODOO(
                protocol=protocol,
                host=hostname,
                port=port,
                version=version,
                opener=opener,
            )
            self._odoo.login(database, username, password)
        self._env_manager_mapping: dict[str, RecordManagerBase[Any]] = {}
        """An internal mapping between env (model) names and their managers.

        This is populated by the manager classes themselves when created,
        and used by the ``Attachment.res_model_manager`` field.

        *Added in version 0.2.1.*
        """
        self._record_manager_mapping: dict[
            Type[RecordBase[Any]],
            RecordManagerBase[Any],
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

    @property
    def odoo(self) -> ODOO:
        """The OdooRPC connection object currently being used
        by this client.
        """
        return self._odoo

    @property
    def db(self) -> DB:
        """The database management service."""
        return self._odoo.db

    @property
    def report(self) -> Report:
        """The report management service."""
        return self._odoo.report

    @property
    def env(self) -> Environment:
        """The OdooRPC environment wrapper object.

        This allows interacting with models that do not have managers
        within this Odoo client.
        Usage is the same as on a native ``odoorpc.ODOO`` object.
        """
        return self._odoo.env

    @property
    def user_id(self) -> int:
        """The ID for the currently logged in user."""
        return self._odoo.env.uid

    @property
    def version(self) -> Version:
        """The version of the server,
        as a comparable ``packaging.version.Version`` object.
        """
        return Version(self._odoo.version)

    @property
    def version_str(self) -> str:
        """The version of the server, as a string."""
        return self._odoo.version
