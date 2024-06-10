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
from typing import TYPE_CHECKING

from . import record

if TYPE_CHECKING:
    from . import credit as credit_module


class CreditTransaction(record.RecordBase):
    @property
    def credit_id(self) -> int:
        """The ID of the credit this transaction was made against."""
        return self._get_ref_id("credit")

    @property
    def credit_name(self) -> str:
        """The name of the credit this transaction was made against."""
        return self._get_ref_name("credit")

    @cached_property
    def credit(self) -> credit_module.Credit:
        """The credit this transaction was made against.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.credits.get(self.credit_id)

    description: str
    """A description of this credit transaction."""

    value: float
    """The value of the credit transaction."""

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "credit_id": "credit",
    }


class CreditTransactionManager(record.RecordManagerBase[CreditTransaction]):
    env_name = "openstack.credit.transaction"
    record_class = CreditTransaction
