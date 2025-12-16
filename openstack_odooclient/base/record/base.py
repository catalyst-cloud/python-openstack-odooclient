# Copyright (C) 2025 Catalyst Cloud Limited
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

from datetime import date, datetime
from types import MappingProxyType, UnionType
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Generic,
    Literal,
    Protocol,
    Type,
    TypeVar,
    Union,
)

from typing_extensions import (
    Self,
    get_args as get_type_args,
    get_origin as get_type_origin,
)

from ...util import is_subclass
from .types import FieldAlias, ModelRef

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from odoorpc import ODOO  # type: ignore[import]
    from odoorpc.env import Environment  # type: ignore[import]

    from ..client import ClientBase

RM = TypeVar("RM", bound="RecordManagerBase")
"""An invariant type variable for a record manager class.

To be used when defining record mixins,
or generic base classes operating on record managers.
"""

RM_co = TypeVar("RM_co", bound="RecordManagerBase", covariant=True)
"""A covariant type variable for a record manager class.

To be used when defining generic protocols, or parameters/return values
that allow ``Record`` objects using a ``RecordManager`` class that is
a subclass of the ``Record`` type within the given content.
"""


class RecordProtocol(Protocol[RM]):
    """The protocol for a record class.

    This defines all common attributes and methods available for
    implementations of records to use.

    The primary use of this class is to be subclassed by mixins, to provide
    type hinting for common attributes and methods available on the
    ``RecordBase`` class.

    ``RecordBase`` is the base class that provides the core functionality
    of a record object, and that is what should be subclassed to make a new
    record class.
    """

    id: int
    """The record's ID in Odoo."""

    create_date: datetime
    """The time the record was created."""

    create_uid: Annotated[int | None, ModelRef("create_uid", User)]
    """The ID of the user that created this record."""

    create_name: Annotated[str | None, ModelRef("create_uid", User)]
    """The name of the user that created this record."""

    create_user: Annotated[User | None, ModelRef("create_uid", User)]
    """The user that created this record.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    write_date: datetime
    """The time the record was last modified."""

    write_uid: Annotated[int | None, ModelRef("write_uid", User)]
    """The ID for the user that last modified this record."""

    write_name: Annotated[str | None, ModelRef("write_uid", User)]
    """The name of the user that last modified this record."""

    write_user: Annotated[User | None, ModelRef("write_uid", User)]
    """The user that last modified this record.

    This fetches the full record from Odoo once,
    and caches it for subsequence accesses.
    """

    _field_mapping: dict[str | None, dict[str, str]] = {}
    """A dictionary structure mapping field names in the local class
    with the equivalents on specific versions of Odoo.

    This allows for providing for backwards compatibility for older versions
    of Odoo, while still providing a consistent API for applications using
    this library.

    Specify ``None`` instead of a version string to provide a general mapping
    for all Odoo versions, allowing for local fields to have a different name
    to their Odoo equivalent.
    """

    @property
    def _client(self) -> ClientBase:
        """The Odoo client that created this record object."""
        ...

    @property
    def _manager(self) -> RM:
        """The manager object responsible for this record."""
        ...

    @property
    def _odoo(self) -> ODOO:
        """The OdooRPC connection object this record was created from."""
        ...

    @property
    def _env(self) -> Environment:
        """The OdooRPC environment object this record was created from."""
        ...

    @classmethod
    def from_record_obj(cls, record_obj: RecordBase[RM]) -> Self:
        """Create a record object of this class's type
        from another record object.

        This is intended to be used to "cast" a record object from
        one type to another (e.g. an organisation-specific implementation
        of a model class).

        :param record_obj: Record to use to create the new object
        :type record_obj: RecordBase[RM]
        :return: Record object of the implementing class's type
        :rtype: Self
        """
        ...

    def as_dict(self, raw: bool = False) -> dict[str, Any]:
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
        :rtype: dict[str, Any]
        """
        ...

    def update(self, **fields: Any) -> None:
        """Update one or more fields on this record in place.

        Field names are passed as keyword arguments.
        This method has the same flexibility with regards to what
        field names are used as when creating records; for example,
        when updating a model ref, either its ID (e.g. ``user_id``)
        or object (e.g. ``user``) field names can be used.

        Note that this record object is not updated in place by
        this method. If you need an updated version of the record
        object, use the `refresh` method to fetch the latest version.

        *Added in version 0.2.1.*
        """
        ...

    def refresh(self) -> Self:
        """Fetch the latest version of this record from Odoo.

        This does not update the record object in place,
        a new object is returned with the up-to-date field values.

        :return: Latest version of the record object
        :rtype: Self
        """
        ...

    def unlink(self) -> None:
        """Delete this record from Odoo."""
        ...

    def delete(self) -> None:
        """Delete this record from Odoo."""
        ...


class RecordBase(RecordProtocol[RM], Generic[RM]):
    """The generic base class for records.

    Subclass this class to implement the record class for custom record types,
    specifying the name of the manager class (string), as available in the
    Python source file, as the generic type argument.
    """

    def __init__(
        self,
        client: ClientBase,
        record: Mapping[str, Any],
        fields: Sequence[str] | None,
    ) -> None:
        self._client_ = client
        self._record = MappingProxyType(record)
        """The raw record fields from OdooRPC."""
        self._fields = tuple(fields) if fields else None
        """The fields selected in the query that created this record object."""
        self._values: dict[str, Any] = {}
        """The cache for the processed record field values."""

    @property
    def _client(self) -> ClientBase:
        return self._client_

    @property
    def _manager(self) -> RM:
        mapping = self._client._record_manager_mapping
        return mapping[type(self)]  # type: ignore[return-value]

    @property
    def _odoo(self) -> ODOO:
        return self._client._odoo

    @property
    def _env(self) -> Environment:
        return self._manager._env

    @property
    def _type_hints(self) -> MappingProxyType[str, Any]:
        return self._manager._record_type_hints

    @classmethod
    def from_record_obj(cls, record_obj: RecordBase[RM_co]) -> Self:
        return cls(
            client=record_obj._client,
            record=record_obj._record,
            fields=record_obj._fields,
        )

    def as_dict(self, raw: bool = False) -> dict[str, Any]:
        return (
            copy.deepcopy(dict(self._record))
            if raw
            else {
                self._manager._get_local_field(field): copy.deepcopy(value)
                for field, value in self._record.items()
            }
        )

    def update(self, **fields: Any) -> None:
        self._manager.update(self.id, **fields)

    def refresh(self) -> Self:
        return type(self)(
            client=self._client,
            record=self._env.read(
                self.id,
                fields=self._fields,
            )[0],
            fields=self._fields,
        )

    def unlink(self) -> None:
        self._manager.unlink(self)

    def delete(self) -> None:
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

    def __getattr__(self, name: str) -> Any:
        # If the field value has already been decoded,
        # return the cached value.
        if name in self._values:
            return self._values[name]
        # NOTE(callumdickinson): Use the type hint to coerce
        # the field value returned in the record dict into the expected type.
        # First, check if the field has a type hint defined at all.
        # If not, just cache the value as is and return it.
        if name not in self._type_hints:
            self._values[name] = self._get_field(name)
            return self._values[name]
        # We know we have a type hint to decode for the field.
        type_hint = self._type_hints[name]
        # If this field is a field alias, recursively fetch
        # the value for the target field.
        field_alias = FieldAlias.get(type_hint)
        if field_alias:
            self._values[name] = getattr(self, field_alias.field)
            return self._values[name]
        # If this field is a model ref, resolve the model ref
        # and return the intended value.
        model_ref = ModelRef.get(type_hint)
        if model_ref:
            self._values[name] = self._getattr_model_ref(
                attr_type=get_type_args(type_hint)[0],
                model_ref=model_ref,
            )
            return self._values[name]
        # Base case: Decode the value according to the field's type hint,
        # cache the value, and return it.
        self._values[name] = self._decode_value(
            type_hint,
            self._get_field(name),
        )
        return self._values[name]

    def _getattr_model_ref(
        self,
        attr_type: Type[Any],
        model_ref: ModelRef,
    ) -> Any:
        field_value = self._record[self._get_remote_field(model_ref.field)]
        # If the expected attribute type is a list, then process the model ref
        # as a list of model IDs or objects.
        if get_type_origin(attr_type) is list:
            value_type = get_type_args(attr_type)[0]
            # Handle a model ref list with the same record type as the
            # parent record. Fetch the records from Odoo, and return
            # the results.
            if value_type is Self:
                return self._manager.list(field_value)
            # List of model objects. Fetch the objects from Odoo,
            # and return the results.
            if is_subclass(value_type, RecordBase):
                return self._client._record_manager_mapping[value_type].list(
                    field_value,
                )
            # List of model IDs. The raw field value is already this format,
            # so just return it as is.
            if value_type is int:
                return field_value
            raise ValueError(
                (
                    "Unsupported field value type for model ref list: "
                    f"{value_type}"
                ),
            )
        # The following is for decoding a singular model ref value.
        # Check if the model ref is optional, and if it is,
        # return the desired value for when the value is empty.
        attr_type_origin = get_type_origin(attr_type)
        if attr_type_origin is Union or attr_type_origin is UnionType:
            unsupported_union = (
                "Only unions of the format 'T | None' "
                "or 'T | Literal[False]' are supported for singular "
                f"model refs, found type hint: {attr_type}"
            )
            union_types = set(get_type_args(attr_type))
            if len(union_types) > 2:  # noqa: PLR2004
                raise ValueError(unsupported_union)
            if type(None) in union_types:
                union_types.remove(type(None))
                if not field_value:
                    return None
            elif Literal[False] in union_types:
                union_types.remove(Literal[False])
                if not field_value:
                    return False
            if len(union_types) != 1:
                raise ValueError(unsupported_union)
            value_type = union_types.pop()
        else:
            value_type = attr_type
        # The model ref is either required, or is optional but a value
        # was found. Determine the appropriate value return type,
        # and generate the value.
        record_id: int = field_value[0]
        record_name: str = field_value[1]
        if value_type is Self:
            return self._manager.get(record_id)
        if is_subclass(value_type, RecordBase):
            return self._client._record_manager_mapping[value_type].get(
                record_id,
            )
        if value_type is int:
            return record_id
        if value_type is str:
            return record_name
        raise ValueError(
            (
                "Unsupported field value type for singular model ref: "
                f"{value_type}"
            ),
        )

    @classmethod
    def _decode_value(cls, type_hint: Any, value: Any) -> Any:
        value_type = get_type_origin(type_hint) or type_hint
        # The basic data types that need special handling.
        if value_type is date:
            return date.fromisoformat(value)
        if value_type is datetime:
            return datetime.fromisoformat(value)
        # When a list is expected, decode each value individually
        # and return the result as a new list with the same order.
        if value_type is list:
            return [
                cls._decode_value(get_type_args(type_hint)[0], v)
                for v in value
            ]
        # When a dict is expected, decode the key and the value of each
        # item separately, and combine the result into a new dict.
        if value_type is dict:
            k_type, v_type = get_type_args(type_hint)
            return {
                cls._decode_value(k_type, k): cls._decode_value(v_type, v)
                for k, v in value.items()
            }
        # Basic case for handling specific union structures.
        # Not suitable for handling complicated union structures.
        # TODO(callumdickinson): Find a way to handle complicated
        # union structures more smartly.
        if value_type is Union or value_type is UnionType:
            attr_union_types = get_type_args(type_hint)
            if len(attr_union_types) == 2:  # noqa: PLR2004
                # T | None
                if type(None) in attr_union_types and value is not None:
                    return cls._decode_value(
                        next(
                            (
                                t
                                for t in attr_union_types
                                if t is not type(None)
                            ),
                        ),
                        value,
                    )
                # T | Literal[False]
                if Literal[False] in attr_union_types and value is not False:
                    return cls._decode_value(
                        next(
                            (
                                t
                                for t in attr_union_types
                                if t is not Literal[False]
                            ),
                        ),
                        value,
                    )
        # Base case: Return the passed value unmodified.
        return value

    def __str__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"record={dict(self._record)}"
            f", fields={list(self._fields) if self._fields else None}"
            ")"
        )

    def __repr__(self) -> str:
        return str(self)


# NOTE(callumdickinson): Import here to avoid circular imports.
from ...managers.user import User  # noqa: E402
from ..record_manager.base import RecordManagerBase  # noqa: E402
