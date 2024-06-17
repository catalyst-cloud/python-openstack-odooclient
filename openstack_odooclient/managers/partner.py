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

from typing import List, Literal, Optional, Union

from typing_extensions import Annotated, Self

from . import (
    pricelist,
    project,
    record_base,
    record_manager_base,
)


class Partner(record_base.RecordBase):
    active: bool
    """Whether or not this partner is active (enabled)."""

    company_id: Annotated[
        int,
        record_base.ModelRef("company_id", company_module.Company),
    ]
    """The ID for the company this partner is owned by."""

    company_name: Annotated[
        str,
        record_base.ModelRef("company_id", company_module.Company),
    ]
    """The name of the company this partner is owned by."""

    company: Annotated[
        company_module.Company,
        record_base.ModelRef("company_id", company_module.Company),
    ]
    """The company this partner is owned by.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    email: str
    """Main e-mail address for the partner."""

    name: str
    """Full name of the partner."""

    os_customer_group_id: Annotated[
        Optional[int],
        record_base.ModelRef(
            "os_customer_group",
            customer_group.CustomerGroup,
        ),
    ]
    """The ID for the customer group this partner is part of,
    if it is part of one.
    """

    os_customer_group_name: Annotated[
        Optional[str],
        record_base.ModelRef(
            "os_customer_group",
            customer_group.CustomerGroup,
        ),
    ]
    """The name of the customer group this partner is part of,
    if it is part of one.
    """

    os_customer_group: Annotated[
        Optional[customer_group.CustomerGroup],
        record_base.ModelRef(
            "os_customer_group",
            customer_group.CustomerGroup,
        ),
    ]
    """The customer group this partner is part of,
    if it is part of one.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    os_project_ids: Annotated[
        List[int],
        record_base.ModelRef("os_projects", project.Project),
    ]
    """A list of IDs for the OpenStack projects that
    belong to this partner.
    """

    os_projects: Annotated[
        List[project.Project],
        record_base.ModelRef("os_projects", project.Project),
    ]
    """The OpenStack projects that belong to this partner.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    os_project_contact_ids: Annotated[
        List[int],
        record_base.ModelRef(
            "os_project_contacts",
            project_contact.ProjectContact,
        ),
    ]
    """A list of IDs for the project contacts that are associated
    with this partner.
    """

    os_project_contacts: Annotated[
        List[project_contact.ProjectContact],
        record_base.ModelRef(
            "os_project_contacts",
            project_contact.ProjectContact,
        ),
    ]
    """The project contacts that are associated with this partner.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    os_referral_id: Annotated[
        Optional[int],
        record_base.ModelRef("os_referral", referral_code.ReferralCode),
    ]
    """The ID for the referral code the partner used on sign-up,
    if one was used.
    """

    os_referral_name: Annotated[
        Optional[str],
        record_base.ModelRef("os_referral", referral_code.ReferralCode),
    ]
    """The name of the referral code the partner used on sign-up,
    if one was used.
    """

    os_referral: Annotated[
        Optional[referral_code.ReferralCode],
        record_base.ModelRef("os_referral", referral_code.ReferralCode),
    ]
    """The referral code the partner used on sign-up, if one was used.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    os_referral_code_ids: Annotated[
        List[int],
        record_base.ModelRef("os_referral_codes", referral_code.ReferralCode),
    ]
    """A list of IDs for the referral codes the partner has used."""

    os_referral_codes: Annotated[
        List[referral_code.ReferralCode],
        record_base.ModelRef("os_referral_codes", referral_code.ReferralCode),
    ]
    """The referral codes the partner has used.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    os_reseller_id: Annotated[
        Optional[int],
        record_base.ModelRef("os_reseller", reseller.Reseller),
    ]
    """The ID for the reseller for this partner, if this partner
    is billed through a reseller.
    """

    os_reseller_name: Annotated[
        Optional[str],
        record_base.ModelRef("os_reseller", reseller.Reseller),
    ]
    """The name of the reseller for this partner, if this partner
    is billed through a reseller.
    """

    os_reseller: Annotated[
        Optional[reseller.Reseller],
        record_base.ModelRef("os_reseller", reseller.Reseller),
    ]
    """The reseller for this partner, if this partner
    is billed through a reseller.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    os_trial_id: Annotated[
        Optional[int],
        record_base.ModelRef("os_trial", trial.Trial),
    ]
    """The ID for the sign-up trial for this partner,
    if signed up under a trial.
    """

    os_trial_name: Annotated[
        Optional[str],
        record_base.ModelRef("os_trial", trial.Trial),
    ]
    """The name of the sign-up trial for this partner,
    if signed up under a trial.
    """

    os_trial: Annotated[
        Optional[trial.Trial],
        record_base.ModelRef("os_trial", trial.Trial),
    ]
    """The sign-up trial for this partner,
    if signed up under a trial.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    parent_id: Annotated[
        Optional[int],
        record_base.ModelRef("parent_id", Self),
    ]
    """The ID for the parent partner of this partner,
    if it has a parent.
    """

    parent_name: Annotated[
        Optional[str],
        record_base.ModelRef("parent_id", Self),
    ]
    """The name of the parent partner of this partner,
    if it has a parent.
    """

    parent: Annotated[Optional[Self], record_base.ModelRef("parent_id", Self)]
    """The parent partner of this partner,
    if it has a parent.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    property_product_pricelist_id: Annotated[
        Optional[int],
        record_base.ModelRef(
            "property_product_pricelist",
            pricelist.Pricelist,
        ),
    ]
    """The ID for the pricelist this partner uses, if explicitly set.

    If not set, the pricelist set for the customer group
    is used (and if that is not set, the global default
    pricelist is used).
    """

    property_product_pricelist_name: Annotated[
        Optional[str],
        record_base.ModelRef(
            "property_product_pricelist",
            pricelist.Pricelist,
        ),
    ]
    """The name of the pricelist this partner uses, if explicitly set.

    If not set, the pricelist set for the customer group
    is used (and if that is not set, the global default
    pricelist is used).
    """

    property_product_pricelist: Annotated[
        Optional[pricelist.Pricelist],
        record_base.ModelRef(
            "property_product_pricelist",
            pricelist.Pricelist,
        ),
    ]
    """The pricelist this partner uses, if explicitly set.

    If not set, the pricelist set for the customer group
    is used (and if that is not set, the global default
    pricelist is used).

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    stripe_customer_id: Union[str, Literal[False]]
    """The Stripe customer ID for this partner, if one has been assigned."""

    user_id: Annotated[
        Optional[int],
        record_base.ModelRef("user_id", user_module.User),
    ]
    """The ID of the internal user associated with this partner,
    if one is assigned.
    """

    user_name: Annotated[
        Optional[str],
        record_base.ModelRef("user_id", user_module.User),
    ]
    """The name of the internal user associated with this partner,
    if one is assigned.
    """

    user: Annotated[
        Optional[user_module.User],
        record_base.ModelRef("user_id", user_module.User),
    ]
    """The internal user associated with this partner,
    if one is assigned.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class PartnerManager(record_manager_base.RecordManagerBase[Partner]):
    env_name = "res.partner"
    record_class = Partner


# NOTE(callumdickinson): Import here to make sure circular imports work.
from . import (  # noqa: E402
    company as company_module,
    customer_group,
    project_contact,
    referral_code,
    reseller,
    trial,
    user as user_module,
)
