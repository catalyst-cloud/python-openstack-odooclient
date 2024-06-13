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

from dataclasses import dataclass
from datetime import date, datetime
from typing import (
    TYPE_CHECKING,
    Literal,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from typing_extensions import (
    get_args as get_type_args,
    get_origin as get_type_origin,
)

# from . import base

if TYPE_CHECKING:
    from typing import Any, List, Mapping, Optional

T = TypeVar("T")


@dataclass(frozen=True)
class FieldAlias:
    """An annotation for alias attributes to define the Odoo field name
    the attribute is an alias for.
    """

    field: str


@dataclass(frozen=True)
class ModelRef:
    """An annotation for attributes that decode an Odoo model reference,
    to define the Odoo field name to be decoded.
    """

    field: str


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


def get_type_tree(type_hint: Type[Any]) -> Tuple[Type[Any], ...]:
    """Generate the type tree for the given annotation.

    This function peels back the annotation layers
    and generates a list containing the type hint encapsulations,
    from the outermost layer to the innermost layer.

    The expected basic data type will end up at the end of the list.

    If the annotation is a union of possible values, the final two elements
    will be as follows:

    >>> from typing import Literal, Union
    >>> from openstack_odooclient.managers.record.util import get_type_tree
    >>> get_type_tree(Union[str, Literal[False]])
    (typing.Union[str, typing.Literal[False]], typing.Union)

    ``Union[T, ...]`` can be evaluated to get the candidate types using
    ``typing.get_args``. This includes ``Optional[T]``,
    which is syntantic sugar for ``Union[T, type(None)]``.

    >>> from typing import Literal, Union, get_args
    >>> get_args(Union[str, Literal[False]])
    (<class 'str'>, typing.Literal[False])

    Similarly, if the data type is a generic type such as ``list``
    or ``dict`` that take type arguments, the final two elements will be
    as follows.

    >>> from typing import Dict
    >>> from openstack_odooclient.managers.record.util import get_type_tree
    >>> get_type_tree(Dict[int, str])
    (typing.Dict[str, int], <class 'dict'>)

    The generic types can be retrieved using ``typing.get_args``.

    >>> from typing import Dict, get_args
    >>> get_args(Dict[int, str])
    (<class 'int'>, <class 'str'>)

    :param type_hint: Type hint to parse
    :type type_hint: Type[Any]
    :return: Type hint tree
    :rtype: Tuple[Type[Any]]
    """

    type_tree: List[Type[Any]] = [type_hint]

    while get_type_origin(type_tree[-1]) is not None:
        origin_type = get_type_origin(type_tree[-1])
        if origin_type is not None:
            type_tree.append(origin_type)

    return tuple(type_tree)


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

    type_tree = get_type_tree(type_hint)

    # The basic data types that need special handling.
    if type_tree[-1] is date:
        return date.fromisoformat(value)  # type: ignore[return-value]

    if type_tree[-1] is datetime:
        return datetime.fromisoformat(value)  # type: ignore[return-value]

    # When a list is expected, decode each value individually
    # and return the result as a new list with the same order.
    if type_tree[-1] is list:
        return [  # type: ignore[return-value]
            decode_value(get_type_args(type_tree[-2])[0], v) for v in value
        ]

    # When a dict is expected, decode the key and the value of each
    # item separately, and combine the result into a new dict.
    if type_tree[-1] is dict:
        key_type, value_type = get_type_args(type_tree[-2])
        return {  # type: ignore[return-value]
            decode_value(key_type, k): decode_value(value_type, v)
            for k, v in value.items()
        }

    # Basic case for handling specific union structures.
    # Not suitable for handling complicated union structures.
    # TODO(callumdickinson): Find a way to handle complicated
    # union structures more smartly.
    if type_tree[-1] is Union:
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


# def encode_create_value(annotation: Type[Any], value: Any) -> Any:
#     """_summary_

#     :param value: _description_
#     :type value: Any
#     :return: _description_
#     :rtype: Any
#     """

#     type_tree = get_type_tree(annotation)
#     value_type = type_tree[-1]

#     if issubclass(value_type, base.RecordBase):
#         if isinstance(value, base.RecordBase):
#             return value.id
#         elif isinstance(value, dict):
#             return {
#                 value_type._resolve_alias(k): encode_create_value(
#                     value_type.__annotations__[k],
#                     v,
#                 )
#                 for k, v in value.items()
#             }
#     if (
#         value_type in (date, datetime)
#         and isinstance(value, (date, datetime))
#     ):
#         return value.isoformat()
#     if (
#         value_type is list
#         and isinstance(value, (list, set, tuple))
#     ):
#         v_type = get_type_args(type_tree[-2])[0]
#         return [encode_create_value(v_type, v) for v in value]

#     return value
