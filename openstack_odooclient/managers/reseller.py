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

from typing import Optional

from typing_extensions import Annotated

from . import record_base, record_manager_base


class Reseller(record_base.RecordBase):
    alternative_billing_url: Optional[str]
    """The URL to the cloud billing page for the reseller, if available."""

    alternative_support_url: Optional[str]
    """The URL to the cloud support centre for the reseller, if available."""

    demo_project_id: Annotated[
        Optional[int],
        record_base.ModelRef("demo_project", project.Project),
    ]
    """The ID for the optional demo project belonging to the reseller."""

    demo_project_name: Annotated[
        Optional[str],
        record_base.ModelRef("demo_project", project.Project),
    ]
    """The name of the optional demo project belonging to the reseller."""

    demo_project: Annotated[
        Optional[project.Project],
        record_base.ModelRef("demo_project", project.Project),
    ]
    """An optional demo project belonging to the reseller.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    hide_billing: bool
    """Whether or not the billing URL should be hidden."""

    hide_support: bool
    """Whether or not the support URL should be hidden."""

    name: str
    """The automatically generated reseller name.

    This is set to the reseller partner's name.
    """

    partner_id: Annotated[
        int,
        record_base.ModelRef("partner", partner_module.Partner),
    ]
    """The ID for the reseller partner."""

    partner_name: Annotated[
        str,
        record_base.ModelRef("partner", partner_module.Partner),
    ]
    """The name of the reseller partner."""

    partner: Annotated[
        partner_module.Partner,
        record_base.ModelRef("partner", partner_module.Partner),
    ]
    """The reseller partner.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    tier_id: Annotated[
        int,
        record_base.ModelRef("tier", reseller_tier.ResellerTier),
    ]
    """The ID for the tier this reseller is under."""

    tier_name: Annotated[
        str,
        record_base.ModelRef("tier", reseller_tier.ResellerTier),
    ]
    """The name of the tier this reseller is under."""

    tier: Annotated[
        reseller_tier.ResellerTier,
        record_base.ModelRef("tier", reseller_tier.ResellerTier),
    ]
    """The tier this reseller is under.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class ResellerManager(record_manager_base.RecordManagerBase[Reseller]):
    env_name = "openstack.reseller"
    record_class = Reseller


# NOTE(callumdickinson): Import here to avoid circular imports.
from . import partner as partner_module, project, reseller_tier  # noqa: E402
