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

from typing import Annotated, Literal

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase
from ..mixins.named_record import NamedRecordManagerMixin, NamedRecordMixin


class Tax(RecordBase["TaxManager"], NamedRecordMixin["TaxManager"]):
    active: bool
    """Whether or not this tax is active (enabled)."""

    amount: float
    """The amount of tax to apply."""

    amount_type: Literal["group", "fixed", "percent", "division"]
    """The method that should be used to tax invoices.

    Values:

    * ``group`` - Group of Taxes
    * ``fixed`` - Fixed
    * ``percent`` - Percentage of Price
    * ``division`` - Percentage of Price Tax Included
    """

    analytic: bool
    """When set to ``True``, the amount computed by this tax will be assigned
    to the same analytic account as the invoice line (if any).
    """

    company_id: Annotated[int, ModelRef("company_id", Company)]
    """The ID for the company this tax is owned by."""

    company_name: Annotated[str, ModelRef("company_id", Company)]
    """The name of the company this tax is owned by."""

    company: Annotated[Company, ModelRef("company_id", Company)]
    """The company this tax is owned by.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    country_code: str
    """The country code for this tax."""

    description: str
    """The label for this tax on invoices."""

    include_base_amount: bool
    """When set to ``True``, taxes included after this one will be calculated
    based on the price with this tax included.
    """

    price_include: bool
    """Whether or not prices included in invoices should include this tax."""

    tax_eligibility: Literal["on_invoice", "on_payment"]
    """When the tax is due for the invoice.

    Values:

    * ``on_invoice`` - Due as soon as the invoice is validated
    * ``on_payment`` - Due as soon as payment of the invoice is received
    """

    tax_group_id: Annotated[int, ModelRef("tax_group_id", TaxGroup)]
    """The ID for the tax group this tax is categorised under."""

    tax_group_name: Annotated[str, ModelRef("tax_group_id", TaxGroup)]
    """The name of the tax group this tax is categorised under."""

    tax_group: Annotated[TaxGroup, ModelRef("tax_group_id", TaxGroup)]
    """The tax group this tax is categorised under.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class TaxManager(RecordManagerBase[Tax], NamedRecordManagerMixin[Tax]):
    env_name = "account.tax"
    record_class = Tax


# NOTE(callumdickinson): Import here to avoid circular imports.
from .company import Company  # noqa: E402
from .tax_group import TaxGroup  # noqa: E402
