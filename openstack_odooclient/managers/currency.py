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

from datetime import date as datetime_date
from typing import Literal

from ..base.record.base import RecordBase
from ..base.record_manager.base import RecordManagerBase
from ..mixins.named_record import NamedRecordManagerMixin, NamedRecordMixin


class Currency(
    RecordBase["CurrencyManager"],
    NamedRecordMixin["CurrencyManager"],
):
    active: bool
    """Whether or not this currency is active (enabled)."""

    currency_unit_label: str | Literal[False]
    """The unit label for this currency, if set."""

    currency_subunit_label: str | Literal[False]
    """The sub-unit label for this currency, if set."""

    date: datetime_date
    """The age of the set currency rate."""

    decimal_places: int
    """Decimal places taken into account for operations on amounts
    in this currency.

    It is determined by the rounding factor (``rounding`` field).
    """

    position: Literal["before", "after"]
    """The position of the currency unit relative to the amount.

    Values:

    * ``before`` - Place the unit before the amount
    * ``after`` - Place the unit after the amount
    """

    rate: float
    """The rate of the currency to the currency of rate 1."""

    rounding: float
    """The rounding factor configured for this currency."""

    symbol: str
    """The currency sign to be used when printing amounts."""


class CurrencyManager(
    RecordManagerBase[Currency],
    NamedRecordManagerMixin[Currency],
):
    env_name = "res.currency"
    record_class = Currency
