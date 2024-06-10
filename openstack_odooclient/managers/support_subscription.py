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
from functools import cached_property
from typing import TYPE_CHECKING, Literal, Optional

from . import record

if TYPE_CHECKING:
    from . import (
        partner as partner_module,
        project as project_module,
        support_subscription_type as support_subscription_type_module,
    )


class SupportSubscription(record.RecordBase):
    billing_type: Literal["paid", "complimentary"]
    """The method of billing for the support subscription.

    Values:

    * ``paid`` - Charge the subscription independently
    * ``complimentary`` - Bundled with a contract that includes the charge
    """

    end_date: date
    """The end date of the credit."""

    @property
    def partner_id(self) -> Optional[int]:
        """The ID for the partner linked to this support subscription,
        if it is linked to a partner.

        Support subscriptions linked to a partner
        cover all projects the partner owns.
        """
        return self._get_ref_id("partner", optional=True)

    @property
    def partner_name(self) -> Optional[str]:
        """The name of thepartner linked to this support subscription,
        if it is linked to a partner.

        Support subscriptions linked to a partner
        cover all projects the partner owns.
        """
        return self._get_ref_name("partner", optional=True)

    @cached_property
    def partner(self) -> Optional[partner_module.Partner]:
        """The partner linked to this support subscription,
        if it is linked to a partner.

        Support subscriptions linked to a partner
        cover all projects the partner owns.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.partner_id
        return (
            self._client.partners.get(record_id)
            if record_id is not None
            else None
        )

    @property
    def project_id(self) -> Optional[int]:
        """The ID of the project this support subscription is for,
        if it is linked to a specific project.
        """
        return self._get_ref_id("project", optional=True)

    @property
    def project_name(self) -> Optional[str]:
        """The name of the project this support subscription is for,
        if it is linked to a specific project.
        """
        return self._get_ref_name("project", optional=True)

    @cached_property
    def project(self) -> Optional[project_module.Project]:
        """The project this support subscription is for,
        if it is linked to a specific project.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.project_id
        return (
            self._client.projects.get(record_id)
            if record_id is not None
            else None
        )

    start_date: date
    """The start date of the credit."""

    @property
    def support_subscription_type_id(self) -> int:
        """The ID of the type of the support subscription."""
        return self._get_ref_id("support_subscription_type")

    @property
    def support_subscription_type_name(self) -> str:
        """The name of the type of the support subscription."""
        return self._get_ref_name("support_subscription_type")

    @cached_property
    def support_subscription_type(
        self,
    ) -> support_subscription_type_module.SupportSubscriptionType:
        """The type of the support subscription.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.support_subscription_types.get(
            self.support_subscription_type_id,
        )

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "partner_id": "partner",
        "project_id": "project",
        "support_subscription_type_id": "support_subscription_type",
    }


class SupportSubscriptionManager(
    record.RecordManagerBase[SupportSubscription],
):
    env_name = "openstack.support_subscription"
    record_class = SupportSubscription
