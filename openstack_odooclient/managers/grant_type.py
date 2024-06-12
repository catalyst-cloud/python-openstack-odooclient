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
from typing import TYPE_CHECKING, List

from . import record

if TYPE_CHECKING:
    from . import grant, product as product_module, product_category


class GrantType(record.RecordBase):
    @property
    def grant_ids(self) -> List[int]:
        """A list of IDs for the grants which are of this grant type."""
        return self._get_field("grants")

    @cached_property
    def grants(self) -> List[grant.Grant]:
        """A list of grants which are of this grant type.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.grants.list(self.grant_ids)

    name: str
    """Name of the Grant Type."""

    @property
    def only_for_product_ids(self) -> List[int]:
        """A list of IDs for the products this grant applies to.

        Mutually exclusive with ``only_for_product_category_ids``.
        If neither are specified, the grant applies to all products.
        """
        return self._get_field("only_for_products")

    @cached_property
    def only_for_products(self) -> List[product_module.Product]:
        """A list of products which this grant applies to.

        Mutually exclusive with ``only_for_product_categories``.
        If neither are specified, the grant applies to all products.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.products.list(self.only_for_product_ids)

    @property
    def only_for_product_category_ids(self) -> List[int]:
        """A list of IDs for the product categories this grant applies to.

        Mutually exclusive with ``only_for_product_ids``.
        If neither are specified, the grant applies to all product
        categories.
        """
        return self._get_field("only_for_product_categories")

    @cached_property
    def only_for_product_categories(
        self,
    ) -> List[product_category.ProductCategory]:
        """A list of product categories which this grant applies to.

        Mutually exclusive with ``only_for_products``.
        If neither are specified, the grant applies to all product
        categories.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.product_categories.list(self.only_for_product_ids)

    only_on_group_root: bool
    """When set to ``True``, this grant type is only allowed to be
    part of an invoice grouping if it is on the group root project.
    """

    @property
    def product_id(self) -> int:
        """The ID of the product to use when applying
        the grant to invoices.
        """
        return self._get_ref_id("product")

    @property
    def product_name(self) -> str:
        """The name of the product to use when applying
        the grant to invoices.
        """
        return self._get_ref_name("product")

    @cached_property
    def product(self) -> product_module.Product:
        """The product to use when applying the grant to invoices.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.products.get(self.product_id)

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "grant_ids": "grants",
        "only_for_product_ids": "only_for_products",
        "only_for_product_category_ids": "only_for_product_categories",
        "product_id": "product",
    }


class GrantTypeManager(record.NamedRecordManagerBase[GrantType]):
    env_name = "openstack.grant.type"
    record_class = GrantType
