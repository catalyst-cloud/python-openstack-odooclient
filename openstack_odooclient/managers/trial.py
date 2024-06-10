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
from functools import cached_property
from typing import TYPE_CHECKING, Literal, Union

from . import record

if TYPE_CHECKING:
    from . import partner as partner_module


class Trial(record.RecordBase):
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

    @property
    def partner_id(self) -> int:
        """The ID for the target partner for this trial."""
        return self._get_ref_id("partner")

    @property
    def partner_name(self) -> str:
        """The name of the target partner for this trial."""
        return self._get_ref_name("partner")

    @cached_property
    def partner(self) -> partner_module.Partner:
        """The target partner for this trial.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.partners.get(self.partner_id)

    start_date: date
    """The start date of this trial."""

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "partner_id": "partner",
    }


class TrialManager(record.RecordManagerBase[Trial]):
    env_name = "openstack.trial"
    record_class = Trial
