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

from typing import TYPE_CHECKING, Protocol, TypeVar, overload

from ..record.base import RecordBase
from .types import FilterCriterion

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence
    from typing import Any, Literal, Type

    from odoorpc import ODOO  # type: ignore[import]
    from odoorpc.env import Environment  # type: ignore[import]

    from ..client import ClientBase

R = TypeVar("R", bound=RecordBase)
"""An invariant type variable for a record class.

To be used when defining record manager mixins,
or generic base classes operating on records.
"""


class RecordManagerProtocol(Protocol[R]):
    """The protocol for a record manager class.

    This defines all common attributes and stubs for methods available for
    implementations of record managers to use.

    The primary use of this class is to be subclassed by mixins, to provide
    type hinting for common attributes and methods available on the
    ``RecordManagerBase`` class.

    ``RecordManagerBase`` is the base class that provides the core
    functionality of a record manager, and that class should be subclassed
    to make a new record manager class.
    """

    env_name: str
    """The Odoo environment (model) name to manage."""

    record_class: Type[R]
    """The record object type to instantiate using this manager."""

    default_fields: tuple[str, ...] | None = None
    """List of fields to fetch by default if a field list is not supplied
    in queries.

    By default, all fields on the model will be fetched.
    """

    @property
    def _client(self) -> ClientBase:
        """The Odoo client object the manager uses."""
        ...

    @property
    def _odoo(self) -> ODOO:
        """The OdooRPC connection object this record manager uses."""
        ...

    @property
    def _env(self) -> Environment:
        """The OdooRPC environment object this record manager uses."""
        ...

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
        :type ids: int | Iterable[int]
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[str] | None, optional
        :param as_dict: Return records as dictionaries, defaults to ``False``
        :type as_dict: bool, optional
        :param optional: Disable missing record errors, defaults to ``False``
        :type optional: bool, optional
        :raises RecordNotFoundError: If IDs are required but some are missing
        :return: List of records
        :rtype: list[R] | list[dict[str, Any]]
        """
        ...

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
        :rtype: R | dict[str, Any] | None
        """
        ...

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
        """Query a unique record by a specific field.

        A number of parameters are available to configure the return type,
        and what happens when a result is not found.

        Additional filters can be added to the search query using the
        ``filters`` parameter. If defined, these filters will be appended
        to the unique field search filter. Filters should be defined
        using the same format that ``search`` uses.

        By default all fields available on the record model
        will be selected, but this can be filtered using the
        ``fields`` parameter.

        Use the ``as_id`` parameter to return the ID of the record,
        instead of the record object.

        Use the ``as_dict`` parameter to return the record as
        a ``dict`` object, instead of a record object.

        When ``optional`` is ``True``, ``None`` is returned if a record
        with the given name does not exist, instead of raising an error.

        *Added in version 0.2.1.*

        :param field: The unique field name to query by
        :type field: str
        :param value: The unique field value
        :type value: Any
        :param filters: Optional additional filters to apply, defaults to None
        :type filters: Iterable[FilterCriterion] | None, optional
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[str] | None, optional
        :param as_id: Return a record ID, defaults to False
        :type as_id: bool, optional
        :param as_dict: Return the record as a dictionary, defaults to False
        :type as_dict: bool, optional
        :param optional: Return ``None`` if not found, defaults to False
        :type optional: bool, optional
        :raises MultipleRecordsFoundError: Multiple records with the same name
        :raises RecordNotFoundError: Record with the given name not found
        :return: Query result (or ``None`` if record not found and optional)
        :rtype: R | int | dict[str, Any] | None
        """
        ...

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
        :type filters: tuple[str, str, Any] | Sequence[Any] | str | None
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[str] or None, optional
        :param order: Order results by field name, defaults to ``None``
        :type order: str or None, optional
        :param as_id: Return the record IDs only, defaults to ``False``
        :type as_id: bool, optional
        :param as_dict: Return records as dictionaries, defaults to ``False``
        :type as_dict: bool, optional
        :return: List of records
        :rtype: list[R] | list[int] | list[dict[str, Any]]
        """
        ...

    def create(self, **fields: Any) -> int:
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
        ...

    def create_multi(self, *records: Mapping[str, Any]) -> builtins.list[int]:
        """Create one or more new records in a single request,
        passing in the mappings containing the record's input fields
        as positional arguments.

        The record mappings should be in the same format as with
        the ``create`` method.

        To fetch the newly created record objects,
        pass the returned IDs to the ``list`` method.

        :return: The IDs of the newly created records
        :rtype: list[int]
        """
        ...

    def update(self, record: int | R, **fields: Any) -> None:
        """Update one or more fields on the given record in place.

        Field names are passed as keyword arguments.
        This method has the same flexibility with regards to what
        field names are used as when creating records; for example,
        when updating a model ref, either its ID (e.g. ``user_id``)
        or object (e.g. ``user``) field names can be used.

        *Added in version 0.2.1.*

        :param record: The record to update (object or ID)
        :type record: int | R
        """
        ...

    def unlink(self, *records: int | R | Iterable[int | R]) -> None:
        """Delete one or more records from Odoo.

        This method accepts either a record object or ID, or an iterable of
        either of those types. Multiple positional arguments are allowed.

        All specified records will be deleted in a single request.

        :param records: The records to delete (object, ID, or record/ID list)
        :type records: Record | int | Iterable[Record | int]
        """
        ...

    def delete(self, *records: R | int | Iterable[R | int]) -> None:
        """Delete one or more records from Odoo.

        This method accepts either a record object or ID, or an iterable of
        either of those types. Multiple positional arguments are allowed.

        All specified records will be deleted in a single request.

        :param records: The records to delete (object, ID, or record/ID list)
        :type records: Record | int | Iterable[Record | int]
        """
        ...
