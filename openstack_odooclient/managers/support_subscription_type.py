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

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase
from ..mixins.named_record import NamedRecordManagerMixin, NamedRecordMixin


class SupportSubscriptionType(
    RecordBase["SupportSubscriptionTypeManager"],
    NamedRecordMixin["SupportSubscriptionTypeManager"],
):
    billing_type: Literal["paid", "complimentary"]
    """The type of support subscription."""

    product_id: Annotated[int, ModelRef("product", Product)]
    """The ID for the product to use to invoice
    the support subscription.
    """

    product_name: Annotated[str, ModelRef("product", Product)]
    """The name of the product to use to invoice
    the support subscription.
    """

    product: Annotated[Product, ModelRef("product", Product)]
    """The product to use to invoice
    the support subscription.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    usage_percent: float
    """Percentage of usage compared to price (0-100)."""

    support_subscription_ids: Annotated[
        list[int],
        ModelRef("support_subscription", SupportSubscription),
    ]
    """A list of IDs for the support subscriptions of this type."""

    support_subscription: Annotated[
        list[SupportSubscription],
        ModelRef("support_subscription", SupportSubscription),
    ]
    """The list of support subscriptions of this type.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    support_subscriptions: Annotated[
        list[SupportSubscription],
        ModelRef("support_subscription", SupportSubscription),
    ]
    """An alias for ``support_subscription``."""


class SupportSubscriptionTypeManager(
    RecordManagerBase[SupportSubscriptionType],
    NamedRecordManagerMixin[SupportSubscriptionType],
):
    env_name = "openstack.support_subscription.type"
    record_class = SupportSubscriptionType


# NOTE(callumdickinson): Import here to avoid circular imports.
from .product import Product  # noqa: E402
from .support_subscription import SupportSubscription  # noqa: E402
