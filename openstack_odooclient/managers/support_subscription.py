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
from typing import Literal, Optional

from typing_extensions import Annotated

from . import record_base, record_manager_base


class SupportSubscription(record_base.RecordBase):
    billing_type: Literal["paid", "complimentary"]
    """The method of billing for the support subscription.

    Values:

    * ``paid`` - Charge the subscription independently
    * ``complimentary`` - Bundled with a contract that includes the charge
    """

    end_date: date
    """The end date of the credit."""

    partner_id: Annotated[
        Optional[int],
        record_base.ModelRef("partner", partner_module.Partner),
    ]
    """The ID for the partner linked to this support subscription,
    if it is linked to a partner.

    Support subscriptions linked to a partner
    cover all projects the partner owns.
    """

    partner_name: Annotated[
        Optional[str],
        record_base.ModelRef("partner", partner_module.Partner),
    ]
    """The name of thepartner linked to this support subscription,
    if it is linked to a partner.

    Support subscriptions linked to a partner
    cover all projects the partner owns.
    """

    partner: Annotated[
        Optional[partner_module.Partner],
        record_base.ModelRef("partner", partner_module.Partner),
    ]
    """The partner linked to this support subscription,
    if it is linked to a partner.

    Support subscriptions linked to a partner
    cover all projects the partner owns.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    project_id: Annotated[
        Optional[int],
        record_base.ModelRef("project", project_module.Project),
    ]
    """The ID of the project this support subscription is for,
    if it is linked to a specific project.
    """

    project_name: Annotated[
        Optional[str],
        record_base.ModelRef("project", project_module.Project),
    ]
    """The name of the project this support subscription is for,
    if it is linked to a specific project.
    """

    project: Annotated[
        Optional[project_module.Project],
        record_base.ModelRef("project", project_module.Project),
    ]
    """The project this support subscription is for,
    if it is linked to a specific project.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    start_date: date
    """The start date of the credit."""

    support_subscription_type_id: Annotated[
        int,
        record_base.ModelRef(
            "support_subscription_type",
            support_subscription_type_module.SupportSubscriptionType,
        ),
    ]
    """The ID of the type of the support subscription."""

    support_subscription_type_name: Annotated[
        str,
        record_base.ModelRef(
            "support_subscription_type",
            support_subscription_type_module.SupportSubscriptionType,
        ),
    ]
    """The name of the type of the support subscription."""

    support_subscription_type: Annotated[
        support_subscription_type_module.SupportSubscriptionType,
        record_base.ModelRef(
            "support_subscription_type",
            support_subscription_type_module.SupportSubscriptionType,
        ),
    ]
    """The type of the support subscription.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class SupportSubscriptionManager(
    record_manager_base.RecordManagerBase[SupportSubscription],
):
    env_name = "openstack.support_subscription"
    record_class = SupportSubscription


# NOTE(callumdickinson): Import here to avoid circular imports.
from . import (  # noqa: E402
    partner as partner_module,
    project as project_module,
    support_subscription_type as support_subscription_type_module,
)
