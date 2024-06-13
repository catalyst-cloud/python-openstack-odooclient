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
from typing import TYPE_CHECKING, List

from . import record_base, record_manager_code_base

if TYPE_CHECKING:
    from . import credit_type, partner


class ReferralCode(record_base.RecordBase):
    allowed_uses: int
    """The number of allowed uses of this referral code.

    Set to ``-1`` for unlimited uses.
    """

    before_reward_usage_threshold: float
    """The amount of usage that must be recorded by the new sign-up
    before the reward credit is awarded to the referrer.
    """

    code: str
    """The unique referral code."""

    name: str
    """Automatically generated name for the referral code."""

    @property
    def referral_ids(self) -> List[int]:
        """A list of IDs for the partners that signed up
        using this referral code.
        """
        return self._get_field("referrals")

    @cached_property
    def referrals(self) -> List[partner.Partner]:
        """The partners that signed up using this referral code.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.partners.list(self.referral_ids)

    referral_credit_amount: float
    """Initial balance for the referral credit."""

    referral_credit_duration: int
    """Duration of the referral credit, in days."""

    @property
    def referral_credit_type_id(self) -> int:
        """The ID of the credit type to use for the referral credit."""
        return self._get_ref_id("referral_credit_type")

    @property
    def referral_credit_type_name(self) -> str:
        """The name of the credit type to use for the referral credit."""
        return self._get_ref_name("referral_credit_type")

    @cached_property
    def referral_credit_type(self) -> credit_type.CreditType:
        """The credit type to use for the referral credit.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.credit_types.get(self.referral_credit_type_id)

    reward_credit_amount: float
    """Initial balance for the reward credit."""

    reward_credit_duration: int
    """Duration of the reward credit, in days."""

    @property
    def reward_credit_type_id(self) -> int:
        """The ID of the credit type to use for the reward credit."""
        return self._get_ref_id("reward_credit_type")

    @property
    def reward_credit_type_name(self) -> str:
        """The name of the credit type to use for the reward credit."""
        return self._get_ref_name("reward_credit_type")

    @cached_property
    def reward_credit_type(self) -> credit_type.CreditType:
        """The credit type to use for the reward credit.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.credit_types.get(self.reward_credit_type_id)

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "referral_ids": "referrals",
        "referral_credit_type_id": "referral_credit_type",
        "reward_credit_type_id": "reward_credit_type",
    }


class ReferralCodeManager(
    record_manager_code_base.CodedRecordManagerBase[ReferralCode],
):
    env_name = "openstack.referral_code"
    record_class = ReferralCode
