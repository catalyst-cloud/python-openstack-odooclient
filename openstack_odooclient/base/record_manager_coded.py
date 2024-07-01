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

from typing import TYPE_CHECKING, overload

from .record_manager_with_unique_field import (
    Record,
    RecordManagerWithUniqueFieldBase,
)

if TYPE_CHECKING:
    from typing import (
        Any,
        Dict,
        Iterable,
        Literal,
        Optional,
        Union,
    )


class CodedRecordManagerBase(RecordManagerWithUniqueFieldBase[Record, str]):
    """A record manager base class for record types with a code field.

    This code field is reasonably expected to be unique, which allows
    methods for getting records by code to be defined.

    The record class should be type hinted with the field to use as the code,
    just like any other field.
    Configure the name of the code field on the manager class by defining
    the ``code_field`` attribute (set to ``code`` by default).
    """

    code_field: str = "code"
    """The field code to use when querying by code in
    the ``get_by_code`` method.
    """

    @overload
    def get_by_code(
        self,
        code: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> Optional[int]: ...

    @overload
    def get_by_code(
        self,
        code: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> Optional[int]: ...

    @overload
    def get_by_code(
        self,
        code: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_by_code(
        self,
        code: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_by_code(
        self,
        code: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> Optional[Dict[str, Any]]: ...

    @overload
    def get_by_code(
        self,
        code: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> Dict[str, Any]: ...

    @overload
    def get_by_code(
        self,
        code: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> Optional[Record]: ...

    @overload
    def get_by_code(
        self,
        code: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> Record: ...

    @overload
    def get_by_code(
        self,
        code: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> Optional[Union[Record, int, Dict[str, Any]]]: ...

    def get_by_code(
        self,
        code: str,
        fields: Optional[Iterable[str]] = None,
        as_id: bool = False,
        as_dict: bool = False,
        optional: bool = False,
    ) -> Optional[Union[Record, int, Dict[str, Any]]]:
        """Query a unique record by code.

        A number of parameters are available to configure the return type,
        and what happens when a result is not found.

        By default all fields available on the record model
        will be selected, but this can be filtered using the
        ``fields`` parameter.

        Use the ``as_id`` parameter to return the ID of the record,
        instead of the record object.

        Use the ``as_dict`` parameter to return the record as
        a ``dict`` object, instead of a record object.

        When ``optional`` is ``True``, ``None`` is returned if a record
        with the given code does not exist, instead of raising an error.

        :param code: The record code
        :type code: str
        :param as_id: Return a record ID, defaults to False
        :type as_id: bool, optional
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[str] or None, optional
        :param as_dict: Return the record as a dictionary, defaults to False
        :type as_dict: bool, optional
        :param optional: Return ``None`` if not found, defaults to False
        :type optional: bool, optional
        :raises MultipleRecordsFoundError: Multiple records with the same code
        :raises RecordNotFoundError: Record with the given code not found
        :return: Query result (or ``None`` if record not found and optional)
        :rtype: Optional[Union[Record, int, Dict[str, Any]]]
        """
        return self._get_by_unique_field(
            field=self.code_field,
            value=code,
            fields=fields,
            as_id=as_id,
            as_dict=as_dict,
            optional=optional,
        )
