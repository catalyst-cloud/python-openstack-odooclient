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
from typing import Literal, Union

from . import record_base, record_manager_name_base


class Currency(record_base.RecordBase):
    active: bool
    """Whether or not this currency is active (enabled)."""

    currency_unit_label: Union[str, Literal[False]]
    """The unit label for this currency, if set."""

    currency_subunit_label: Union[str, Literal[False]]
    """The sub-unit label for this currency, if set."""

    date: datetime_date
    """The current date to which the currency rate is up to date."""

    decimal_places: int
    """Decimal places taken into account for operations on amounts
    in this currency.

    It is determined by the rounding factor (``rounding`` field).
    """

    name: str
    """The ISO-4217 currency code for the currency."""

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
    record_manager_name_base.NamedRecordManagerBase[Currency],
):
    env_name = "res.currency"
    record_class = Currency
