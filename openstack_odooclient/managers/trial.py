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
from typing import Annotated, Literal

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase


class Trial(RecordBase["TrialManager"]):
    account_suspended_date: date | Literal[False]
    """The date the account was suspended, following the end of the trial."""

    account_terminated_date: date | Literal[False]
    """The date the account was terminated, following the end of the trial."""

    account_upgraded_date: date | Literal[False]
    """The date the account was upgraded to a full account,
    following the end of the trial.
    """

    end_date: date
    """The end date of this trial."""

    partner_id: Annotated[int, ModelRef("partner", Partner)]
    """The ID for the target partner for this trial."""

    partner_name: Annotated[str, ModelRef("partner", Partner)]
    """The name of the target partner for this trial."""

    partner: Annotated[Partner, ModelRef("partner", Partner)]
    """The target partner for this trial.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    start_date: date
    """The start date of this trial."""


class TrialManager(RecordManagerBase[Trial]):
    env_name = "openstack.trial"
    record_class = Trial


# NOTE(callumdickinson): Import here to avoid circular imports.
from .partner import Partner  # noqa: E402
