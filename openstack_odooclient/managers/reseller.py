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
from typing import TYPE_CHECKING, Optional

from . import record

if TYPE_CHECKING:
    from . import partner as partner_module, project, reseller_tier


class Reseller(record.RecordBase):
    alternative_billing_url: Optional[str]
    """The URL to the cloud billing page for the reseller, if available."""

    alternative_support_url: Optional[str]
    """The URL to the cloud support centre for the reseller, if available."""

    @property
    def demo_project_id(self) -> Optional[int]:
        """The ID for the optional demo project belonging to the reseller."""
        return self._get_ref_id("project_demo", optional=True)

    @property
    def demo_project_name(self) -> Optional[str]:
        """The name of the optional demo project belonging to the reseller."""
        return self._get_ref_name("project_demo", optional=True)

    @cached_property
    def demo_project(self) -> Optional[project.Project]:
        """An optional demo project belonging to the reseller.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.project_id
        return (
            self._client.projects.get(record_id)
            if record_id is not None
            else None
        )

    hide_billing: bool
    """Whether or not the billing URL should be hidden."""

    hide_support: bool
    """Whether or not the support URL should be hidden."""

    name: str
    """The automatically generated reseller name.

    This is set to the reseller partner's name.
    """

    @property
    def partner_id(self) -> int:
        """The ID for the reseller partner."""
        return self._get_ref_id("partner")

    @property
    def partner_name(self) -> str:
        """The name of the reseller partner."""
        return self._get_ref_name("partner")

    @cached_property
    def partner(self) -> partner_module.Partner:
        """The reseller partner.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.partners.get(self.partner_id)

    @property
    def tier_id(self) -> int:
        """The ID for the tier this reseller is under."""
        return self._get_ref_id("tier")

    @property
    def tier_name(self) -> str:
        """The name of the tier this reseller is under."""
        return self._get_ref_name("tier")

    @cached_property
    def tier(self) -> reseller_tier.ResellerTier:
        """The tier this reseller is under.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.reseller_tiers.get(self.tier_id)

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "demo_project_id": "demo_project",
        "partner_id": "partner",
        "tier_id": "tier",
    }


class ResellerManager(record.RecordManagerBase[Reseller]):
    env_name = "openstack.reseller"
    record_class = Reseller
