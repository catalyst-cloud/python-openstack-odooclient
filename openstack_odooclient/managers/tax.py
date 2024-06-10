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
from typing import TYPE_CHECKING, Literal

from . import record

if TYPE_CHECKING:
    from . import company as company_module, tax_group as tax_group_module


class Tax(record.RecordBase):
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

    @property
    def company_id(self) -> int:
        """The ID for the company this tax is owned by."""
        return self._get_ref_id("company_id")

    @property
    def company_name(self) -> str:
        """The name of the company this tax is owned by."""
        return self._get_ref_name("company_id")

    @cached_property
    def company(self) -> company_module.Company:
        """The company this tax is owned by.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.companies.get(self.company_id)

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

    @property
    def tax_group_id(self) -> int:
        """The ID for the company partner this tax is owned by."""
        return self._get_ref_id("tax_group_id")

    @property
    def tax_group_name(self) -> str:
        """The name of the tax_group partner this tax is owned by."""
        return self._get_ref_name("tax_group_id")

    @cached_property
    def tax_group(self) -> tax_group_module.TaxGroup:
        """The tax_group partner this tax is owned by.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.tax_groups.get(self.tax_group_id)

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "company": "company_id",
        "tax_group": "tax_group_id",
    }


class TaxManager(record.NamedRecordManagerBase[Tax]):
    env_name = "account.tax"
    record_class = Tax
