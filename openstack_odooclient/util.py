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

from typing import TYPE_CHECKING, Any, Type, TypeGuard, TypeVar

if TYPE_CHECKING:
    from collections.abc import Mapping

# Same values as defined in odoo.tools.misc.
DEFAULT_SERVER_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_SERVER_TIME_FORMAT = "%H:%M:%S"
DEFAULT_SERVER_DATETIME_FORMAT = (
    f"{DEFAULT_SERVER_DATE_FORMAT} {DEFAULT_SERVER_TIME_FORMAT}"
)

T = TypeVar("T")


def get_mapped_field(
    field_mapping: Mapping[str | None, Mapping[str, str]],
    odoo_version: str,
    field: str,
) -> str:
    """Map a field name to its representative in the given field mapping,
    based on the given Odoo version.

    If a representative value is not found for the given Odoo version,
    check the ``None`` mapping for all Odoo versions.
    If none is found there either, return the field name as is.

    :param field_mapping: Field mapping structure
    :type field_mapping: Mapping[str | None, Mapping[str, str]]
    :param odoo_version: Odoo server version
    :type odoo_version: str
    :param field: Field name to map
    :type field: str
    :return: Mapped field name
    :rtype: str
    """

    try:
        return field_mapping[odoo_version][field]
    except KeyError:
        try:
            return field_mapping[None][field]
        except KeyError:
            return field


def is_subclass(
    type_obj: Type[Any],
    classes: Type[T] | tuple[Type[T], ...],
) -> TypeGuard[Type[T]]:
    """Check whether or not the given type is a subclass of
    any of the given classes (single class, or tuple of one or more classes).

    Identical to the built-in ``issubclass`` method (and uses it internally),
    but returns ``False`` instead of raising ``TypeError`` when the given type
    does not match.

    :param type_obj: Type object to check
    :type type_obj: Type[Any]
    :param classes: Classes to check the type object is a subclass of
    :type classes: Type[Any] | tuple[Type[Any]]
    :return: ``True`` if the type is a subclass of any of the given classes
    :rtype: bool
    """

    try:
        return issubclass(type_obj, classes)
    except TypeError:
        return False
