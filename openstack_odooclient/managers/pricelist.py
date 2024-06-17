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

from typing import Literal, Optional, Union

from typing_extensions import Annotated

from ..base.record import ModelRef, RecordBase
from ..base.record_manager_named import NamedRecordManagerBase
from .product import Product


class Pricelist(RecordBase):
    active: bool
    """Whether or not the pricelist is active."""

    company_id: Annotated[Optional[int], ModelRef("company_id", Company)]
    """The ID for the company for this pricelist, if set."""

    company_name: Annotated[Optional[str], ModelRef("company_id", Company)]
    """The name of the company for this pricelist, if set."""

    company: Annotated[Optional[Company], ModelRef("company_id", Company)]
    """The company for this pricelist, if set.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    currency_id: Annotated[int, ModelRef("currency_id", Currency)]
    """The ID for the currency used in this pricelist."""

    currency_name: Annotated[str, ModelRef("currency_id", Currency)]
    """The name of the currency used in this pricelist."""

    currency: Annotated[Currency, ModelRef("currency_id", Currency)]
    """The currency used in this pricelist.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    discount_policy: Literal["with_discount", "without_discount"]
    """Discount policy for the pricelist.

    Values:

    * ``with_discount`` - Discount included in the price
    * ``without_discount`` - Show public price & discount to the customer
    """

    name: str
    """The name of this pricelist."""

    def get_price(self, product: Union[int, Product], qty: float) -> float:
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


class PricelistManager(NamedRecordManagerBase[Pricelist]):
    env_name = "product.pricelist"
    record_class = Pricelist

    def get_price(
        self,
        pricelist: Union[int, Pricelist],
        product: Union[int, Product],
        qty: float,
    ) -> float:
        """Get the price to charge for a given pricelist, product
        and quantity.

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
            (product.id if isinstance(product, Product) else product),
            max(qty, 0),
        )[str(pricelist_id)]
        return price if qty >= 0 else -price


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .company import Company  # noqa: E402
from .currency import Currency  # noqa: E402
