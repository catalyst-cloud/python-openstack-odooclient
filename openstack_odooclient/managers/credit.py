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
from typing import Annotated

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase


class Credit(RecordBase["CreditManager"]):
    credit_type_id: Annotated[int, ModelRef("credit_type", CreditType)]
    """The ID of the type of this credit."""

    credit_type_name: Annotated[str, ModelRef("credit_type", CreditType)]
    """The name of the type of this credit."""

    credit_type: Annotated[CreditType, ModelRef("credit_type", CreditType)]
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

    transaction_ids: Annotated[
        list[int],
        ModelRef("transactions", CreditTransaction),
    ]
    """A list of IDs for the transactions that have been made
    using this credit.
    """

    transactions: Annotated[
        list[CreditTransaction],
        ModelRef("transactions", CreditTransaction),
    ]
    """The transactions that have been made using this credit.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    voucher_code_id: Annotated[
        int | None,
        ModelRef("voucher_code", VoucherCode),
    ]
    """The ID of the voucher code used when applying for the credit,
    if one was supplied.
    """

    voucher_code_name: Annotated[
        str | None,
        ModelRef("voucher_code", VoucherCode),
    ]
    """The name of the voucher code used when applying for the credit,
    if one was supplied.
    """

    voucher_code: Annotated[
        VoucherCode | None,
        ModelRef("voucher_code", VoucherCode),
    ]
    """The voucher code used when applying for the credit,
    if one was supplied.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class CreditManager(RecordManagerBase[Credit]):
    env_name = "openstack.credit"
    record_class = Credit


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .credit_transaction import CreditTransaction  # noqa: E402
from .credit_type import CreditType  # noqa: E402
from .voucher_code import VoucherCode  # noqa: E402
