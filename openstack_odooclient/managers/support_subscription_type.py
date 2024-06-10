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
from typing import TYPE_CHECKING, List, Literal

from . import record

if TYPE_CHECKING:
    from . import (
        product as product_module,
        support_subscription as support_subscription_type,
    )


class SupportSubscriptionType(record.RecordBase):
    billing_type: Literal["paid", "complimentary"]
    """The type of support subscription."""

    name: str
    """The name of the support subscription type."""

    @property
    def product_id(self) -> int:
        """The ID for the product to use to invoice
        the support subscription.
        """
        return self._get_ref_id("product")

    @property
    def product_name(self) -> str:
        """The name of the product to use to invoice
        the support subscription.
        """
        return self._get_ref_name("product")

    @cached_property
    def product(self) -> product_module.Product:
        """The product to use to invoice
        the support subscription.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.products.get(self.product_id)

    usage_percent: float
    """Percentage of usage compared to price (0-100)."""

    @property
    def support_subscription_ids(self) -> List[int]:
        """A list of IDs for the support subscriptions of this type."""
        return self._get_field("support_subscription")

    @cached_property
    def support_subscription(
        self,
    ) -> List[support_subscription_type.SupportSubscription]:
        """The list of support subscriptions of this type.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.support_subscriptions.list(
            self.support_subscription_ids,
        )

    @cached_property
    def support_subscriptions(
        self,
    ) -> List[support_subscription_type.SupportSubscription]:
        """An alias for ``support_subscription``."""
        return self.support_subscription

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "product": "product_id",
        "support_subscription_ids": "support_subscription",
        "support_subscriptions": "support_subscription",
    }


class SupportSubscriptionTypeManager(
    record.NamedRecordManagerBase[SupportSubscriptionType],
):
    env_name = "openstack.support_subscription.type"
    record_class = SupportSubscriptionType
