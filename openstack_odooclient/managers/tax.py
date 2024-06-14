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

from typing import Literal

from typing_extensions import Annotated

from . import record_base, record_manager_name_base, util


class Tax(record_base.RecordBase):
    active: bool
    """Whether or not this tax is active (enabled)."""

    amount: float
    """The amount of tax to apply."""

    amount_type: Literal["group", "fixed", "percent", "division"]
    """
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

    company_id: Annotated[int, util.ModelRef("company_id")]
    """The ID for the company this tax is owned by."""

    company_name: Annotated[str, util.ModelRef("company_id")]
    """The name of the company this tax is owned by."""

    company: Annotated[company_module.Company, util.ModelRef("company_id")]
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

    name: str
    """Tax name."""

    price_include: bool
    """Whether or not prices included in invoices should include this tax."""

    tax_eligibility: Literal["on_invoice", "on_payment"]
    """When the tax is due for the invoice.

    Values:

    * ``on_invoice`` - Due as soon as the invoice is validated
    * ``on_payment`` - Due as soon as payment of the invoice is received
    """

    tax_group_id: Annotated[int, util.ModelRef("tax_group_id")]
    """The ID for the tax group this tax is categorised under."""

    tax_group_name: Annotated[str, util.ModelRef("tax_group_id")]
    """The name of the tax group this tax is categorised under."""

    tax_group: Annotated[
        tax_group_module.TaxGroup,
        util.ModelRef("tax_group_id"),
    ]
    """The tax group this tax is categorised under.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class TaxManager(record_manager_name_base.NamedRecordManagerBase[Tax]):
    env_name = "account.tax"
    record_class = Tax


# NOTE(callumdickinson): Import here to avoid circular imports.
from . import (  # noqa: E402
    company as company_module,
    tax_group as tax_group_module,
)
