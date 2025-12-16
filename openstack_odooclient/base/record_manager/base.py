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

import builtins
import itertools

from collections.abc import Iterable, Mapping, Sequence
from datetime import date, datetime
from types import MappingProxyType, UnionType
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Generic,
    Literal,
    Type,
    Union,
    overload,
)

from typing_extensions import (
    Self,
    get_args as get_type_args,
    get_origin as get_type_origin,
    get_type_hints,
)

from ...exceptions import MultipleRecordsFoundError, RecordNotFoundError
from ...util import (
    DEFAULT_SERVER_DATE_FORMAT,
    DEFAULT_SERVER_DATETIME_FORMAT,
    get_mapped_field,
)
from ..record.base import RecordBase
from ..record.types import FieldAlias, ModelRef
from .protocol import R, RecordManagerProtocol
from .types import FilterCriterion

if TYPE_CHECKING:
    from odoorpc import ODOO  # type: ignore[import]
    from odoorpc.env import Environment  # type: ignore[import]

    from ..client import ClientBase


class RecordManagerBase(RecordManagerProtocol[R], Generic[R]):
    """A generic record manager base class.

    This is the class that is subclassed create a record manager
    for querying, creating and managing record objects.

    To define a record manager for your custom record class:

    1. Set ``RecordManagerBase`` as the superclass, and pass the
       record class as the type argument to configure type hinting
       for record manager methods.
    2. Set the ``env_name`` class attribute on the record manager
       to the Odoo model name for the record type.
    3. Set the ``record_class`` class attribute on the record manager
       to define the record class that will be used to create record objects.

    >>> from openstack_odooclient import Client, RecordBase, RecordManagerBase
    >>> class CustomRecord(RecordBase["CustomRecordManager"]):
    ...     name: str
    >>> class CustomRecordManager(RecordManagerBase[CustomRecord]):
    ...     env_name = "custom.record"
    ...     record_class = CustomRecord

    Once you have your manager class, subclass the ``Client``
    class and add a type hint for your custom record manager.
    This will allow you to use custom record managers on your
    Odoo client objects.

    >>> class CustomClient(Client):
    ...     custom_records: CustomRecordManager
    """

    def __init__(self, client: ClientBase) -> None:
        self._client_ = client
        # Assign this record manager object as the manager
        # responsible for the configured record class in the client.
        self._client._env_manager_mapping[self.env_name] = self
        self._client._record_manager_mapping[self.record_class] = self
        self._record_type_hints = MappingProxyType(
            get_type_hints(
                self.record_class,
                include_extras=True,
            ),
        )
        """The type hints for the fields defined in the record class."""
        self._field_mapping_reverse = {
            odoo_version: {
                remote_field: local_field
                for local_field, remote_field in field_mapping.items()
            }
            for odoo_version, field_mapping in (
                self.record_class._field_mapping.items()
            )
        }
        """Dynamically generated "reverse" field mapping for the
        record class, mapping Odoo version-specific remote field names
        to their representations on the record class.
        """
        self._model_ref_mapping: dict[str, str] = {}
        """Mapping of the remote field name for a model ref
        to the local field name representing the model ref's IDs.

        Examples:

        * (remote) ``product_id`` -> ``product_id`` (local)
        * (remote) ``child_id`` -> ``child_ids`` (local)
        * (remote) ``os_project`` -> ``os_project_id`` (local)
        """
        for local_field, type_hint in self._record_type_hints.items():
            model_ref = ModelRef.get(type_hint)
            if model_ref:
                field_type = get_type_args(type_hint)[0]
                try:
                    if field_type is int or (
                        get_type_origin(field_type) is list
                        and get_type_args(field_type)[0] is int
                    ):
                        self._model_ref_mapping[model_ref.field] = local_field
                except IndexError:
                    pass

    @property
    def _client(self) -> ClientBase:
        """The Odoo client object the manager uses."""
        return self._client_

    @property
    def _odoo(self) -> ODOO:
        """The OdooRPC connection object this record manager uses."""
        return self._client._odoo

    @property
    def _env(self) -> Environment:
        """The OdooRPC environment object this record manager uses."""
        return self._odoo.env[self.env_name]

    @overload
    def list(
        self,
        ids: int | Iterable[int],
        *,
        fields: Iterable[str] | None = ...,
        as_dict: Literal[False] = ...,
        optional: bool = ...,
    ) -> builtins.list[R]: ...

    @overload
    def list(
        self,
        ids: int | Iterable[int],
        *,
        fields: Iterable[str] | None = ...,
        as_dict: Literal[True],
        optional: bool = ...,
    ) -> builtins.list[dict[str, Any]]: ...

    @overload
    def list(
        self,
        ids: int | Iterable[int],
        *,
        fields: Iterable[str] | None = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> builtins.list[R] | builtins.list[dict[str, Any]]: ...

    def list(
        self,
        ids: int | Iterable[int],
        fields: Iterable[str] | None = None,
        as_dict: bool = False,
        optional: bool = False,
    ) -> builtins.list[R] | builtins.list[dict[str, Any]]:
        if isinstance(ids, int):
            _ids: int | list[int] = ids
        else:
            _ids = list(ids)
            if not _ids:
                return []  # type: ignore[return-value]
        fields = fields or self.default_fields or None
        _fields = (
            list(
                dict.fromkeys(
                    (self._encode_field(f) for f in fields),
                ).keys(),
            )
            if fields is not None
            else None
        )
        records: Iterable[dict[str, Any]] = self._env.read(
            _ids,
            fields=_fields,
        )
        if as_dict:
            res_dicts = [
                {
                    self._get_local_field(field): value
                    for field, value in record_dict.items()
                }
                for record_dict in records
            ]
        else:
            res_objs = [
                self.record_class(
                    client=self._client,
                    record=record,
                    fields=_fields,
                )
                for record in records
            ]
        if not optional:
            required_ids = {_ids} if isinstance(_ids, int) else set(_ids)
            found_ids: set[int] = (
                set(record["id"] for record in res_dicts)
                if as_dict
                else set(record.id for record in res_objs)
            )
            missing_ids = required_ids - found_ids
            if missing_ids:
                raise RecordNotFoundError(
                    (
                        f"{self.record_class.__name__} records "
                        "with IDs not found: "
                        f"{', '.join(str(i) for i in sorted(missing_ids))}"
                    ),
                )
        return res_dicts if as_dict else res_objs

    @overload
    def get(
        self,
        id: int,
        *,
        fields: Iterable[str] | None = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> R: ...

    @overload
    def get(
        self,
        id: int,
        *,
        fields: Iterable[str] | None = ...,
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> dict[str, Any]: ...

    @overload
    def get(
        self,
        id: int,
        *,
        fields: Iterable[str] | None = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> R | None: ...

    @overload
    def get(
        self,
        id: int,
        *,
        fields: Iterable[str] | None = ...,
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> dict[str, Any] | None: ...

    @overload
    def get(
        self,
        id: int,
        *,
        fields: Iterable[str] | None = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> R | dict[str, Any] | None: ...

    def get(
        self,
        id: int,  # noqa: A002
        fields: Iterable[str] | None = None,
        as_dict: bool = False,
        optional: bool = False,
    ) -> R | dict[str, Any] | None:
        try:
            return self.list(
                id,
                fields=fields,
                as_dict=as_dict,
                optional=True,
            )[0]
        except IndexError:
            if optional:
                return None
            else:
                raise RecordNotFoundError(
                    (
                        f"{self.record_class.__name__} record not found "
                        f"with ID: {id}"
                    ),
                ) from None

    @overload
    def get_by_unique_field(
        self,
        field: str,
        value: Any,
        *,
        filters: Iterable[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> int: ...

    @overload
    def get_by_unique_field(
        self,
        field: str,
        value: Any,
        *,
        filters: Iterable[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> int | None: ...

    @overload
    def get_by_unique_field(
        self,
        field: str,
        value: Any,
        *,
        filters: Iterable[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_by_unique_field(
        self,
        field: str,
        value: Any,
        *,
        filters: Iterable[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_by_unique_field(
        self,
        field: str,
        value: Any,
        *,
        filters: Iterable[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> dict[str, Any] | None: ...

    @overload
    def get_by_unique_field(
        self,
        field: str,
        value: Any,
        *,
        filters: Iterable[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> dict[str, Any]: ...

    @overload
    def get_by_unique_field(
        self,
        field: str,
        value: Any,
        *,
        filters: Iterable[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> R | None: ...

    @overload
    def get_by_unique_field(
        self,
        field: str,
        value: Any,
        *,
        filters: Iterable[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> R: ...

    @overload
    def get_by_unique_field(
        self,
        field: str,
        value: Any,
        *,
        filters: Iterable[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> R | int | dict[str, Any] | None: ...

    def get_by_unique_field(
        self,
        field: str,
        value: Any,
        filters: Iterable[FilterCriterion] | None = None,
        fields: Iterable[str] | None = None,
        as_id: bool = False,
        as_dict: bool = False,
        optional: bool = False,
    ) -> R | int | dict[str, Any] | None:
        field_filter = [(field, "=", value)]
        try:
            records = self.search(
                filters=(
                    list(itertools.chain(field_filter, filters))
                    if filters
                    else field_filter
                ),
                fields=fields,
                as_id=as_id,
                as_dict=as_dict,
            )
            if len(records) > 1:
                raise MultipleRecordsFoundError(
                    (
                        f"Multiple {self.record_class.__name__} records "
                        f"found with {field!r} value {value!r} "
                        "when only one was expected: "
                        f"{', '.join(str(r) for r in records)}"
                    ),
                )
            return records[0]
        except IndexError:
            if optional:
                return None
            else:
                raise RecordNotFoundError(
                    (
                        f"{self.record_class.__name__} record not found "
                        f"with {field!r} value: {value}"
                    ),
                ) from None

    @overload
    def search(
        self,
        filters: Sequence[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        order: str | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
    ) -> builtins.list[R]: ...

    @overload
    def search(
        self,
        filters: Sequence[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        order: str | None = ...,
        *,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
    ) -> builtins.list[int]: ...

    @overload
    def search(
        self,
        filters: Sequence[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        order: str | None = ...,
        as_id: Literal[False] = ...,
        *,
        as_dict: Literal[True],
    ) -> builtins.list[dict[str, Any]]: ...

    @overload
    def search(
        self,
        filters: Sequence[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        order: str | None = ...,
        *,
        as_id: Literal[True],
        as_dict: Literal[True],
    ) -> builtins.list[int]: ...

    @overload
    def search(
        self,
        filters: Sequence[FilterCriterion] | None = ...,
        fields: Iterable[str] | None = ...,
        order: str | None = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
    ) -> (
        builtins.list[R] | builtins.list[int] | builtins.list[dict[str, Any]]
    ): ...

    def search(
        self,
        filters: Sequence[FilterCriterion] | None = None,
        fields: Iterable[str] | None = None,
        order: str | None = None,
        as_id: bool = False,
        as_dict: bool = False,
    ) -> builtins.list[R] | builtins.list[int] | builtins.list[dict[str, Any]]:
        ids: list[int] = self._env.search(
            (self._encode_filters(filters) if filters else []),
            order=order,
        )
        if as_id:
            return ids
        if ids:
            return self.list(
                ids,
                fields=fields,
                as_dict=as_dict,
                # A race condition might occur where a record is deleted
                # after finding the ID but before querying the contents of it.
                # If this happens, silently drop the record ID from the result.
                optional=True,
            )
        return []  # type: ignore[return-value]

    def _encode_filters(
        self,
        filters: Sequence[FilterCriterion],
    ) -> builtins.list[str | tuple[str, str, Any]]:
        _filters: list[str | tuple[str, str, Any]] = []
        for f in filters:
            if isinstance(f, str):
                _filters.append(f)
            else:
                field_type, field_name = self._encode_filter_field(field=f[0])
                operator: str = f[1]
                if operator in ("in", "not in"):
                    value = [
                        self._encode_value(type_hint=field_type, value=v)
                        for v in f[2]
                    ]
                elif operator in ("child_of", "parent_of"):
                    value = (
                        [
                            self._encode_value(type_hint=field_type, value=v)
                            for v in f[2]
                        ]
                        if isinstance(f[2], (list, set, tuple))
                        else self._encode_value(
                            type_hint=field_type,
                            value=f[2],
                        )
                    )
                else:
                    value = self._encode_value(
                        type_hint=field_type,
                        value=f[2],
                    )
                _filters.append((field_name, operator, value))
        return _filters

    def _encode_filter_field(self, field: str) -> tuple[Any, str]:
        # The field reference in a filter may be nested.
        # Split the reference by the delimiter (.),
        # so we can perform a recursive lookup of the correct field
        # to return.
        field_refs = field.split(".")
        # Handle nested field references.
        # These are mapped to model refs in the Odoo client,
        # with the remote equivalent of the field names encoded
        # in the return value.
        # If no model ref is found for the given field reference,
        # the type will be set to Any.
        if len(field_refs) > 1:
            local_field = self._decode_field(field_refs[0])
            remote_field = self._encode_field(field_refs[0])
            if local_field not in self._record_type_hints:
                return (Any, f"{remote_field}.{'.'.join(field_refs[1:])}")
            type_hint: Any = self._record_type_hints[local_field]
            model_ref = ModelRef.get(type_hint)
            if model_ref:
                record_class: Type[RecordBase] = (
                    self.record_class
                    if model_ref.record_class is Self
                    else model_ref.record_class
                )
                type_hint, remote_field_refs = (
                    self._client._record_manager_mapping[
                        record_class  # type: ignore[index]
                    ]._encode_filter_field(
                        field=".".join(field_refs[1:]),
                    )
                )
                return (type_hint, f"{remote_field}.{remote_field_refs}")
            return (Any, f"{remote_field}.{'.'.join(field_refs[1:])}")
        # Base base: The field reference is not nested
        # (references a local field on this manager's record class.)
        # Fetch the local and remote representations of the given field.
        # Field aliases and model ref target fields are resolved
        # at this point.
        local_field = self._decode_field(field)
        remote_field = self._encode_field(field)
        # If there is no type hint defined for the given field,
        # return the Any type to denote that no processing should be done.
        if local_field not in self._record_type_hints:
            return (Any, remote_field)
        type_hint = self._record_type_hints[local_field]
        return (type_hint, remote_field)

    def create(self, **fields: Any) -> int:
        return self._env.create(self._encode_create_fields(fields))

    def create_multi(self, *records: Mapping[str, Any]) -> builtins.list[int]:
        res: int | list[int] = self._env.create(
            [self._encode_create_fields(record) for record in records],
        )
        if isinstance(res, int):
            return [res]
        return res

    def _encode_create_fields(
        self,
        fields: Mapping[str, Any],
    ) -> dict[str, Any]:
        create_fields: dict[str, Any] = {}
        field_remote_mapping: dict[str, str] = {}
        for field, value in fields.items():
            remote_field, remote_value = self._encode_create_field(
                field=field,
                value=value,
            )
            if remote_field in field_remote_mapping:
                raise ValueError(
                    (
                        "Conflicting field keys found that resolve to the "
                        "same remote field when creating record from "
                        f"mapping: {fields} (conflicting keys: "
                        f"{field_remote_mapping[remote_field]}, {field})"
                    ),
                )
            field_remote_mapping[remote_field] = field
            create_fields[remote_field] = remote_value
        return create_fields

    def _encode_create_field(
        self,
        field: str,
        value: Any,
    ) -> tuple[str, Any]:
        # Fetch the local and remote representations of the given field.
        # Field aliases and model ref target fields are resolved
        # at this point.
        local_field = self._decode_field(field)
        remote_field = self._encode_field(field)
        # If there is no type hint for the given field, map the value
        # to the field unchanged.
        if local_field not in self._record_type_hints:
            return (remote_field, value)
        # Fetch the type hint for parsing.
        type_hint = self._record_type_hints[local_field]
        # If this field is a model ref, encode the model ref
        # according to the given value's type, and map the result
        # to the Odoo model's ref field name.
        model_ref = ModelRef.get(type_hint)
        if model_ref:
            # NOTE(callumdickinson): JSON RPC API model link reference.
            # https://www.odoo.com/documentation/14.0/developer/reference/addons/orm.html#odoo.models.Model.write
            #  * (0, 0, {values}) - Link to a new record that needs to
            #    be created with the given values dictionary.
            #  * (1, id, {values}) - Update the linked record *id*
            #    (write *values* to it).
            #  * (2, id) - Remove and delete the linked record *id*.
            #    Calls ``unlink`` on ID, deleting the object
            #    completely, and the link to it as well.
            #  * (3, id) - Cut the link to the linked record *id*.
            #    Deletes the relationship between the two objects,
            #    but does not delete the target object itself.
            #  * (4, id) - Link to existing record *id*
            #    (adds a relationship).
            #  * (5) - Unlink all record links.
            #    Functions like using (3,ID) for all linked records.
            #  * (6, 0, [ids]) - Replace the list of linked IDs
            #    with *ids*. Functions like using (5), then (4, id)
            #    for each ID in the list of IDs.
            attr_type: Any = get_type_args(type_hint)[0]
            # If the field is a list of multiple model refs,
            # iterate over the given value and decode the elements
            # appropriately.
            if get_type_origin(attr_type) is list:
                if not value:
                    return (remote_field, [])
                remote_values: list[
                    tuple[int, int] | tuple[int, int, dict[str, Any]]
                ] = []
                for v in value:
                    if isinstance(v, int):
                        remote_values.append((4, v))
                    elif isinstance(v, RecordBase):
                        remote_values.append((4, v.id))
                    elif isinstance(v, dict):
                        manager = (
                            self
                            if model_ref.record_class is Self
                            else self._client._record_manager_mapping[
                                model_ref.record_class
                            ]
                        )
                        remote_values.append(
                            (0, 0, manager._encode_create_fields(v)),
                        )
                    else:
                        raise ValueError(
                            (
                                "Unsupported element value for model "
                                f"ref list field '{field}' "
                                f"when creating record: {v}"
                            ),
                        )
                return (remote_field, remote_values)
            # If the value type is an integer, treat it as a record ID
            # and assign i to the field.
            if isinstance(value, int):
                return (remote_field, value)
            # If the value type is a record object, then treat it as if
            # it already exists on Odoo, and return the record ID to assign
            # to the field.
            if isinstance(value, RecordBase):
                return (remote_field, value.id)
            # NOTE(callumdickinson): Nested records cannot be created
            # for singular record refs (Many2one relations).
            # The target record must be created separately first,
            # then linked in this record using either the target record's
            # object or ID.
            raise ValueError(
                (
                    f"Unsupported value for model ref field '{field}' "
                    f"when creating record: {value}"
                ),
            )
        # For regular fields, encode the value based on its type hint.
        return (
            remote_field,
            self._encode_value(type_hint=type_hint, value=value),
        )

    def update(self, record: int | R, **fields: Any) -> None:
        self._env.update(
            record.id if isinstance(record, RecordBase) else record,
            self._encode_create_fields(fields),
        )

    def unlink(self, *records: int | R | Iterable[int | R]) -> None:
        _ids: list[int] = []
        for ids in records:
            if isinstance(ids, int):
                _ids.append(ids)
            elif isinstance(ids, RecordBase):
                _ids.append(ids.id)
            else:
                _ids.extend(
                    ((i.id if isinstance(i, RecordBase) else i) for i in ids),
                )
        self._env.unlink(_ids)

    def delete(self, *records: R | int | Iterable[R | int]) -> None:
        self.unlink(*records)

    def _get_remote_field(self, field: str) -> str:
        # If the field is a model ref, use the reference field name
        # as the remote field.
        if field in self._record_type_hints:
            model_ref = ModelRef.get(self._record_type_hints[field])
            if model_ref:
                field = model_ref.field
        # Map the local field to the correct remote field name
        # based on the version of the Odoo server.
        return get_mapped_field(
            field_mapping=self.record_class._field_mapping,
            odoo_version=self._odoo.version,
            field=field,
        )

    def _get_local_field(self, field: str) -> str:
        # Map the remote field to the correct local field name
        # based on the version of the Odoo server.
        local_field = get_mapped_field(
            field_mapping=self._field_mapping_reverse,
            odoo_version=self._odoo.version,
            field=field,
        )
        # If the field is a model ref, find the local field
        # presenting the model ref's record IDs.
        if local_field in self._model_ref_mapping:
            return self._model_ref_mapping[local_field]
        return local_field

    def _resolve_alias(self, field: str) -> str:
        if field not in self._record_type_hints:
            return field
        # NOTE(callumdickinson): Continually resolve field aliases
        # until we get to a field that is not an alias.
        resolved_aliases: set[str] = set()
        alias_chain: list[str] = []
        annotation = FieldAlias.get(self._record_type_hints[field])
        while annotation:
            # Check if field aliases loop back on each other.
            if field in resolved_aliases:
                raise ValueError(
                    (
                        "Found recursive field alias definitions "
                        f"on {self.record_class.__name__}: "
                        f"{' -> '.join(alias_chain)}"
                    ),
                )
            resolved_aliases.add(field)
            alias_chain.append(field)
            # Resolve the target field from the alias annotation,
            # and try to fetch the target field's annotation to check
            # if it is also an alias.
            field = annotation.field
            if field not in self._record_type_hints:
                break
            annotation = FieldAlias.get(self._record_type_hints[field])
        return field

    def _decode_field(self, field: str) -> str:
        return self._get_local_field(self._resolve_alias(field))

    def _encode_field(self, field: str) -> str:
        return self._get_remote_field(self._resolve_alias(field))

    def _encode_value(self, type_hint: Any, value: Any) -> Any:
        # Field aliases should be parsed before we get to this point.
        # Handle model refs specially.
        if ModelRef.is_annotated(type_hint):
            attr_type = get_type_origin(get_type_args(type_hint)[0])
            if attr_type is list:
                # False, None or empty structures are expected here.
                if not value:
                    return []
                if isinstance(value, (list, set, tuple)):
                    return [
                        (
                            record.id
                            if isinstance(record, RecordBase)
                            else record
                        )
                        for record in value
                    ]
            if isinstance(value, RecordBase):
                return value.id
            # None is our internal representation of "no value".
            # Odoo generally expects False.
            if value is None:
                return False
            # Should be a record ID (int), or False.
            return value
        # For every other field type, parse the possible value types
        # from the type hint.
        # First, remove Annotated to get the actual attribute type.
        type_hint_origin = get_type_origin(type_hint) or type_hint
        attr_type = (
            get_type_args(type_hint)[0]
            if type_hint_origin is Annotated
            else type_hint
        )
        # Next, get a list of allowed values types from the attribute type.
        # If there is only one, create a list containing only that type.
        attr_type_origin = get_type_origin(attr_type) or attr_type
        value_types = (
            get_type_args(attr_type)
            if attr_type_origin is Union or attr_type_origin is UnionType
            else [attr_type]
        )
        # Recursively handle the types that need to be serialised.
        for value_type in value_types:
            value_type_origin = get_type_origin(value_type) or value_type
            if value_type is date and isinstance(value, date):
                return value.strftime(DEFAULT_SERVER_DATE_FORMAT)
            if value_type is datetime and isinstance(value, datetime):
                return value.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            if value_type_origin is list and isinstance(
                value,
                (list, set, tuple),
            ):
                v_type = get_type_args(value_type)[0]
                return [self._encode_value(v_type, v) for v in value]
        return value
