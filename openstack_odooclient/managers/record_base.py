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
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Literal,
    Optional,
    Sequence,
    Type,
    Union,
    overload,
)

from typing_extensions import (
    Annotated,
    Self,
    get_args as get_type_args,
    get_origin as get_type_origin,
    get_type_hints,
)

from .util import FieldAlias, ModelRef, decode_value, is_subclass

if TYPE_CHECKING:
    from odoorpc import ODOO  # type: ignore[import]
    from odoorpc.env import Environment  # type: ignore[import]

    from .. import client
    from . import record_manager_base


class RecordBase:
    id: int
    """The record's ID in Odoo."""

    create_date: datetime
    """The time the record was created."""

    create_uid: Annotated[int, ModelRef("create_uid")]
    """The ID of the user that created this record."""

    create_name: Annotated[str, ModelRef("create_uid")]
    """The name of the user that created this record."""

    create_user: Annotated[user.User, ModelRef("create_uid")]
    """The user that created this record.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    write_date: datetime
    """The time the record was last modified."""

    write_uid: Annotated[int, ModelRef("write_uid")]
    """The ID for the user that last modified this record."""

    write_name: Annotated[str, ModelRef("write_uid")]
    """The name of the user that last modified this record."""

    write_user: Annotated[user.User, ModelRef("create_uid")]
    """The user that last modified this record.

    This fetches the full record from Odoo once,
    and caches it for subsequence access.
    """

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

    def __init__(
        self,
        client: client.Client,
        manager: record_manager_base.RecordManagerBase,
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
        return alias
        # return cls._alias_mapping.get(
        #     alias,
        #     cls._base_alias_mapping.get(alias, alias),
        # )

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
        # NOTE(callumdickinson): Use the type hint to coerce
        # the field value returned in the record dict into the expected type.
        type_hints = get_type_hints(type(self), include_extras=True)
        # First, check if the field has a type hint defined at all.
        # If not, just cache the value as is and return it.
        if name not in type_hints:
            self._values[name] = self._get_field(name)
            return self._values[name]
        # We know we have a type hint to decode for the field.
        type_hint = type_hints[name]
        # Check if the field is annotated.
        # There are special code paths for handling fields
        # with specific annotations added to them.
        if get_type_origin(type_hint) is Annotated:
            type_args = get_type_args(type_hint)
            attr_type: Type[Any] = type_args[0]
            annotations = type_args[1:]
            if len(annotations) == 1:
                annotation = annotations[0]
                # If this field is a field alias,
                # recursively fetch the value for the target field.
                if isinstance(annotation, FieldAlias):
                    return getattr(self, annotation.field)
                # If this field is a model ref, resolve the model ref
                # and return the intended value.
                if isinstance(annotation, ModelRef):
                    self._values[name] = self._getattr_model_ref(
                        attr_type=attr_type,
                        model_ref=annotation,
                    )
                    return self._values[name]
                raise ValueError(
                    (
                        f"Unsupported annotation for field '{name}': "
                        f"{annotation}"
                    ),
                )
        # Base case: Decode the value according to the field's type hint,
        # cache the value, and return it.
        self._values[name] = decode_value(type_hint, self._get_field(name))
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
                    "Unsupported field value typefor model ref list: "
                    f"{value_type}"
                ),
            )
        # The following is for decoding a singular model ref value.
        # Check if the model ref is optional, and if it is,
        # return the desired value for when the value is empty.
        if get_type_origin(attr_type) is Union:
            unsupported_union = (
                "Only unions of the format Optional[T], "
                "Union[T, type(None)] or Union[T, Literal[False]] "
                "are supported for singular model refs, "
                f"found type hint: {attr_type}"
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
        if value_type is int:
            return record_id
        if value_type is str:
            return record_name
        if is_subclass(value_type, RecordBase):
            return self._client._record_manager_mapping[value_type].get(
                record_id,
            )
        raise ValueError(
            (
                "Unsupported field value type for singular model ref: "
                f"{value_type}"
            ),
        )

    def __str__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"record={self._record}"
            f", fields={self._fields}"
            ")"
        )

    def __repr__(self) -> str:
        return str(self)


# NOTE(callumdickinson): Import here to avoid circular imports.
from . import user  # noqa: E402
