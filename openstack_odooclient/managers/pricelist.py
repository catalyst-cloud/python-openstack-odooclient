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
from typing import TYPE_CHECKING, Literal, Optional, Union

from . import product as product_module, record

if TYPE_CHECKING:
    from . import company as company_module, currency as currency_module


class Pricelist(record.RecordBase):
    active: bool
    """Whether or not the pricelist is active."""

    @property
    def company_id(self) -> Optional[int]:
        """The ID for the company for this pricelist, if set."""
        return self._get_ref_id("company_id", optional=True)

    @property
    def company_name(self) -> Optional[str]:
        """The name of the company for this pricelist, if set."""
        return self._get_ref_name("company_id", optional=True)

    @cached_property
    def company(self) -> Optional[company_module.Company]:
        """The company for this pricelist, if set.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.company_id
        return (
            self._client.companies.get(record_id)
            if record_id is not None
            else None
        )

    @property
    def currency_id(self) -> int:
        """The ID for the currency used in this pricelist."""
        return self._get_ref_id("currency_id")

    @property
    def currency_name(self) -> str:
        """The name of the currency used in this pricelist."""
        return self._get_ref_name("currency_id")

    @cached_property
    def currency(self) -> currency_module.Currency:
        """The currency used in this pricelist.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.currencies.get(self.currency_id)

    discount_policy: Literal["with_discount", "without_discount"]
    """Discount policy for the pricelist.

    Values:

    * ``with_discount`` - Discount included in the price
    * ``without_discount`` - Show public price & discount to the customer
    """

    display_name: str
    """The display name of the pricelist."""

    default_code: str
    """The unit of this product.

    Referred to as the "Default Code" in Odoo.
    """

    description: str
    """A short description of this product."""

    name: str
    """The name of this pricelist."""

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "company": "company_id",
        "currency": "currency_id",
    }

    def get_price(
        self,
        product: Union[int, product_module.Product],
        qty: float,
    ) -> float:
        """Get the price to charge for a given product and quantity.

        :param product: Product to get the price for (ID or object)
        :type product: int or Product
        :param qty: Quantity to charge for
        :type qty: float
        :return: Price to charge
        :rtype: float
        """
        return self._client.pricelists.get_price(
            pricelist=self,
            product=product,
            qty=qty,
        )


class PricelistManager(record.NamedRecordManagerBase[Pricelist]):
    env_name = "product.pricelist"
    record_class = Pricelist

    def get_price(
        self,
        pricelist: Union[int, Pricelist],
        product: Union[int, product_module.Product],
        qty: float,
    ) -> float:
        """Get the price to charge for a given product and quantity.

        :param pricelist: Pricelist to reference (ID or object)
        :type pricelist: int or Pricelist
        :param product: Product to get the price for (ID or object)
        :type product: int or Product
        :param qty: Quantity to charge for
        :type qty: float
        :return: Price to charge
        :rtype: float
        """
        pricelist_id = (
            pricelist.id if isinstance(pricelist, Pricelist) else pricelist
        )
        price = self._env.price_get(
            pricelist_id,
            (
                product.id
                if isinstance(product, product_module.Product)
                else product
            ),
            max(qty, 0),
        )[str(pricelist_id)]
        return price if qty >= 0 else -price
