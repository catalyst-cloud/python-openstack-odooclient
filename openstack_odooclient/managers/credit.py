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
from typing import TYPE_CHECKING, List, Optional

from . import record

if TYPE_CHECKING:
    from . import (
        credit_transaction,
        credit_type as credit_type_module,
        voucher_code as voucher_code_module,
    )


class Credit(record.RecordBase):
    @property
    def credit_type_id(self) -> int:
        """The ID of the type of this credit."""
        return self._get_ref_id("credit_type")

    @property
    def credit_type_name(self) -> str:
        """The name of this type of credit."""
        return self._get_ref_name("credit_type")

    @cached_property
    def credit_type(self) -> credit_type_module.CreditType:
        """The type of this credit.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.credit_types.get(self.credit_type_id)

    current_balance: float
    """The current remaining balance on the credit."""

    expiry_date: date
    """The date the credit expires."""

    initial_balance: float
    """The initial balance this credit started off with."""

    name: str
    """The automatically generated name of the credit."""

    start_date: date
    """The start date of the credit."""

    @property
    def transaction_ids(self) -> List[int]:
        """A list of IDs for the transactions that have been made
        using this credit.
        """
        return self._get_field("transactions")

    @cached_property
    def transactions(self) -> List[credit_transaction.CreditTransaction]:
        """The transactions that have been made using this credit.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.credit_transactions.list(self.transaction_ids)

    @property
    def voucher_code_id(self) -> Optional[int]:
        """The ID of the voucher code used when applying for the credit,
        if one was supplied.
        """
        return self._get_ref_id("voucher_code", optional=True)

    @property
    def voucher_code_name(self) -> Optional[str]:
        """The name of the voucher code used when applying for the credit,
        if one was supplied.
        """
        return self._get_ref_name("voucher_code", optional=True)

    @cached_property
    def voucher_code(self) -> Optional[voucher_code_module.VoucherCode]:
        """Voucher code used when applying for the credit,
        if one was supplied.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.voucher_code_id
        return (
            self._client.voucher_codes.get(record_id)
            if record_id is not None
            else None
        )

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "credit_type_id": "credit_type",
        "transaction_ids": "transactions",
        "voucher_code_id": "voucher_code",
    }


class CreditManager(record.RecordManagerBase[Credit]):
    env_name = "openstack.credit"
    record_class = Credit
