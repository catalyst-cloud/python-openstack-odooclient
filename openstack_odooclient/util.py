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
from typing import (
    Any,
    Literal,
    Mapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from typing_extensions import (
    get_args as get_type_args,
    get_origin as get_type_origin,
)

T = TypeVar("T")

# Same values as defined in odoo.tools.misc.
DEFAULT_SERVER_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_SERVER_TIME_FORMAT = "%H:%M:%S"
DEFAULT_SERVER_DATETIME_FORMAT = (
    f"{DEFAULT_SERVER_DATE_FORMAT} {DEFAULT_SERVER_TIME_FORMAT}"
)


def get_mapped_field(
    field_mapping: Mapping[Optional[str], Mapping[str, str]],
    odoo_version: str,
    field: str,
) -> str:
    """Map a field name to its representative in the given field mapping,
    based on the given Odoo version.

    If a representative value is not found for the given Odoo version,
    check the ``None`` mapping for all Odoo versions.
    If none is found there either, return the field name as is.

    :param field_mapping: Field mapping structure
    :type field_mapping: Mapping[Optional[str], Mapping[str, str]]
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
    classes: Union[Type[Any], Tuple[Type[Any]]],
) -> bool:
    """Check whether or not the given type is a subclass of
    any of the given classes (single class, or tuple of one or more classes).

    Identical to the built-in ``issubclass`` method (and uses it internally),
    but returns ``False`` instead of raising ``TypeError`` when the given type
    does not match.

    :param type_obj: Type object to check
    :type type_obj: Type[Any]
    :param classes: Classes to check the type object is a subclass of
    :type classes: Union[Type[Any], Tuple[Type[Any]]]
    :return: ``True`` if the type is a subclass of any of the given classes
    :rtype: bool
    """

    try:
        return issubclass(type_obj, classes)
    except TypeError:
        return False


def decode_value(type_hint: Type[T], value: Any) -> T:
    """Decode a raw Odoo JSON field value to its local representation,
    based on the given type hint from the record class.

    :param type_hint: The type hint to use to decode the value
    :type type_hint: Type[T]
    :param value: The value to decode
    :type value: Any
    :return: The decoded value
    :rtype: T
    """

    value_type = get_type_origin(type_hint) or type_hint

    # The basic data types that need special handling.
    if value_type is date:
        return date.fromisoformat(value)  # type: ignore[return-value]

    if value_type is datetime:
        return datetime.fromisoformat(value)  # type: ignore[return-value]

    # When a list is expected, decode each value individually
    # and return the result as a new list with the same order.
    if value_type is list:
        return [  # type: ignore[return-value]
            decode_value(get_type_args(type_hint)[0], v) for v in value
        ]

    # When a dict is expected, decode the key and the value of each
    # item separately, and combine the result into a new dict.
    if value_type is dict:
        key_type, value_type = get_type_args(type_hint)
        return {  # type: ignore[return-value]
            decode_value(key_type, k): decode_value(value_type, v)
            for k, v in value.items()
        }

    # Basic case for handling specific union structures.
    # Not suitable for handling complicated union structures.
    # TODO(callumdickinson): Find a way to handle complicated
    # union structures more smartly.
    if value_type is Union:
        attr_union_types = get_type_args(type_hint)
        if len(attr_union_types) == 2:  # noqa: PLR2004
            # Optional[T]
            if type(None) in attr_union_types and value is not None:
                return decode_value(
                    next(t for t in attr_union_types if t is not type(None)),
                    value,
                )
            # Union[T, Literal[False]]
            if Literal[False] in attr_union_types and value is not False:
                return decode_value(
                    next(
                        (
                            t
                            for t in attr_union_types
                            if t is not Literal[False]
                        ),
                    ),
                    value,
                )

    # Base case: Return the passed value unmodified.
    return value
