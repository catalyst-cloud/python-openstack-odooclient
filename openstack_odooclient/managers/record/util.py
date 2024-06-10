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
    TYPE_CHECKING,
    Literal,
    Type,
    TypeVar,
    Union,
    get_args as get_type_args,
    get_origin as get_type_origin,
)

if TYPE_CHECKING:
    from typing import Any, List, Mapping, Optional

T = TypeVar("T")


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


def decode_value(annotation: Type[T], value: Any) -> T:
    """Decode a raw Odoo JSON field value to its local client representation,
    based on the annotation defined in the record model.

    :param annotation: The annotation to use to decode the value
    :type annotation: Type[T]
    :param value: The value to decode
    :type value: Any
    :return: The decoded value
    :rtype: T
    """

    # Create a type tree, which peels back the annotation layers
    # to find the basic data type that is expected.
    type_tree: List[Type[Any]] = [annotation]
    while get_type_origin(type_tree[-1]) is not None:
        origin_type = get_type_origin(type_tree[-1])
        if origin_type is not None:
            type_tree.append(origin_type)

    # The basic data types that need special handling.
    if type_tree[-1] is date:
        return date.fromisoformat(value)  # type: ignore[return-value]
    elif type_tree[-1] is datetime:
        return datetime.fromisoformat(value)  # type: ignore[return-value]
    # When a list is expected, decode each value individually
    # and return the result as a new list with the same order.
    elif type_tree[-1] is list:
        return [  # type: ignore[return-value]
            decode_value(get_type_args(type_tree[-2])[0], v) for v in value
        ]
    # When a dict is expected, decode the key and the value of each
    # item separately, and combine the result into a new dict.
    elif type_tree[-1] is dict:
        key_type, value_type = get_type_args(type_tree[-2])
        return {  # type: ignore[return-value]
            decode_value(key_type, k): decode_value(value_type, v)
            for k, v in value.items()
        }
    # Basic case for handling specific union structures.
    # Not suitable for handling complicated union structures.
    # TODO(callumdickinson): Find a way to handle complicated
    # union structures more smartly.
    elif type_tree[-1] is Union:
        attr_union_types = get_type_args(type_tree[-2])
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
