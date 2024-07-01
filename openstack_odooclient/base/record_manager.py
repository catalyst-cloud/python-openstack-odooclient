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

from datetime import date, datetime
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
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

from ..exceptions import RecordNotFoundError
from ..util import (
    DEFAULT_SERVER_DATE_FORMAT,
    DEFAULT_SERVER_DATETIME_FORMAT,
    get_mapped_field,
)
from .record import FieldAlias, ModelRef, RecordBase

if TYPE_CHECKING:
    from odoorpc import ODOO  # type: ignore[import]
    from odoorpc.env import Environment  # type: ignore[import]

    from .client import ClientBase

Record = TypeVar("Record", bound=RecordBase)
FilterCriterion = Union[Tuple[str, str, Any], Sequence[Any], str]


class RecordManagerBase(Generic[Record]):
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
    >>> class CustomRecordManager(RecordManager[CustomRecord]):
    ...     env_name = "custom.record"
    ...     record_class = CustomRecord

    Once you have your manager class, subclass the ``Client``
    class and add a type hint for your custom record manager.
    This will allow you to use custom record managers on your
    Odoo client objects.

    >>> class CustomClient(Client):
    ...     custom_records: CustomRecordManager
    """

    env_name: str
    """The Odoo environment (model) name to manage."""

    record_class: Type[Record]
    """The record object type to instantiate using this manager."""

    default_fields: Optional[Tuple[str, ...]] = None
    """List of fields to fetch by default if a field list is not supplied
    in queries.

    By default, all fields on the model will be fetched.
    """

    def __init__(self, client: ClientBase) -> None:
        self._client = client
        """The Odoo client object the manager uses."""
        # Assign this record manager object as the manager
        # responsible for the configured record class in the client.
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
        self._model_ref_mapping: Dict[str, str] = {}
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
        ids: Union[int, Iterable[int]],
        *,
        fields: Optional[Iterable[str]] = ...,
        as_dict: Literal[False] = ...,
        optional: bool = ...,
    ) -> List[Record]: ...

    @overload
    def list(
        self,
        ids: Union[int, Iterable[int]],
        *,
        fields: Optional[Iterable[str]] = ...,
        as_dict: Literal[True],
        optional: bool = ...,
    ) -> List[Dict[str, Any]]: ...

    @overload
    def list(
        self,
        ids: Union[int, Iterable[int]],
        *,
        fields: Optional[Iterable[str]] = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> Union[List[Record], List[Dict[str, Any]]]: ...

    def list(
        self,
        ids: Union[int, Iterable[int]],
        fields: Optional[Iterable[str]] = None,
        as_dict: bool = False,
        optional: bool = False,
    ) -> Union[List[Record], List[Dict[str, Any]]]:
        """Get one or more specific records by ID.

        By default all fields available on the record model
        will be selected, but this can be filtered using the
        ``fields`` parameter.

        Use the ``as_dict`` parameter to return records as ``dict``
        objects, instead of record objects.

        By default, the method checks that all provided IDs
        were found and returned (and will raise an error if any are missing),
        at the cost of a small performance hit.
        To instead return the list of records that were found
        without raising an error, set ``optional`` to ``True``.

        If ``ids`` is given an empty iterator, this method
        returns an empty list.

        :param ids: Record ID, or list of record IDs
        :type ids: Union[int, Iterable[int]]
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Optional[Iterable[str]], optional
        :param as_dict: Return records as dictionaries, defaults to ``False``
        :type as_dict: bool, optional
        :param optional: Disable missing record errors, defaults to ``False``
        :type optional: bool, optional
        :raises RecordNotFoundError: If IDs are required but some are missing
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
            found_ids: Set[int] = (
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
    def search(
        self,
        filters: Optional[Sequence[FilterCriterion]] = ...,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
    ) -> List[Record]: ...

    @overload
    def search(
        self,
        filters: Optional[Sequence[FilterCriterion]] = ...,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        *,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
    ) -> List[int]: ...

    @overload
    def search(
        self,
        filters: Optional[Sequence[FilterCriterion]] = ...,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: Literal[False] = ...,
        *,
        as_dict: Literal[True],
    ) -> List[Dict[str, Any]]: ...

    @overload
    def search(
        self,
        filters: Optional[Sequence[FilterCriterion]] = ...,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        *,
        as_id: Literal[True],
        as_dict: Literal[True],
    ) -> List[int]: ...

    @overload
    def search(
        self,
        filters: Optional[Sequence[FilterCriterion]] = ...,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
    ) -> Union[List[Record], List[int], List[Dict[str, Any]]]: ...

    def search(
        self,
        filters: Optional[Sequence[FilterCriterion]] = None,
        fields: Optional[Iterable[str]] = None,
        order: Optional[str] = None,
        as_id: bool = False,
        as_dict: bool = False,
    ) -> Union[List[Record], List[int], List[Dict[str, Any]]]:
        """Query the ERP for records, optionally defining
        filters to constrain the search and other parameters,
        and return the results.

        Query filters should be defined using the ORM API search domain
        format. For more information on the ORM API search domain format:

        https://www.odoo.com/documentation/14.0/developer/reference/addons/orm.html#search-domains

        Filters are a sequence of criteria, where each criterion
        is one of the following types of values:

        * A 3-tuple or 3-element sequence in ``(field_name, operator, value)``
        format, where:

          * ``field_name`` (``str``) is the the name of the field to filter by.
          * ``operator`` (`str`) is the comparison operator to use (for more
            information on the available operators, check the ORM API
            search domain documentation).
          * ``value`` (`Any`) is the value to compare records against.

        * A logical operator which prefixes the following filter criteria
        to form a **criteria combination**:

          * ``&`` is a logical AND. Records only match if **both** of the
            following **two** criteria match.
          * ``|`` is a logical OR. Records match if **either** of the
            following **two** criteria match.
          * ``!`` is a logical NOT (negation). Records match if the
            following **one** criterion does **NOT** match.

        Every criteria combination is implicitly combined using a logical AND
        to form the overall filter to use to query records.

        For the field value, this method accepts the same types as defined
        on the record objects.

        In addition to the native Odoo field names, field aliases
        and model ref field names can be specified as the field name
        in the search filter. Record objects can also be directly
        passed as the value on a filter, not just record IDs.

        When specifying a range of possible values, lists, tuples
        and sets are supported.

        Search criteria using nested field references can be defined
        by using the dot-notation (``.``) to specify what field on what
        record reference to check.
        Field names and values for nested field references are
        validated and encoded just like criteria for standard
        field references.

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
        :type filters: Union[Tuple[str, str, Any], Sequence[Any], str] | None
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[str] or None, optional
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
    ) -> List[Union[str, Tuple[str, str, Any]]]:
        _filters: List[Union[str, Tuple[str, str, Any]]] = []
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

    def _encode_filter_field(self, field: str) -> Tuple[Any, str]:
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

    def create(self, **fields) -> int:
        """Create a new record, using the specified keyword arguments
        as input fields.

        This method allows a lot of flexibility in how input fields
        should be defined.

        The fields passed to this method should use the same field names
        and value types that are defined on the record classes.
        The Odoo Client library will convert the values to the formats
        that the Odoo API expects.

        For example, when defining references to another record,
        you can either pass the record ID, or the record object.
        The field name can also either be for the ID or the object.

        Field aliases are also resolved to their target field names.

        When creating a record with a list of references to another record
        (a ``One2many`` or ``Many2many`` relation), it is possible to nest
        record mappings where an ID or object would normally go.
        New records will be created for those mappings, and linked
        to the parent record. Nested record mappings are recursively validated
        and processed in the same way as the parent record.

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

        The record mappings should be in the same format as with
        the ``create`` method.

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
    ) -> Tuple[str, Any]:
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

    def unlink(
        self,
        *records: Union[int, Record, Iterable[Union[int, Record]]],
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
        resolved_aliases: Set[str] = set()
        alias_chain: List[str] = []
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
        type_hint_origin = get_type_origin(type_hint) or type_hint
        attr_type = (
            get_type_args(type_hint)[0]
            if type_hint_origin is Annotated
            else type_hint_origin
        )
        attr_type_origin = get_type_origin(attr_type) or attr_type
        value_types = (
            get_type_args(attr_type)
            if attr_type_origin is Union
            else [attr_type_origin]
        )
        # Recursively handle the types that need to be serialised.
        for value_type in value_types:
            if value_type is date and isinstance(value, date):
                return value.strftime(DEFAULT_SERVER_DATE_FORMAT)
            if value_type is datetime and isinstance(value, datetime):
                return value.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            if value_type is list and isinstance(value, (list, set, tuple)):
                v_type = get_type_args(type_hint)[0]
                return [self._encode_value(v_type, v) for v in value]
        return value
