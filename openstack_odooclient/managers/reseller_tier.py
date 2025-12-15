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

from typing import Annotated

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase
from ..mixins.named_record import NamedRecordManagerMixin, NamedRecordMixin


class ResellerTier(
    RecordBase["ResellerTierManager"],
    NamedRecordMixin["ResellerTierManager"],
):
    discount_percent: float
    """The maximum discount percentage for this reseller tier (0-100)."""

    discount_product_id: Annotated[
        int,
        ModelRef("discount_product", Product),
    ]
    """The ID of the discount product for the reseller tier."""

    discount_product_name: Annotated[
        str,
        ModelRef("discount_product", Product),
    ]
    """The name of the discount product for the reseller tier."""

    discount_product: Annotated[
        Product,
        ModelRef("discount_product", Product),
    ]
    """The discount product for the reseller tier.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    free_monthly_credit: float
    """The amount the reseller gets monthly in credit for demo projects."""

    free_monthly_credit_product_id: Annotated[
        int,
        ModelRef("free_monthly_credit_product", Product),
    ]
    """The ID of the product to use when adding the free monthly credit
    to demo project invoices.
    """

    free_monthly_credit_product_name: Annotated[
        str,
        ModelRef("free_monthly_credit_product", Product),
    ]
    """The name of the product to use when adding the free monthly credit
    to demo project invoices.
    """

    free_monthly_credit_product: Annotated[
        Product,
        ModelRef("free_monthly_credit_product", Product),
    ]
    """The product to use when adding the free monthly credit
    to demo project invoices.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    free_support_hours: int
    """The amount of free support hours the reseller is entitled to
    under this tier.
    """

    min_usage_threshold: float
    """The minimum required usage amount for the reseller tier."""


class ResellerTierManager(
    RecordManagerBase[ResellerTier],
    NamedRecordManagerMixin[ResellerTier],
):
    env_name = "openstack.reseller.tier"
    record_class = ResellerTier


# NOTE(callumdickinson): Import here to avoid circular imports.
from .product import Product  # noqa: E402
