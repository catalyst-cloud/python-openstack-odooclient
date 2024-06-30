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

import itertools

from typing import TYPE_CHECKING, Generic, TypeVar, overload

from ..exceptions import MultipleRecordsFoundError, RecordNotFoundError
from .record_manager import Record, RecordManagerBase

if TYPE_CHECKING:
    from typing import (
        Any,
        Dict,
        Iterable,
        Literal,
        Optional,
        Union,
    )

T = TypeVar("T")


class RecordManagerWithUniqueFieldBase(
    RecordManagerBase[Record],
    Generic[Record, T],
):
    """A generic record manager base class for defining a record class
    with a searchable unique field.

    In addition to the usual generic type arg, a second type arg
    should be provided when subclassing ``RecordManagerWithUniqueFieldBase``.
    This becomes the expected type of the searchable unique field.

    >>> from openstack_odooclient import (
    ...     RecordBase,
    ...     RecordManagerWithUniqueFieldBase,
    ... )
    >>> class CustomRecord(RecordBase["CustomRecordManager"]):
    ...     name: str
    >>> class CustomRecordManager(
    ...     RecordManagerWithUniqueFieldBase[CustomRecord, str],
    ... ):
    ...     env_name = "custom.record"
    ...     record_class = CustomRecord

    Once you have your manager class, you can define methods
    that use the provided ``_get_by_unique_field`` method to implement
    custom search functionality according to your needs.
    """

    @overload
    def _get_by_unique_field(
        self,
        field: str,
        value: T,
        *,
        filters: Optional[Iterable[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> Optional[int]: ...

    @overload
    def _get_by_unique_field(
        self,
        field: str,
        value: T,
        *,
        filters: Optional[Iterable[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> Optional[int]: ...

    @overload
    def _get_by_unique_field(
        self,
        field: str,
        value: T,
        *,
        filters: Optional[Iterable[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def _get_by_unique_field(
        self,
        field: str,
        value: T,
        *,
        filters: Optional[Iterable[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def _get_by_unique_field(
        self,
        field: str,
        value: T,
        *,
        filters: Optional[Iterable[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> Optional[Dict[str, Any]]: ...

    @overload
    def _get_by_unique_field(
        self,
        field: str,
        value: T,
        *,
        filters: Optional[Iterable[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> Dict[str, Any]: ...

    @overload
    def _get_by_unique_field(
        self,
        field: str,
        value: T,
        *,
        filters: Optional[Iterable[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> Optional[Record]: ...

    @overload
    def _get_by_unique_field(
        self,
        field: str,
        value: T,
        *,
        filters: Optional[Iterable[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> Record: ...

    @overload
    def _get_by_unique_field(
        self,
        field: str,
        value: T,
        *,
        filters: Optional[Iterable[Any]] = ...,
        fields: Optional[Iterable[str]] = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> Optional[Union[Record, int, Dict[str, Any]]]: ...

    def _get_by_unique_field(
        self,
        field: str,
        value: T,
        filters: Optional[Iterable[Any]] = None,
        fields: Optional[Iterable[str]] = None,
        as_id: bool = False,
        as_dict: bool = False,
        optional: bool = False,
    ) -> Optional[Union[Record, int, Dict[str, Any]]]:
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

        :param field: The unique field name to query by
        :type field: str
        :param value: The unique field value
        :type value: T
        :param filters: Optional additional filters to apply, defaults to None
        :type filters: Optional[Iterable[Any]], optional
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[str] or None, optional
        :param as_id: Return a record ID, defaults to False
        :type as_id: bool, optional
        :param as_dict: Return the record as a dictionary, defaults to False
        :type as_dict: bool, optional
        :param optional: Return ``None`` if not found, defaults to False
        :type optional: bool, optional
        :raises MultipleRecordsFoundError: Multiple records with the same name
        :raises RecordNotFoundError: Record with the given name not found
        :return: Query result (or ``None`` if record not found and optional)
        :rtype: Optional[Union[Record, int, Dict[str, Any]]]
        """
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
