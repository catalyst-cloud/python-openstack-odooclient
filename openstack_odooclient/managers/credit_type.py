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
    from . import credit, product as product_module, product_category


class CreditType(record.RecordBase):
    @property
    def credit_ids(self) -> List[int]:
        """A list of IDs for the credits which are of this credit type."""
        return self._get_field("credits")

    @cached_property
    def credits(self) -> List[credit.Credit]:
        """A list of credits which are of this credit type.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.credits.list(self.credit_ids)

    name: str
    """Name of the Credit Type."""

    @property
    def only_for_product_ids(self) -> List[int]:
        """A list of IDs for the products this credit applies to.

        Mutually exclusive with ``only_for_product_category_ids``.
        If neither are specified, the credit applies to all products.
        """
        return self._get_field("only_for_products")

    @cached_property
    def only_for_products(self) -> List[product_module.Product]:
        """A list of products which this credit applies to.

        Mutually exclusive with ``only_for_product_categories``.
        If neither are specified, the credit applies to all products.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.products.list(self.only_for_product_ids)

    @property
    def only_for_product_category_ids(self) -> List[int]:
        """A list of IDs for the product categories this credit applies to.

        Mutually exclusive with ``only_for_product_ids``.
        If neither are specified, the credit applies to all product
        categories.
        """
        return self._get_field("only_for_product_categories")

    @cached_property
    def only_for_product_categories(
        self,
    ) -> List[product_category.ProductCategory]:
        """A list of product categories which this credit applies to.

        Mutually exclusive with ``only_for_products``.
        If neither are specified, the credit applies to all product
        categories.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.product_categories.list(self.only_for_product_ids)

    @property
    def product_id(self) -> int:
        """The ID of the product to use when applying
        the credit to invoices.
        """
        return self._get_ref_id("product")

    @property
    def product_name(self) -> str:
        """The name of the product to use when applying
        the credit to invoices.
        """
        return self._get_ref_name("product")

    @cached_property
    def product(self) -> product_module.Product:
        """The product to use when applying the credit to invoices.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.products.get(self.product_id)

    refundable: bool
    """Whether or not the credit is refundable."""

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "credit_ids": "credits",
        "only_for_product_ids": "only_for_products",
        "only_for_product_category_ids": "only_for_product_categories",
        "product_id": "product",
    }


class CreditTypeManager(record.NamedRecordManagerBase[CreditType]):
    env_name = "openstack.credit.type"
    record_class = CreditType
