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

from datetime import date
from typing import Annotated, Literal

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase


class SupportSubscription(RecordBase["SupportSubscriptionManager"]):
    billing_type: Literal["paid", "complimentary"]
    """The method of billing for the support subscription.

    Values:

    * ``paid`` - Charge the subscription independently
    * ``complimentary`` - Bundled with a contract that includes the charge
    """

    end_date: date
    """The end date of the credit."""

    partner_id: Annotated[int | None, ModelRef("partner", Partner)]
    """The ID for the partner linked to this support subscription,
    if it is linked to a partner.

    Support subscriptions linked to a partner
    cover all projects the partner owns.
    """

    partner_name: Annotated[str | None, ModelRef("partner", Partner)]
    """The name of the partner linked to this support subscription,
    if it is linked to a partner.

    Support subscriptions linked to a partner
    cover all projects the partner owns.
    """

    partner: Annotated[Partner | None, ModelRef("partner", Partner)]
    """The partner linked to this support subscription,
    if it is linked to a partner.

    Support subscriptions linked to a partner
    cover all projects the partner owns.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    project_id: Annotated[int | None, ModelRef("project", Project)]
    """The ID of the project this support subscription is for,
    if it is linked to a specific project.
    """

    project_name: Annotated[str | None, ModelRef("project", Project)]
    """The name of the project this support subscription is for,
    if it is linked to a specific project.
    """

    project: Annotated[Project | None, ModelRef("project", Project)]
    """The project this support subscription is for,
    if it is linked to a specific project.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    start_date: date
    """The start date of the credit."""

    support_subscription_type_id: Annotated[
        int,
        ModelRef("support_subscription_type", SupportSubscriptionType),
    ]
    """The ID of the type of the support subscription."""

    support_subscription_type_name: Annotated[
        str,
        ModelRef("support_subscription_type", SupportSubscriptionType),
    ]
    """The name of the type of the support subscription."""

    support_subscription_type: Annotated[
        SupportSubscriptionType,
        ModelRef("support_subscription_type", SupportSubscriptionType),
    ]
    """The type of the support subscription.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class SupportSubscriptionManager(RecordManagerBase[SupportSubscription]):
    env_name = "openstack.support_subscription"
    record_class = SupportSubscription


# NOTE(callumdickinson): Import here to avoid circular imports.
from .partner import Partner  # noqa: E402
from .project import Project  # noqa: E402
from .support_subscription_type import SupportSubscriptionType  # noqa: E402
