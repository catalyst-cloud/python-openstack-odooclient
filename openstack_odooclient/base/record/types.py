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
from functools import cached_property
from typing import Annotated, Any

from packaging.specifiers import SpecifierSet
from packaging.version import Version
from typing_extensions import (
    Self,
    get_args as get_type_args,
    get_origin as get_type_origin,
)


class AnnotationBase:
    @classmethod
    def get_all(cls, type_hint: Any) -> list[Self]:
        """Return all annotations of this type from the given type hint.

        :param type_hint: The type hint to parse
        :type type_hint: Any
        :return: All applied annotations of this type
        :rtype: list[Self]
        """
        if get_type_origin(type_hint) is not Annotated:
            return []
        return [
            annotation
            for annotation in get_type_args(type_hint)[1:]
            if isinstance(annotation, cls)
        ]

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
        annotations = cls.get_all(type_hint)
        return annotations[-1] if annotations else None

    @classmethod
    def is_annotated(cls, type_hint: Any) -> bool:
        """Checks whether or not the given type hint is annotated
        with an annotation of this type.

        :param type_hint: The type hint to parse
        :type type_hint: Any
        :return: ``True`` if annotated, otherwise ``False``
        :rtype: bool
        """
        return bool(cls.get_all(type_hint))


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


@dataclass(frozen=True)
class VersionMapping(AnnotationBase):
    """An annotation for defining version-specific names for a field.

    This annotation is used to transparently handle Odoo server version
    differences. Clients only need to reference the field name defined on the
    record object; the Python OpenStack Odoo Client library will transparently
    convert between the local and the correct remote field names, depending on
    the server's version.

    When defining the annotation, set the first argument to the version
    specifier that defines the set of versions to match, and set the second
    argument to the name of the field to use.

    >>> from typing import Annotated
    >>> from openstack_odooclient import RecordBase, User, VersionMapping
    >>> class CustomRecord(RecordBase["CustomRecordManager"]):
    ...     name: Annotated[str, VersionMapping("<18.0", "old_name")]

    For model refs,  the version mapping applies to the model ref field
    specified in the ``ModelRef`` annotation. The version mapping only needs
    to be defined on **one** of the defined model ref fields (the same version
    mapping will be used for all of them). It is recommended to add it to the
    field representing the record ID (or list of record IDs), as shown below.

    >>> from typing import Annotated
    >>> from openstack_odooclient import (
    ...     ModelRef,
    ...     RecordBase,
    ...     User,
    ...     VersionMapping,
    ... )
    >>> class CustomRecord(RecordBase["CustomRecordManager"]):
    ...     user_id: Annotated[
    ...         int,
    ...         ModelRef("user_id", User),
    ...         VersionMapping("<18.0", "old_user_id"),
    ...     ]
    ...     user_name: Annotated[str, ModelRef("user_id", User)]
    ...     user: Annotated[User, ModelRef("user_id", User)]

    Multiple version mappings can be defined for a single field.
    Version mappings are evaluated in order, and the first one that
    matches is used.

    >>> from typing import Annotated
    >>> from openstack_odooclient import RecordBase, User, VersionMapping
    >>> class CustomRecord(RecordBase["CustomRecordManager"]):
    ...     name: Annotated[
    ...         str,
    ...         VersionMapping("<14.0", "old_name1"),
    ...         VersionMapping(">=14.0,<18.0", "old_name2"),
    ...     ]

    For more information, check the OpenStack Odoo Client
    library documentation.
    """

    matching_versions: str
    name: str

    @cached_property
    def _specifier_set(self) -> SpecifierSet:
        return SpecifierSet(self.matching_versions)

    def matches(self, version: str | Version) -> bool:
        """Check whether or not the given Odoo version matches
        this version mapping.

        :param version: Odoo version
        :type version: str | Version
        :return: ``True`` if the version matches, otherwise ``False``
        :rtype: bool
        """
        return self._specifier_set.contains(version)

    @classmethod
    def get_field_name(
        cls,
        name: str,
        type_hint: Any,
        version: str | Version,
    ) -> str:
        """Return the correct field name to use for the given model field
        and Odoo version.

        If any version mapping annotations are defined on the field's
        type hint, they are evaluated against the given Odoo version.
        The field name defined on the first matching version mapping
        is used.

        If none of the given version mappings match, or there are no version
        mappings defined at all, the default field name is returned.

        :param name: Default field name
        :type name: str
        :param type_hint: Field type hint
        :type type_hint: Any
        :param version: Odoo version
        :type version: str | version
        :return: Field name to use
        :rtype: str
        """
        for annotation in cls.get_all(type_hint):
            if annotation.matches(version):
                return annotation.name
        return name
