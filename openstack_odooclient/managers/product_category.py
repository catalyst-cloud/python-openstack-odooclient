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

from typing import List, Literal, Optional, Union

from typing_extensions import Annotated

from . import record_base, record_manager_name_base, util


class ProductCategory(record_base.RecordBase):
    child_id: Annotated[List[int], util.ModelRef("child_id")]
    """A list of IDs for the child categories."""

    child_ids: Annotated[List[int], util.FieldAlias("child_id")]
    """An alias for ``child_id``."""

    children: Annotated[
        List[ProductCategory],
        util.ModelRef("child_id"),
    ]
    """The list of child categories.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    complete_name: str
    """The complete product category tree."""

    name: str
    """Name of the product category."""

    parent_id: Annotated[Optional[int], util.ModelRef("parent_id")]
    """The ID for the parent product category, if this category
    is the child of another category.
    """

    parent_name: Annotated[Optional[str], util.ModelRef("parent_id")]
    """The name of the parent product category, if this category
    is the child of another category.
    """

    parent: Annotated[Optional[ProductCategory], util.ModelRef("parent_id")]
    """The parent product category, if this category
    is the child of another category.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    parent_path: Union[str, Literal[False]]
    """The path of the parent product category, if there is a parent."""

    product_count: int
    """The number of products under this category."""


class ProductCategoryManager(
    record_manager_name_base.NamedRecordManagerBase[ProductCategory],
):
    env_name = "product.category"
    record_class = ProductCategory
