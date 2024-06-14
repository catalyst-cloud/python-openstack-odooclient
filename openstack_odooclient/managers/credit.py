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
from typing import List, Optional

from typing_extensions import Annotated

from . import record_base, record_manager_base, util


class Credit(record_base.RecordBase):
    credit_type_id: Annotated[int, util.ModelRef("credit_type")]
    """The ID of the type of this credit."""

    credit_type_name: Annotated[str, util.ModelRef("credit_type")]
    """The name of the type of this credit."""

    credit_type: Annotated[
        credit_type_module.CreditType,
        util.ModelRef("credit_type"),
    ]
    """The type of this credit.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

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

    transaction_ids: Annotated[List[int], util.ModelRef("transactions")]
    """A list of IDs for the transactions that have been made
    using this credit.
    """

    transactions: Annotated[
        List[credit_transaction.CreditTransaction],
        util.ModelRef("transactions"),
    ]
    """The transactions that have been made using this credit.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    voucher_code_id: Annotated[Optional[int], util.ModelRef("voucher_code")]
    """The ID of the voucher code used when applying for the credit,
    if one was supplied.
    """

    voucher_code_name: Annotated[Optional[str], util.ModelRef("voucher_code")]
    """The name of the voucher code used when applying for the credit,
    if one was supplied.
    """

    voucher_code: Annotated[
        Optional[voucher_code_module.VoucherCode],
        util.ModelRef("voucher_code"),
    ]
    """The voucher code used when applying for the credit,
    if one was supplied.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class CreditManager(record_manager_base.RecordManagerBase[Credit]):
    env_name = "openstack.credit"
    record_class = Credit


# NOTE(callumdickinson): Import here to make sure circular imports work.
from . import (  # noqa: E402
    credit_transaction,
    credit_type as credit_type_module,
    voucher_code as voucher_code_module,
)
