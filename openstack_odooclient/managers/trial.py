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
from typing import Literal, Union

from typing_extensions import Annotated

from . import record_base, record_manager_base, util


class Trial(record_base.RecordBase):
    account_suspended_date: Union[date, Literal[False]]
    """The date the account was suspended, following the end of the trial."""

    account_terminated_date: Union[date, Literal[False]]
    """The date the account was terminated, following the end of the trial."""

    account_upgraded_date: Union[date, Literal[False]]
    """The date the account was upgraded to a full account,
    following the end of the trial.
    """

    end_date: date
    """The end date of this trial."""

    partner_id: Annotated[int, util.ModelRef("partner")]
    """The ID for the target partner for this trial."""

    partner_name: Annotated[str, util.ModelRef("partner")]
    """The name of the target partner for this trial."""

    partner: Annotated[partner_module.Partner, util.ModelRef("partner")]
    """The target partner for this trial.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    start_date: date
    """The start date of this trial."""


class TrialManager(record_manager_base.RecordManagerBase[Trial]):
    env_name = "openstack.trial"
    record_class = Trial


# NOTE(callumdickinson): Import here to avoid circular imports.
from . import partner as partner_module  # noqa: E402
