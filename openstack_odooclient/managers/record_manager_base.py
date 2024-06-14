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

from datetime import date, datetime, time
from typing import TYPE_CHECKING, Generic, TypeVar, overload

from typing_extensions import (
    Annotated,
    get_args as get_type_args,
    get_origin as get_type_origin,
    get_type_hints,
)

from ..exceptions import RecordNotFoundError
from .record_base import RecordBase
from .util import (
    DEFAULT_SERVER_DATE_FORMAT,
    DEFAULT_SERVER_DATETIME_FORMAT,
    DEFAULT_SERVER_TIME_FORMAT,
    ModelRef,
    get_mapped_field,
)

if TYPE_CHECKING:
    from typing import (
        Any,
        Dict,
        Iterable,
        List,
        Literal,
        Mapping,
        Optional,
        Sequence,
        Set,
        Tuple,
        Type,
        Union,
    )

    from odoorpc import ODOO  # type: ignore[import]
    from odoorpc.env import Environment  # type: ignore[import]

    from .. import client

Record = TypeVar("Record", bound=RecordBase)


class RecordManagerBase(Generic[Record]):
    env_name: str
    """The Odoo environment (model) name to manage."""

    record_class: Type[Record]
    """The record object type to instatiate using this manager."""

    default_fields: Optional[Set[str]] = None
    """List of fields to fetch by default if a field list is not supplied
    in queries.

    By default, all fields on the model will be fetched.
    """

    def __init__(self, client: client.Client) -> None:
        self._client = client
        self._field_mapping_reverse = {
            odoo_version: {
                remote_field: local_field
                for local_field, remote_field in field_mapping.items()
            }
            for odoo_version, field_mapping in (
                self.record_class._field_mapping.items()
            )
        }
        self._client._record_manager_mapping[self.record_class] = self

    @property
    def _odoo(self) -> ODOO:
        return self._client._odoo

    @property
    def _env(self) -> Environment:
        return self._odoo.env[self.env_name]

    @overload
    def list(
        self,
        ids: Union[int, Iterable[int]],
        fields: Optional[Iterable[str]] = ...,
        as_dict: Literal[False] = ...,
    ) -> List[Record]: ...

    @overload
    def list(
        self,
        ids: Union[int, Iterable[int]],
        fields: Optional[Iterable[str]] = ...,
        *,
        as_dict: Literal[True],
    ) -> List[Dict[str, Any]]: ...

    @overload
    def list(
        self,
        ids: Union[int, Iterable[int]],
        fields: Optional[Iterable[str]] = ...,
        as_dict: bool = ...,
    ) -> Union[List[Record], List[Dict[str, Any]]]: ...

    def list(
        self,
        ids: Union[int, Iterable[int]],
        fields: Optional[Iterable[str]] = None,
        as_dict: bool = False,
    ) -> Union[List[Record], List[Dict[str, Any]]]:
        """Get one or more specific records by ID.

        By default all fields available on the record model
        will be selected, but this can be filtered using the
        ``fields`` parameter.

        Use the ``as_dict`` parameter to return records as ``dict``
        objects, instead of record objects.

        If ``ids`` is given an empty iterator, this method
        returns an empty list.

        :param ids: Record ID, or list of record IDs
        :type ids: Union[int, Iterable[int]]
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Optional[Iterable[str]], optional
        :param as_dict: Return records as dictionaries, defaults to ``False``
        :type as_dict: bool, optional
        :return: List of records
        :rtype: list[Record] or list[dict[str, Any]]
        """
        if isinstance(ids, int):
            _ids: Union[int, List[int]] = ids
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
        records: Iterable[Dict[str, Any]] = self._env.read(
            _ids,
            fields=_fields,
        )
        if as_dict:
            return [
                {
                    self._get_local_field(field): value
                    for field, value in record_dict.items()
                }
                for record_dict in records
            ]
        return [
            self.record_class(
                client=self._client,
                manager=self,
                record=record,
                fields=_fields,
            )
            for record in records
        ]

    @overload
    def get(
        self,
        id: int,  # noqa: A002
        *,
        fields: Optional[Iterable[str]] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> Record: ...

    @overload
    def get(
        self,
        id: int,  # noqa: A002
        *,
        fields: Optional[Iterable[str]] = ...,
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> Dict[str, Any]: ...

    @overload
    def get(
        self,
        id: int,  # noqa: A002
        *,
        fields: Optional[Iterable[str]] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> Optional[Record]: ...

    @overload
    def get(
        self,
        id: int,  # noqa: A002
        *,
        fields: Optional[Iterable[str]] = ...,
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> Optional[Dict[str, Any]]: ...

    @overload
    def get(
        self,
        id: int,  # noqa: A002
        *,
        fields: Optional[Iterable[str]] = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> Optional[Union[Record, Dict[str, Any]]]: ...

    def get(
        self,
        id: int,  # noqa: A002
        fields: Optional[Iterable[str]] = None,
        as_dict: bool = False,
        optional: bool = False,
    ) -> Optional[Union[Record, Dict[str, Any]]]:
        """Get a single record by ID.

        By default all fields available on the record model
        will be selected, but this can be filtered using the
        ``fields`` parameter.

        Use the ``as_dict`` parameter to return the record as
        a ``dict`` object, instead of a record object.

        :param ids: Record ID
        :type ids: int
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[str] or None, optional
        :param as_dict: Return record as a dictionary, defaults to ``False``
        :type as_dict: bool, optional
        :param optional: Return ``None`` if not found, defaults to ``False``
        :raises RecordNotFoundError: Record with the given ID not found
        :return: List of records
        :rtype: Union[Record, List[str, Any]]
        """
        try:
            return self.list(id, fields=fields, as_dict=as_dict)[0]
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
    def search(
        self,
        filters: Optional[Sequence[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
    ) -> List[Record]: ...

    @overload
    def search(
        self,
        filters: Optional[Sequence[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        *,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
    ) -> List[int]: ...

    @overload
    def search(
        self,
        filters: Optional[Sequence[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: Literal[False] = ...,
        *,
        as_dict: Literal[True],
    ) -> List[Dict[str, Any]]: ...

    @overload
    def search(
        self,
        filters: Optional[Sequence[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        *,
        as_id: Literal[True],
        as_dict: Literal[True],
    ) -> List[int]: ...

    @overload
    def search(
        self,
        filters: Optional[Sequence[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
    ) -> Union[List[Record], List[int], List[Dict[str, Any]]]: ...

    def search(
        self,
        filters: Optional[Sequence[Any]] = None,
        fields: Optional[Iterable[str]] = None,
        order: Optional[str] = None,
        as_id: bool = False,
        as_dict: bool = False,
    ) -> Union[List[Record], List[int], List[Dict[str, Any]]]:
        """Query the ERP for records, optionally defining
        filters to constrain the search and other parameters,
        and return the results.

        Query filters should be defined using the same format as OdooRPC,
        but some additional features are supported:

        * Odoo client field aliases can be specified as the field name,
          in additional to the original field name on the Odoo model
          (e.g. ``create_user`` instead of ``create_uid``).
        * Record objects can be directly passed as the value
          on a filter, where a record ID would normally be expected.
        * Sets and tuples are supported when specifying a range of values,
          in addition to lists.

        To search *all* records, leave ``filters`` unset
        (or set it to ``None``).

        By default all fields available on the record model
        will be selected, but this can be filtered using the
        ``fields`` parameter.

        Use the ``as_id`` parameter to return the record as
        a list of IDs, instead of record objects.

        Use the ``as_dict`` parameter to return the record as
        a list of ``dict`` objects, instead of record objects.

        :param filters: Filters to query by, defaults to ``None`` (no filters)
        :type filters: Sequence[Any] or None, optional
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[int] or None, optional
        :param order: Order results by field name, defaults to ``None``
        :type order: str or None, optional
        :param as_id: Return the record IDs only, defaults to ``False``
        :type as_id: bool, optional
        :param as_dict: Return records as dictionaries, defaults to ``False``
        :type as_dict: bool, optional
        :return: List of records
        :rtype: list[Record] or list[int] or list[dict[str, Any]]
        """
        ids: List[int] = self._env.search(
            (self._encode_filters(filters) if filters else []),
            order=order,
        )
        if as_id:
            return ids
        if ids:
            return self.list(ids, fields=fields, as_dict=as_dict)
        return []  # type: ignore[return-value]

    def create(self, **fields) -> int:
        """Create a new record, using the specified keyword arguments
        as input fields.

        To fetch the newly created record object,
        pass the returned ID to the ``get`` method.

        :return: The ID of the newly created record
        :rtype: int
        """
        return self._env.create(self._encode_create_fields(fields))

    def create_multi(self, *records: Mapping[str, Any]) -> List[int]:
        """Create one or more new records in a single request,
        passing in the mappings containing the record's input fields
        as positional arguments.

        To fetch the newly created record objects,
        pass the returned IDs to the ``list`` method.

        :return: The IDs of the newly created records
        :rtype: List[int]
        """
        res: Union[int, List[int]] = self._env.create(
            [self._encode_create_fields(record) for record in records],
        )
        if isinstance(res, int):
            return [res]
        return res

    def _encode_create_fields(
        self,
        fields: Mapping[str, Any],
    ) -> Dict[str, Any]:
        create_fields: Dict[str, Any] = {}
        field_remote_mapping: Dict[str, str] = {}
        type_hints = get_type_hints(self.record_class, include_extras=True)
        for field, value in fields.items():
            remote_field, remote_value = self._encode_create_field(
                type_hints=type_hints,
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
        type_hints: Mapping[str, Type[Any]],
        field: str,
        value: Any,
    ) -> Tuple[str, Any]:
        # Fetch the local and remote representations of the given field.
        # Field aliases are resolved at this point.
        orig_field = self._resolve_alias(field)
        local_field = self._get_local_field(orig_field)
        remote_field = self._get_remote_field(orig_field)
        # If there is no type hint for the given field, map the value
        # to the field unchanged.
        if local_field not in type_hints:
            return (remote_field, value)
        # Fetch the type hint for parsing.
        type_hint = type_hints[local_field]
        # Perform special handling of annotated fields.
        if get_type_origin(type_hint) is Annotated:
            type_args = get_type_args(type_hint)
            attr_type: Type[Any] = type_args[0]
            annotations = type_args[1:]
            if len(annotations) == 1:
                annotation = annotations[0]
                # If this field is a model ref, encode the model ref
                # according to the given value's type, and map the result
                # to the Odoo model's ref field name.
                if isinstance(annotation, ModelRef):
                    # NOTE(callumdickinson): JSON RPC API model link
                    # definition reference.
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
                    model_ref_field = self._get_remote_field(annotation.field)
                    # If the field is a list of multiple model refs,
                    # iterate over the given value and decode the elements
                    # appropriately.
                    if get_type_origin(attr_type) is list:
                        value_type = get_type_args(attr_type)[0]
                        if not value:
                            return (model_ref_field, [])
                        remote_values: List[
                            Union[
                                Tuple[int, int],
                                Tuple[int, int, Dict[str, Any]],
                            ],
                        ] = []
                        for v in value:
                            if isinstance(v, int):
                                remote_values.append((4, v))
                            elif isinstance(v, RecordBase):
                                remote_values.append((4, v.id))
                            elif isinstance(v, dict):
                                manager = self._client._record_manager_mapping[
                                    value_type
                                ]
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
                        return (model_ref_field, remote_values)
                    # If the value type is an integer,
                    # treat it as a record ID and assign i to the field.
                    if isinstance(value, int):
                        return (model_ref_field, value)
                    # If the value type is a record object,
                    # then treat it as if it already exists on Odoo,
                    # and return the record ID to assign to the field.
                    if isinstance(value, RecordBase):
                        return (model_ref_field, value.id)
                    # If the value type is a dictionary,
                    # then treat it as a nested record to be created
                    # alongside the parent record.
                    # Encode the contents of the dict recursively
                    # using the record class's manager object,
                    # and assign it to the parent record so they can
                    # both be created.
                    # TODO(callumdickinson): Check that this works.
                    if isinstance(value, dict):
                        return (
                            model_ref_field,
                            [
                                (
                                    0,
                                    0,
                                    self._client._record_manager_mapping[
                                        attr_type
                                    ]._encode_create_fields(value),
                                ),
                            ],
                        )
                    raise ValueError(
                        (
                            f"Unsupported value for model ref field '{field}' "
                            f"when creating record: {value}"
                        ),
                    )
                raise ValueError(
                    (
                        f"Unsupported annotation for field '{field}': "
                        f"{annotation}"
                    ),
                )
        # For regular fields, encode the value based on its type hint.
        return (
            remote_field,
            self._encode_create_value(type_hint=type_hint, value=value),
        )

    def _encode_create_value(self, type_hint: Type[Any], value: Any) -> Any:
        value_type = get_type_origin(type_hint)
        if value_type is date and isinstance(value, date):
            return value.strftime(DEFAULT_SERVER_DATE_FORMAT)
        if value_type is time and isinstance(value, time):
            return value.strftime(DEFAULT_SERVER_TIME_FORMAT)
        if value_type is datetime and isinstance(value, datetime):
            return value.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        if value_type is list and isinstance(value, (list, set, tuple)):
            v_type = get_type_args(type_hint)[0]
            return [self._encode_create_value(v_type, v) for v in value]
        return value

    def unlink(
        self,
        *records: Union[Record, int, Iterable[Union[Record, int]]],
    ) -> None:
        """Delete one or more records from Odoo.

        This method accepts either a record object or ID, or an iterable of
        either of those types. Multiple positional arguments are allowed.

        All specified records will be deleted in a single request.

        :param records: The records to delete (object, ID, or record/ID list)
        :type records: Union[Record, int, Iterable[Union[Record, int]]]
        """
        _ids: List[int] = []
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

    def delete(
        self,
        *records: Union[Record, int, Iterable[Union[Record, int]]],
    ) -> None:
        """Delete one or more records from Odoo.

        This method accepts either a record object or ID, or an iterable of
        either of those types. Multiple positional arguments are allowed.

        All specified records will be deleted in a single request.

        :param records: The records to delete (object, ID, or record/ID list)
        :type records: Union[Record, int, Iterable[Union[Record, int]]]
        """
        self.unlink(*records)

    def _get_remote_field(self, field: str) -> str:
        return get_mapped_field(
            field_mapping=self.record_class._field_mapping,
            odoo_version=self._odoo.version,
            field=field,
        )

    def _get_local_field(self, field: str) -> str:
        return get_mapped_field(
            field_mapping=self._field_mapping_reverse,
            odoo_version=self._odoo.version,
            field=field,
        )

    def _resolve_alias(self, alias: str) -> str:
        return self.record_class._resolve_alias(alias)

    def _encode_field(self, field: str) -> str:
        return self._get_remote_field(self._resolve_alias(field))

    def _encode_value(self, value: Any) -> Any:
        if isinstance(value, RecordBase):
            return value.id
        if isinstance(value, (date, time, datetime)):
            return value.isoformat()
        if isinstance(value, (list, set, tuple)):
            return [self._encode_value(v) for v in value]
        return value

    def _encode_filters(self, filters: Sequence[Any]) -> List[Any]:
        # TODO(callumdickinson): Parse nested field references
        # (e.g. "product.categ_id") in filters.
        _filters: List[Any] = []
        for f in filters:
            if isinstance(f, tuple):
                _filter = (
                    self._encode_field(f[0]),  # Field name.
                    f[1],  # Filter operator (=, >=, in, etc).
                    self._encode_value(f[2]),  # Possible value(s).
                )
            else:
                _filter = f
            _filters.append(_filter)
        return _filters
