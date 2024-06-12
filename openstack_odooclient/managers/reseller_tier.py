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
from typing import TYPE_CHECKING

from . import record

if TYPE_CHECKING:
    from . import product


class ResellerTier(record.RecordBase):
    discount_percent: float
    """The maximum discount percentage for this reseller tier (0-100)."""

    @property
    def discount_product_id(self) -> int:
        """The ID of the discount product for the reseller tier."""
        return self._get_ref_id("discount_product")

    @property
    def discount_product_name(self) -> str:
        """The name of the discount product for the reseller tier."""
        return self._get_ref_name("discount_product")

    @cached_property
    def discount_product(self) -> product.Product:
        """The discount product for the reseller tier.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.products.get(self.discount_product_id)

    free_monthly_credit: float
    """The amount the reseller gets monthly in credit for demo projects."""

    @property
    def free_monthly_credit_product_id(self) -> int:
        """The ID of the product to use when adding the free monthly credit
        to demo project invoices.
        """
        return self._get_ref_id("free_monthly_credit_product")

    @property
    def free_monthly_credit_product_name(self) -> str:
        """The name of the product to use when adding the free monthly credit
        to demo project invoices.
        """
        return self._get_ref_name("free_monthly_credit_product")

    @cached_property
    def free_monthly_credit_product(self) -> product.Product:
        """The product to use when adding the free monthly credit
        to demo project invoices.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.products.get(self.free_monthly_credit_product_id)

    free_support_hours: int
    """The amount of free support hours the reseller is entitled to
    under this tier.
    """

    name: str
    """Reseller tier name."""

    min_usage_threshold: float
    """The minimum required usage amount for the reseller tier."""

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "discount_product_id": "discount_product",
        "free_monthly_credit_product_id": "free_monthly_credit_product",
    }


class ResellerTierManager(record.NamedRecordManagerBase[ResellerTier]):
    env_name = "openstack.reseller.tier"
    record_class = ResellerTier
