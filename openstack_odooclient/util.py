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

from typing import Any, Type, TypeGuard, TypeVar

# Same values as defined in odoo.tools.misc.
DEFAULT_SERVER_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_SERVER_TIME_FORMAT = "%H:%M:%S"
DEFAULT_SERVER_DATETIME_FORMAT = (
    f"{DEFAULT_SERVER_DATE_FORMAT} {DEFAULT_SERVER_TIME_FORMAT}"
)

T = TypeVar("T")


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
