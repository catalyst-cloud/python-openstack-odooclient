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

from typing import Annotated, Literal

from typing_extensions import Self

from ..base.record.base import RecordBase
from ..base.record.types import FieldAlias, ModelRef
from ..base.record_manager.base import RecordManagerBase


class ProductCategory(RecordBase["ProductCategoryManager"]):
    child_id: Annotated[list[int], ModelRef("child_id", Self)]
    """A list of IDs for the child categories."""

    child_ids: Annotated[list[int], FieldAlias("child_id")]
    """An alias for ``child_id``."""

    children: Annotated[list[Self], ModelRef("child_id", Self)]
    """The list of child categories.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    complete_name: str
    """The complete product category tree."""

    name: str
    """The name of the product category.

    Not guaranteed to be unique, even under the same parent category.
    """

    parent_id: Annotated[int | None, ModelRef("parent_id", Self)]
    """The ID for the parent product category, if this category
    is the child of another category.
    """

    parent_name: Annotated[str | None, ModelRef("parent_id", Self)]
    """The name of the parent product category, if this category
    is the child of another category.
    """

    parent: Annotated[Self | None, ModelRef("parent_id", Self)]
    """The parent product category, if this category
    is the child of another category.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    parent_path: str | Literal[False]
    """The path of the parent product category, if there is a parent."""

    product_count: int
    """The number of products under this category."""


class ProductCategoryManager(RecordManagerBase[ProductCategory]):
    env_name = "product.category"
    record_class = ProductCategory
