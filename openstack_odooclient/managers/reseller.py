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


class Reseller(RecordBase["ResellerManager"]):
    alternative_billing_url: str | None
    """The URL to the cloud billing page for the reseller, if available."""

    alternative_support_url: str | None
    """The URL to the cloud support centre for the reseller, if available."""

    demo_project_id: Annotated[
        int | None,
        ModelRef("demo_project", Project),
    ]
    """The ID for the optional demo project belonging to the reseller."""

    demo_project_name: Annotated[
        str | None,
        ModelRef("demo_project", Project),
    ]
    """The name of the optional demo project belonging to the reseller."""

    demo_project: Annotated[
        Project | None,
        ModelRef("demo_project", Project),
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

    partner_id: Annotated[int, ModelRef("partner", Partner)]
    """The ID for the reseller partner."""

    partner_name: Annotated[str, ModelRef("partner", Partner)]
    """The name of the reseller partner."""

    partner: Annotated[Partner, ModelRef("partner", Partner)]
    """The reseller partner.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    tier_id: Annotated[int, ModelRef("tier", ResellerTier)]
    """The ID for the tier this reseller is under."""

    tier_name: Annotated[str, ModelRef("tier", ResellerTier)]
    """The name of the tier this reseller is under."""

    tier: Annotated[ResellerTier, ModelRef("tier", ResellerTier)]
    """The tier this reseller is under.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class ResellerManager(RecordManagerBase[Reseller]):
    env_name = "openstack.reseller"
    record_class = Reseller


# NOTE(callumdickinson): Import here to avoid circular imports.
from .partner import Partner  # noqa: E402
from .project import Project  # noqa: E402
from .reseller_tier import ResellerTier  # noqa: E402
