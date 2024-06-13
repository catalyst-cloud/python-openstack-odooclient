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

from typing_extensions import Annotated

from . import (
    pricelist,
    project,
    record_base,
    record_manager_base,
    util,
)


class Partner(record_base.RecordBase):
    active: bool
    """Whether or not this partner is active (enabled)."""

    company_id: Annotated[int, util.ModelRef("company_id")]
    """The ID for the company this partner is owned by."""

    company_name: Annotated[str, util.ModelRef("company_id")]
    """The name of the company this partner is owned by."""

    company: Annotated[company_module.Company, util.ModelRef("company_id")]
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
        util.ModelRef("os_customer_group"),
    ]
    """The ID for the customer group this partner is part of,
    if it is part of one.
    """

    os_customer_group_name: Annotated[
        Optional[str],
        util.ModelRef("os_customer_group"),
    ]
    """The name of the customer group this partner is part of,
    if it is part of one.
    """

    os_customer_group: Annotated[
        Optional[customer_group.CustomerGroup],
        util.ModelRef("os_customer_group"),
    ]
    """The customer group this partner is part of,
    if it is part of one.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    os_project_ids: Annotated[List[int], util.ModelRef("os_projects")]
    """A list of IDs for the OpenStack projects that
    belong to this partner.
    """

    os_projects: Annotated[
        List[project.Project],
        util.ModelRef("os_projects"),
    ]
    """The OpenStack projects that belong to this partner.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    os_project_contact_ids: Annotated[
        List[int],
        util.ModelRef("os_project_contacts"),
    ]
    """A list of IDs for the project contacts that are associated
    with this partner.
    """

    os_project_contacts: Annotated[
        List[project_contact.ProjectContact],
        util.ModelRef("os_project_contacts"),
    ]
    """The project contacts that are associated with this partner.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    os_referral_id: Annotated[Optional[int], util.ModelRef("os_referral")]
    """The ID for the referral code the partner used on sign-up,
    if one was used.
    """

    os_referral_name: Annotated[Optional[str], util.ModelRef("os_referral")]
    """The name of the referral code the partner used on sign-up,
    if one was used.
    """

    os_referral: Annotated[
        Optional[referral_code.ReferralCode],
        util.ModelRef("os_referral"),
    ]
    """The referral code the partner used on sign-up, if one was used.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    os_referral_code_ids: Annotated[
        List[int],
        util.ModelRef("os_referral_codes"),
    ]
    """A list of IDs for the referral codes the partner has used."""

    os_referral_codes: Annotated[
        List[referral_code.ReferralCode],
        util.ModelRef("os_referral_codes"),
    ]
    """The referral codes the partner has used.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    os_reseller_id: Annotated[Optional[int], util.ModelRef("os_reseller")]
    """The ID for the reseller for this partner, if this partner
    is billed through a reseller.
    """

    os_reseller_name: Annotated[Optional[str], util.ModelRef("os_reseller")]
    """The name of the reseller for this partner, if this partner
    is billed through a reseller.
    """

    os_reseller: Annotated[
        Optional[reseller.Reseller],
        util.ModelRef("os_reseller"),
    ]
    """The reseller for this partner, if this partner
    is billed through a reseller.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    os_trial_id: Annotated[Optional[int], util.ModelRef("os_trial")]
    """The ID for the sign-up trial for this partner,
    if signed up under a trial.
    """

    os_trial_name: Annotated[Optional[str], util.ModelRef("os_trial")]
    """The name of the sign-up trial for this partner,
    if signed up under a trial.
    """

    os_trial: Annotated[Optional[trial.Trial], util.ModelRef("os_trial")]
    """The sign-up trial for this partner,
    if signed up under a trial.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    parent_id: Annotated[Optional[int], util.ModelRef("parent_id")]
    """The ID for the parent partner of this partner,
    if it has a parent.
    """

    parent_name: Annotated[Optional[str], util.ModelRef("parent_id")]
    """The name of the parent partner of this partner,
    if it has a parent.
    """

    parent: Annotated[Optional[Partner], util.ModelRef("parent_id")]
    """The parent partner of this partner,
    if it has a parent.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    property_product_pricelist_id: Annotated[
        Optional[int],
        util.ModelRef("property_product_pricelist"),
    ]
    """The ID for the pricelist this partner uses, if explicitly set.

    If not set, the pricelist set for the customer group
    is used (and if that is not set, the global default
    pricelist is used).
    """

    property_product_pricelist_name: Annotated[
        Optional[str],
        util.ModelRef("property_product_pricelist"),
    ]
    """The name of the pricelist this partner uses, if explicitly set.

    If not set, the pricelist set for the customer group
    is used (and if that is not set, the global default
    pricelist is used).
    """

    property_product_pricelist: Annotated[
        Optional[pricelist.Pricelist],
        util.ModelRef("property_product_pricelist"),
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

    user_id: Annotated[Optional[int], util.ModelRef("user_id")]
    """The ID of the internal user associated with this partner,
    if one is assigned.
    """

    user_name: Annotated[Optional[str], util.ModelRef("user_id")]
    """The name of the internal user associated with this partner,
    if one is assigned.
    """

    user: Annotated[Optional[user_module.User], util.ModelRef("user_id")]
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
