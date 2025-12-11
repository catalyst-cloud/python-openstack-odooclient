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

from dataclasses import dataclass
from typing import Annotated, Any

from typing_extensions import (
    Self,
    get_args as get_type_args,
    get_origin as get_type_origin,
)


class AnnotationBase:
    @classmethod
    def get(cls, type_hint: Any) -> Self | None:
        """Return the annotation applied to the given type hint,
        if the type hint is annotated with this type of annotation.

        If multiple matching annotations are found, the last occurrence
        is returned.

        :param type_hint: The type hint to parse
        :type type_hint: Any
        :return: Applied annotation, or ``None`` if no annotation was found
        :rtype: Self | None
        """
        if get_type_origin(type_hint) is not Annotated:
            return None
        matching_annotation: Self | None = None
        for annotation in get_type_args(type_hint)[1:]:
            if isinstance(annotation, cls):
                matching_annotation = annotation
        return matching_annotation

    @classmethod
    def is_annotated(cls, type_hint: Any) -> bool:
        """Checks whether or not the given type hint is annotated
        with an annotation of this type.

        :param type_hint: The type hint to parse
        :type type_hint: Any
        :return: ``True`` if annotated, otherwise ``False``
        :rtype: bool
        """
        return bool(cls.get(type_hint))


@dataclass(frozen=True)
class FieldAlias(AnnotationBase):
    """An annotation for defining field aliases
    (fields that point to other fields).

    Aliases are automatically resolved to the target field
    when searching or creating records, or referencing field values
    on record objects.

    >>> from typing import Annotated
    >>> from openstack_odooclient import FieldAlias, RecordBase
    >>> class CustomRecord(RecordBase["CustomRecordManager"]):
    ...     name: str
    ...     name_alias: Annotated[str, FieldAlias("name")]
    """

    field: str


@dataclass(frozen=True)
class ModelRef(AnnotationBase):
    """An annotation for defining model refs
    (fields that provide an interface to a model reference on a record).

    Model refs are used to express relationships between record types.
    The first argument is the name of the relationship field in Odoo,
    the second argument is the record class that type is represented by
    in the OpenStack Odoo Client library.

    >>> from typing import Annotated
    >>> from openstack_odooclient import ModelRef, RecordBase, User
    >>> class CustomRecord(RecordBase["CustomRecordManager"]):
    ...     user_id: Annotated[int, ModelRef("user_id", User)]
    ...     user_name: Annotated[str, ModelRef("user_id", User)]
    ...     user: Annotated[User, ModelRef("user_id", User)]

    For more information, check the OpenStack Odoo Client
    library documentation.
    """

    field: str
    record_class: Any
