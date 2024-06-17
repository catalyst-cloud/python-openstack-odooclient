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

from typing import List, Literal

from typing_extensions import Annotated

from . import record_base, record_manager_name_base


class SupportSubscriptionType(record_base.RecordBase):
    billing_type: Literal["paid", "complimentary"]
    """The type of support subscription."""

    name: str
    """The name of the support subscription type."""

    product_id: Annotated[
        int,
        record_base.ModelRef("product", product_module.Product),
    ]
    """The ID for the product to use to invoice
    the support subscription.
    """

    product_name: Annotated[
        str,
        record_base.ModelRef("product", product_module.Product),
    ]
    """The name of the product to use to invoice
    the support subscription.
    """

    product: Annotated[
        product_module.Product,
        record_base.ModelRef("product", product_module.Product),
    ]
    """The product to use to invoice
    the support subscription.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    usage_percent: float
    """Percentage of usage compared to price (0-100)."""

    support_subscription_ids: Annotated[
        List[int],
        record_base.ModelRef(
            "support_subscription",
            support_subscription_type.SupportSubscription,
        ),
    ]
    """A list of IDs for the support subscriptions of this type."""

    support_subscription: Annotated[
        List[support_subscription_type.SupportSubscription],
        record_base.ModelRef(
            "support_subscription",
            support_subscription_type.SupportSubscription,
        ),
    ]
    """The list of support subscriptions of this type.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    support_subscriptions: Annotated[
        List[support_subscription_type.SupportSubscription],
        record_base.ModelRef(
            "support_subscription",
            support_subscription_type.SupportSubscription,
        ),
    ]
    """An alias for ``support_subscription``."""


class SupportSubscriptionTypeManager(
    record_manager_name_base.NamedRecordManagerBase[SupportSubscriptionType],
):
    env_name = "openstack.support_subscription.type"
    record_class = SupportSubscriptionType


# NOTE(callumdickinson): Import here to avoid circular imports.
from . import (  # noqa: E402
    product as product_module,
    support_subscription as support_subscription_type,
)
