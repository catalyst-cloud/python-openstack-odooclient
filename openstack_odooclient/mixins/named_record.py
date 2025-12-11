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

from typing import TYPE_CHECKING, Any, Generic, Literal, overload

from ..base.record.base import RM, RecordProtocol
from ..base.record_manager.base import R, RecordManagerProtocol

if TYPE_CHECKING:
    from collections.abc import Iterable


class NamedRecordMixin(RecordProtocol[RM], Generic[RM]):
    """A record mixin for record types with a ``name`` field.

    Include this mixin to add the ``name`` field, with ``str`` type,
    to your custom record class. This allows the additional methods
    provided by ``NamedRecordManagerMixin`` to be used.
    """

    name: str
    """The unique name of the record."""


class NamedRecordManagerMixin(RecordManagerProtocol[R], Generic[R]):
    """A record manager mixin for record types with a ``name`` field.

    The ``name`` field is expected to be unique, which allows
    methods for getting records by name to be defined.

    The record class must either include the ``NamedRecordMixin`` mixin,
    or have its own ``name`` field defined with the ``str`` type.
    """

    @overload
    def get_by_name(
        self,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> int | None: ...

    @overload
    def get_by_name(
        self,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> int | None: ...

    @overload
    def get_by_name(
        self,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_by_name(
        self,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_by_name(
        self,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> dict[str, Any] | None: ...

    @overload
    def get_by_name(
        self,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> dict[str, Any]: ...

    @overload
    def get_by_name(
        self,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> R | None: ...

    @overload
    def get_by_name(
        self,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> R: ...

    @overload
    def get_by_name(
        self,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> R | int | dict[str, Any] | None: ...

    def get_by_name(
        self,
        name: str,
        fields: Iterable[str] | None = None,
        as_id: bool = False,
        as_dict: bool = False,
        optional: bool = False,
    ) -> R | int | dict[str, Any] | None:
        """Query a unique record by name.

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
        with the given name does not exist, instead of raising an error.

        :param name: The record name
        :type name: str
        :param as_id: Return a record ID, defaults to False
        :type as_id: bool, optional
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[str] | None, optional
        :param as_dict: Return the record as a dictionary, defaults to False
        :type as_dict: bool, optional
        :param optional: Return ``None`` if not found, defaults to False
        :type optional: bool, optional
        :raises MultipleRecordsFoundError: Multiple records with the same name
        :raises RecordNotFoundError: Record with the given name not found
        :return: Query result (or ``None`` if record not found and optional)
        :rtype: R | int | dict[str, Any] | None
        """
        return self.get_by_unique_field(
            field="name",
            value=name,
            fields=fields,
            as_id=as_id,
            as_dict=as_dict,
            optional=optional,
        )
