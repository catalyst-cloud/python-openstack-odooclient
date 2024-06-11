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

import copy

from datetime import datetime
from functools import cached_property
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Literal,
    Optional,
    Sequence,
    get_type_hints,
    overload,
)

from odoorpc import ODOO  # type: ignore[import]
from odoorpc.env import Environment  # type: ignore[import]
from typing_extensions import Self

from .util import decode_value

if TYPE_CHECKING:
    from ... import client
    from .. import partner
    from . import manager_base


class RecordBase:
    id: int
    """The record's ID in Odoo."""

    create_date: datetime
    """The time the record was created."""

    @property
    def create_uid(self) -> int:
        """The ID of the partner that created this record."""
        return self._get_ref_id("create_uid")

    @property
    def create_name(self) -> str:
        """The name of the partner that created this record."""
        return self._get_ref_name("create_uid")

    @cached_property
    def create_user(self) -> partner.Partner:
        """The partner that created this record.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.partners.get(self.create_uid)

    write_date: datetime
    """The time the record was last modified."""

    @property
    def write_uid(self) -> int:
        """The ID of the partner that last modified this record."""
        return self._get_ref_id("write_uid")

    @property
    def write_name(self) -> str:
        """The name of the partner that modified this record."""
        return self._get_ref_name("write_uid")

    @cached_property
    def write_user(self) -> partner.Partner:
        """The partner that last modified this record.

        This fetches a full Partner object from Odoo once,
        and caches it for subsequence access.
        """
        return self._client.partners.get(self.write_uid)

    _field_mapping: Dict[Optional[str], Dict[str, str]] = {}
    """A dictionary structure mapping field names in the local class
    with the equivalents on specific versions of Odoo.

    This allows for providing for backwards compatibility for older versions
    of Odoo, while still providing a consistent API for applications using
    this library.

    Specify ``None`` instead of a version string to provide a general mapping
    for all Odoo versions, allowing for local fields to have a different name
    to their Odoo equivalent.
    """

    _alias_mapping: Dict[str, str] = {}
    """A dictionary structure mapping aliases
    (normally defined in the record class) to the corresponding field name
    in Odoo.

    This is primarily used to define aliases for search filtering purposes,
    to allow either e.g. ``write_uid`` or ``write_user`` to be specified,
    instead of just ``write_uid``, when using the ``search`` method.
    """

    _base_alias_mapping = {
        "create_user": "create_uid",
        "write_user": "write_uid",
    }

    def __init__(
        self,
        client: client.Client,
        manager: manager_base.RecordManagerBase,
        record: Dict[str, Any],
        fields: Optional[Sequence[str]],
    ) -> None:
        self._client = client
        self._manager = manager
        self._record = record
        self._fields = fields
        self._values: Dict[str, Any] = {}

    @property
    def _env(self) -> Environment:
        return self._manager._env

    @property
    def _odoo(self) -> ODOO:
        return self._client._odoo

    @classmethod
    def from_record_obj(cls, record_obj: RecordBase) -> Self:
        """Create a record object of this class's type
        from another record object.

        This is intended to be used to "cast" a record object from
        one type to another (e.g. an organisation-specific implementation
        of a model class).

        :param record_obj: Record to use to create the new object
        :type record_obj: RecordBase
        :return: Record object of the implementing class's type
        :rtype: Self
        """
        return cls(
            client=record_obj._client,
            manager=record_obj._manager,
            record=record_obj._record,
            fields=record_obj._fields,
        )

    def as_dict(self, raw: bool = False) -> Dict[str, Any]:
        """Convert this record object to a dictionary.

        The fields and values in the dictionary are the same
        as if the record was queried using ``as_dict=True``.
        This changes field names to the record object equivalents,
        if they are different, to take into account fields being
        named differently across Odoo versions.

        Set ``raw=True`` to instead get the raw record dictionary
        fields and values as returned by OdooRPC.

        :param raw: Return raw dictionary from OdooRPC, defaults to False
        :type raw: bool, optional
        :return: Record dictionary
        :rtype: Dict[str, Any]
        """
        return (
            copy.deepcopy(self._record)
            if raw
            else {
                self._manager._get_local_field(field): copy.deepcopy(value)
                for field, value in self._record.items()
            }
        )

    def refresh(self) -> Self:
        """Fetch the latest version of this record from Odoo.

        This does not update the record object in place,
        a new object is returned with the up-to-date field values.

        :return: Latest version of the record object
        :rtype: Self
        """
        return type(self)(
            client=self._client,
            manager=self._manager,
            record=self._env.read(
                self.id,
                fields=self._fields,
            )[0],
            fields=self._fields,
        )

    def unlink(self) -> None:
        """Delete this record from Odoo."""
        self._manager.unlink(self)

    def delete(self) -> None:
        """Delete this record from Odoo."""
        self._manager.delete(self)

    def _get_remote_field(self, field: str) -> str:
        return self._manager._get_remote_field(field)

    def _get_local_field(self, field: str) -> str:
        return self._manager._get_local_field(field)

    def _get_field(self, name: str) -> Any:
        try:
            return self._record[self._get_remote_field(name)]
        except KeyError as err:
            raise AttributeError(str(err)) from None

    @classmethod
    def _resolve_alias(cls, alias: str) -> str:
        return cls._alias_mapping.get(
            alias,
            cls._base_alias_mapping.get(alias, alias),
        )

    @overload
    def _get_ref_id(
        self,
        name: str,
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def _get_ref_id(
        self,
        name: str,
        optional: Literal[True],
    ) -> Optional[int]: ...

    @overload
    def _get_ref_id(
        self, name: str, optional: bool = ...
    ) -> Optional[int]: ...

    def _get_ref_id(self, name: str, optional: bool = False) -> Optional[int]:
        # NOTE(callumdickinson): This method intentionally does not test
        # for field existence, so an error is raised if the field is not
        # actually selected in the query.
        # If an optional ref is selected in a query but a ref is not set,
        # ``False`` is returned instead of the expected 2-element list.
        ref = self._get_field(name)
        if not optional:
            return ref[0]
        return ref[0] if ref else None

    @overload
    def _get_ref_name(
        self,
        name: str,
        optional: Literal[False] = ...,
    ) -> str: ...

    @overload
    def _get_ref_name(
        self,
        name: str,
        optional: Literal[True],
    ) -> Optional[str]: ...

    @overload
    def _get_ref_name(
        self, name: str, optional: bool = ...
    ) -> Optional[str]: ...

    def _get_ref_name(
        self,
        name: str,
        optional: bool = False,
    ) -> Optional[str]:
        # NOTE(callumdickinson): This method intentionally does not test
        # for field existence, so an error is raised if the field is not
        # actually selected in the query.
        # If an optional ref is selected in a query but a ref is not set,
        # ``False`` is returned instead of the expected 2-element list.
        ref = self._get_field(name)
        if not optional:
            return ref[1]
        return ref[1] if ref else None

    def __getattr__(self, name: str) -> Any:
        # If the field value has already been decoded,
        # return the cached value.
        if name in self._values:
            return self._values[name]
        value = self._get_field(name)
        # NOTE(callumdickinson): Use the type annotation to coerce
        # the field value returned in the record dict into the expected type.
        # If no annotation was found for the field, cache the value
        # unmodified.
        annotations = get_type_hints(type(self))
        self._values[name] = (
            decode_value(annotations[name], value)
            if name in annotations
            else value
        )
        # Return the now-cached value.
        return self._values[name]

    def __str__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"record={self._record}"
            f", fields={self._fields}"
            ")"
        )

    def __repr__(self) -> str:
        return str(self)
