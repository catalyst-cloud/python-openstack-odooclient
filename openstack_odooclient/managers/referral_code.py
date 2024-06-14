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

from typing import List

from typing_extensions import Annotated

from . import record_base, record_manager_code_base, util


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

    referral_ids: Annotated[List[int], util.ModelRef("referrals")]
    """A list of IDs for the partners that signed up
    using this referral code.
    """

    referrals: Annotated[List[partner.Partner], util.ModelRef("referrals")]
    """The partners that signed up using this referral code.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    referral_credit_amount: float
    """Initial balance for the referral credit."""

    referral_credit_duration: int
    """Duration of the referral credit, in days."""

    referral_credit_type_id: Annotated[
        int,
        util.ModelRef("referral_credit_type"),
    ]
    """The ID of the credit type to use for the referral credit."""

    referral_credit_type_name: Annotated[
        str,
        util.ModelRef("referral_credit_type"),
    ]
    """The name of the credit type to use for the referral credit."""

    referral_credit_type: Annotated[
        credit_type.CreditType,
        util.ModelRef("referral_credit_type"),
    ]
    """The credit type to use for the referral credit.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    reward_credit_amount: float
    """Initial balance for the reward credit."""

    reward_credit_duration: int
    """Duration of the reward credit, in days."""

    reward_credit_type_id: Annotated[int, util.ModelRef("reward_credit_type")]
    """The ID of the credit type to use for the reward credit."""

    reward_credit_type_name: Annotated[
        str,
        util.ModelRef("reward_credit_type"),
    ]
    """The name of the credit type to use for the reward credit."""

    reward_credit_type: Annotated[
        credit_type.CreditType,
        util.ModelRef("reward_credit_type"),
    ]
    """The credit type to use for the reward credit.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class ReferralCodeManager(
    record_manager_code_base.CodedRecordManagerBase[ReferralCode],
):
    env_name = "openstack.referral_code"
    record_class = ReferralCode


# NOTE(callumdickinson): Import here to avoid circular imports.
from . import credit_type, partner  # noqa: E402
