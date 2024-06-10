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

from functools import cached_property
from typing import TYPE_CHECKING, List, Literal, Optional, Union

from . import record

if TYPE_CHECKING:
    from . import partner


class PartnerCategory(record.RecordBase):
    active: bool
    """Whether or not the partner category is active."""

    @property
    def child_ids(self) -> List[int]:
        """A list of IDs for the child categories."""
        return self._get_field("child_id")

    @cached_property
    def children(self) -> List[PartnerCategory]:
        """The list of child categories.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.partner_categories.list(self.child_ids)

    color: int
    """Colour index for the partner category."""

    @property
    def colour(self) -> int:
        """Alias for ``color``."""
        return self.color

    name: str
    """Partner category name."""

    @property
    def parent_id(self) -> Optional[int]:
        """The ID for the parent partner category, if this category
        is the child of another category.
        """
        return self._get_ref_id("parent_id", optional=True)

    @property
    def parent_name(self) -> Optional[str]:
        """The name of the parent partner category, if this category
        is the child of another category.
        """
        return self._get_ref_name("parent_id", optional=True)

    @cached_property
    def parent(self) -> Optional[PartnerCategory]:
        """The parent partner category, if this category
        is the child of another category.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.parent_id
        return (
            self._client.partner_categories.get(record_id)
            if record_id is not None
            else None
        )

    parent_path: Union[str, Literal[False]]
    """The path of the parent partner category, if there is a parent."""

    @property
    def partner_ids(self) -> List[int]:
        """A list of IDs for the partners in this category."""
        return self._get_field("partner_id")

    @cached_property
    def partners(self) -> List[partner.Partner]:
        """The list of partners in this category.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.partners.list(self.partner_ids)

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "child_ids": "child_id",
        "children": "child_id",
        "parent": "parent_id",
        "partner_ids": "partner_id",
        "partners": "partner_id",
    }


class PartnerCategoryManager(record.NamedRecordManagerBase[PartnerCategory]):
    env_name = "res.partner.category"
    record_class = PartnerCategory
