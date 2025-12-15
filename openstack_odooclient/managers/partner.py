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

from typing_extensions import Self

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase


class Partner(RecordBase["PartnerManager"]):
    active: bool
    """Whether or not this partner is active (enabled)."""

    company_id: Annotated[int, ModelRef("company_id", Company)]
    """The ID for the company this partner is owned by."""

    company_name: Annotated[str, ModelRef("company_id", Company)]
    """The name of the company this partner is owned by."""

    company: Annotated[Company, ModelRef("company_id", Company)]
    """The company this partner is owned by.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    email: str
    """Main e-mail address for the partner."""

    name: str
    """Full name of the partner."""

    os_customer_group_id: Annotated[
        int | None,
        ModelRef("os_customer_group", CustomerGroup),
    ]
    """The ID for the customer group this partner is part of,
    if it is part of one.
    """

    os_customer_group_name: Annotated[
        str | None,
        ModelRef("os_customer_group", CustomerGroup),
    ]
    """The name of the customer group this partner is part of,
    if it is part of one.
    """

    os_customer_group: Annotated[
        CustomerGroup | None,
        ModelRef("os_customer_group", CustomerGroup),
    ]
    """The customer group this partner is part of,
    if it is part of one.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    os_project_ids: Annotated[list[int], ModelRef("os_projects", Project)]
    """A list of IDs for the OpenStack projects that
    belong to this partner.
    """

    os_projects: Annotated[list[Project], ModelRef("os_projects", Project)]
    """The OpenStack projects that belong to this partner.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    os_project_contact_ids: Annotated[
        list[int],
        ModelRef("os_project_contacts", ProjectContact),
    ]
    """A list of IDs for the project contacts that are associated
    with this partner.
    """

    os_project_contacts: Annotated[
        list[ProjectContact],
        ModelRef("os_project_contacts", ProjectContact),
    ]
    """The project contacts that are associated with this partner.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    os_referral_id: Annotated[
        int | None,
        ModelRef("os_referral", ReferralCode),
    ]
    """The ID for the referral code the partner used on sign-up,
    if one was used.
    """

    os_referral_name: Annotated[
        str | None,
        ModelRef("os_referral", ReferralCode),
    ]
    """The name of the referral code the partner used on sign-up,
    if one was used.
    """

    os_referral: Annotated[
        ReferralCode | None,
        ModelRef("os_referral", ReferralCode),
    ]
    """The referral code the partner used on sign-up, if one was used.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    os_referral_code_ids: Annotated[
        list[int],
        ModelRef("os_referral_codes", ReferralCode),
    ]
    """A list of IDs for the referral codes the partner has used."""

    os_referral_codes: Annotated[
        list[ReferralCode],
        ModelRef("os_referral_codes", ReferralCode),
    ]
    """The referral codes the partner has used.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    os_reseller_id: Annotated[
        int | None,
        ModelRef("os_reseller", Reseller),
    ]
    """The ID for the reseller for this partner, if this partner
    is billed through a reseller.
    """

    os_reseller_name: Annotated[
        str | None,
        ModelRef("os_reseller", Reseller),
    ]
    """The name of the reseller for this partner, if this partner
    is billed through a reseller.
    """

    os_reseller: Annotated[
        Reseller | None,
        ModelRef("os_reseller", Reseller),
    ]
    """The reseller for this partner, if this partner
    is billed through a reseller.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    os_trial_id: Annotated[int | None, ModelRef("os_trial", Trial)]
    """The ID for the sign-up trial for this partner,
    if signed up under a trial.
    """

    os_trial_name: Annotated[str | None, ModelRef("os_trial", Trial)]
    """The name of the sign-up trial for this partner,
    if signed up under a trial.
    """

    os_trial: Annotated[Trial | None, ModelRef("os_trial", Trial)]
    """The sign-up trial for this partner,
    if signed up under a trial.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    parent_id: Annotated[
        int | None,
        ModelRef("parent_id", Self),
    ]
    """The ID for the parent partner of this partner,
    if it has a parent.
    """

    parent_name: Annotated[
        str | None,
        ModelRef("parent_id", Self),
    ]
    """The name of the parent partner of this partner,
    if it has a parent.
    """

    parent: Annotated[Self | None, ModelRef("parent_id", Self)]
    """The parent partner of this partner,
    if it has a parent.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    property_product_pricelist_id: Annotated[
        int | None,
        ModelRef("property_product_pricelist", Pricelist),
    ]
    """The ID for the pricelist this partner uses, if explicitly set.

    If not set, the pricelist set for the customer group
    is used (and if that is not set, the global default
    pricelist is used).
    """

    property_product_pricelist_name: Annotated[
        str | None,
        ModelRef("property_product_pricelist", Pricelist),
    ]
    """The name of the pricelist this partner uses, if explicitly set.

    If not set, the pricelist set for the customer group
    is used (and if that is not set, the global default
    pricelist is used).
    """

    property_product_pricelist: Annotated[
        Pricelist | None,
        ModelRef("property_product_pricelist", Pricelist),
    ]
    """The pricelist this partner uses, if explicitly set.

    If not set, the pricelist set for the customer group
    is used (and if that is not set, the global default
    pricelist is used).

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    stripe_customer_id: str | Literal[False]
    """The Stripe customer ID for this partner, if one has been assigned."""

    user_id: Annotated[int | None, ModelRef("user_id", User)]
    """The ID of the internal user associated with this partner,
    if one is assigned.
    """

    user_name: Annotated[str | None, ModelRef("user_id", User)]
    """The name of the internal user associated with this partner,
    if one is assigned.
    """

    user: Annotated[User | None, ModelRef("user_id", User)]
    """The internal user associated with this partner,
    if one is assigned.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class PartnerManager(RecordManagerBase[Partner]):
    env_name = "res.partner"
    record_class = Partner


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .company import Company  # noqa: E402
from .customer_group import CustomerGroup  # noqa: E402
from .pricelist import Pricelist  # noqa: E402
from .project import Project  # noqa: E402
from .project_contact import ProjectContact  # noqa: E402
from .referral_code import ReferralCode  # noqa: E402
from .reseller import Reseller  # noqa: E402
from .trial import Trial  # noqa: E402
from .user import User  # noqa: E402
