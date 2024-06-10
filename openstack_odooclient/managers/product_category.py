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
from typing import List, Literal, Optional, Union

from . import record


class ProductCategory(record.RecordBase):
    @property
    def child_ids(self) -> List[int]:
        """A list of IDs for the child categories."""
        return self._get_field("child_id")

    @cached_property
    def children(self) -> List[ProductCategory]:
        """The list of child categories.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.product_categories.list(self.child_ids)

    complete_name: str
    """The complete product category tree."""

    name: str
    """Name of the product category."""

    @property
    def parent_id(self) -> Optional[int]:
        """The ID for the parent product category, if this category
        is the child of another category.
        """
        return self._get_ref_id("parent_id", optional=True)

    @property
    def parent_name(self) -> Optional[str]:
        """The name of the parent product category, if this category
        is the child of another category.
        """
        return self._get_ref_name("parent_id", optional=True)

    @cached_property
    def parent(self) -> Optional[ProductCategory]:
        """The parent product category, if this category
        is the child of another category.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.parent_id
        return (
            self._client.product_categories.get(record_id)
            if record_id is not None
            else None
        )

    parent_path: Union[str, Literal[False]]
    """The path of the parent product category, if there is a parent."""

    product_count: int
    """The number of products under this category."""

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "child_ids": "child_id",
        "children": "child_id",
        "parent": "parent_id",
    }


class ProductCategoryManager(record.NamedRecordManagerBase[ProductCategory]):
    env_name = "product.category"
    record_class = ProductCategory
