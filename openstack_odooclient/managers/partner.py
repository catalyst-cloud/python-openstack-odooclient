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
from typing import TYPE_CHECKING, List, Literal, Optional, Union

from . import record

if TYPE_CHECKING:
    from . import (
        customer_group,
        pricelist,
        project,
        project_contact,
        referral_code,
        reseller,
        trial,
        user as user_module,
    )


class Partner(record.RecordBase):
    active: bool
    """Whether or not this Partner is active."""

    email: str
    """Main e-mail address for the partner."""

    name: str
    """Full name of the partner."""

    @property
    def os_customer_group_id(self) -> Optional[int]:
        """The ID for the customer group this partner is part of,
        if it is part of one.
        """
        return self._get_ref_id("os_customer_group", optional=True)

    @property
    def os_customer_group_name(self) -> Optional[str]:
        """The name of the customer group this partner is part of,
        if it is part of one.
        """
        return self._get_ref_name("os_customer_group", optional=True)

    @cached_property
    def os_customer_group(self) -> Optional[customer_group.CustomerGroup]:
        """The customer group this partner is part of,
        if it is part of one.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.os_customer_group_id
        return (
            self._client.customer_groups.get(record_id)
            if record_id is not None
            else None
        )

    @property
    def os_project_ids(self) -> List[int]:
        """A list of IDs for the OpenStack projects that
        belong to this partner.
        """
        return self._get_field("os_projects")

    @cached_property
    def os_projects(self) -> List[project.Project]:
        """The OpenStack projects that belong to this partner.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.projects.list(self.os_project_ids)

    @property
    def os_project_contact_ids(self) -> List[int]:
        """A list of IDs for the project contacts that are associated
        with this partner.
        """
        return self._get_field("os_project_contacts")

    @cached_property
    def os_project_contacts(self) -> List[project_contact.ProjectContact]:
        """The project contacts that are associated with this partner.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.project_contacts.list(self.os_project_contact_ids)

    @property
    def os_referral_id(self) -> Optional[int]:
        """The ID for the referral code the partner used on sign-up,
        if one was used.
        """
        return self._get_ref_id("os_referral", optional=True)

    @property
    def os_referral_name(self) -> Optional[str]:
        """The name of the referral code the partner used on sign-up,
        if one was used.
        """
        return self._get_ref_name("os_referral", optional=True)

    @cached_property
    def os_referral(self) -> Optional[referral_code.ReferralCode]:
        """The referral code the partner used on sign-up, if one was used.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.os_referral_id
        return (
            self._client.referral_codes.get(record_id)
            if record_id is not None
            else None
        )

    @property
    def os_referral_code_ids(self) -> List[int]:
        """A list of IDs for the referral codes the partner has used."""
        return self._get_field("os_referral_codes")

    @cached_property
    def os_referral_codes(self) -> List[referral_code.ReferralCode]:
        """The referral codes the partner has used.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.referral_codes.list(self.os_referral_code_ids)

    @property
    def os_reseller_id(self) -> Optional[int]:
        """The ID for the reseller for this partner, if this partner
        is billed through a reseller.
        """
        return self._get_ref_id("os_reseller", optional=True)

    @property
    def os_reseller_name(self) -> Optional[str]:
        """The name of the reseller for this partner, if this partner
        is billed through a reseller.
        """
        return self._get_ref_name("os_reseller", optional=True)

    @cached_property
    def os_reseller(self) -> Optional[reseller.Reseller]:
        """The reseller for this partner, if this partner
        is billed through a reseller.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.os_reseller_id
        return (
            self._client.resellers.get(record_id)
            if record_id is not None
            else None
        )

    @property
    def os_trial_id(self) -> Optional[int]:
        """The ID for the sign-up trial for this partner,
        if signed up under a trial.
        """
        return self._get_ref_id("os_trial", optional=True)

    @property
    def os_trial_name(self) -> Optional[str]:
        """The name of the sign-up trial for this partner,
        if signed up under a trial.
        """
        return self._get_ref_name("os_trial", optional=True)

    @cached_property
    def os_trial(self) -> Optional[trial.Trial]:
        """The sign-up trial for this partner,
        if signed up under a trial.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.os_trial_id
        return (
            self._client.trials.get(record_id)
            if record_id is not None
            else None
        )

    @property
    def parent_id(self) -> Optional[int]:
        """The ID for the parent partner of this partner,
        if it has a parent.
        """
        return self._get_ref_id("parent_id", optional=True)

    @property
    def parent_name(self) -> Optional[str]:
        """The name of the parent partner of this partner,
        if it has a parent.
        """
        return self._get_ref_name("parent_id", optional=True)

    @cached_property
    def parent(self) -> Optional[Partner]:
        """The parent partner of this partner,
        if it has a parent.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.parent_id
        return (
            self._client.partners.get(record_id)
            if record_id is not None
            else None
        )

    @property
    def property_product_pricelist_id(self) -> Optional[int]:
        """The ID for the pricelist this partner uses, if explicitly set.

        If not set, the pricelist set for the customer group
        is used (and if that is not set, the global default
        pricelist is used).
        """
        return self._get_ref_id("property_product_pricelist", optional=True)

    @property
    def property_product_pricelist_name(self) -> Optional[str]:
        """The name of the pricelist this partner uses, if explicitly set.

        If not set, the pricelist set for the customer group
        is used (and if that is not set, the global default
        pricelist is used).
        """
        return self._get_ref_name("property_product_pricelist", optional=True)

    @cached_property
    def property_product_pricelist(self) -> Optional[pricelist.Pricelist]:
        """The pricelist this partner uses, if explicitly set.

        If not set, the pricelist set for the customer group
        is used (and if that is not set, the global default
        pricelist is used).

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.property_product_pricelist_id
        return (
            self._client.pricelists.get(record_id)
            if record_id is not None
            else None
        )

    stripe_customer_id: Union[str, Literal[False]]
    """The Stripe customer ID for this Partner, if one has been assigned."""

    @property
    def user_id(self) -> Optional[int]:
        """The ID of the internal user in charge of this partner,
        if one is assigned.
        """
        return self._get_ref_id("user_id", optional=True)

    @property
    def user_name(self) -> Optional[str]:
        """The ID of the internal user in charge of this partner,
        if one is assigned.
        """
        return self._get_ref_name("user_id")

    @cached_property
    def user(self) -> Optional[user_module.User]:
        """The internal user in charge of this partner,
        if one is assigned.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.user_id
        return (
            self._client.users.get(record_id)
            if record_id is not None
            else None
        )

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "os_customer_group_id": "os_customer_group",
        "os_project_ids": "os_projects",
        "os_project_contact_ids": "os_project_contacts",
        "os_referral_id": "os_referral",
        "os_referral_code_ids": "os_referral_codes",
        "os_reseller_id": "os_reseller",
        "os_trial_id": "os_trial",
        "parent": "parent_id",
        "property_product_pricelist_id": "property_product_pricelist",
        "user": "user_id",
    }


class PartnerManager(record.RecordManagerBase[Partner]):
    env_name = "res.partner"
    record_class = Partner
