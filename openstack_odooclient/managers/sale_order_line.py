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
from typing import TYPE_CHECKING, List, Literal, Optional, Union

from . import record_base, record_manager_base

if TYPE_CHECKING:
    from . import (
        account_move_line,
        company as company_module,
        currency as currency_module,
        partner,
        product as product_module,
        project,
        sale_order,
        tax as tax_module,
        uom,
    )


class SaleOrderLine(record_base.RecordBase):
    @property
    def company_id(self) -> int:
        """The ID for the company this sale order line
        was generated for.
        """
        return self._get_ref_id("company_id")

    @property
    def company_name(self) -> str:
        """The name of the company this sale order line
        was generated for.
        """
        return self._get_ref_name("company_id")

    @cached_property
    def company(self) -> company_module.Company:
        """The company this sale order line
        was generated for.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.companies.get(self.company_id)

    @property
    def currency_id(self) -> int:
        """The ID for the currency used in this sale order line."""
        return self._get_ref_id("currency_id")

    @property
    def currency_name(self) -> str:
        """The name of the currency used in this sale order line."""
        return self._get_ref_name("currency_id")

    @cached_property
    def currency(self) -> currency_module.Currency:
        """The currency used in this sale order line.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.currencies.get(self.currency_id)

    discount: float
    """Discount percentage on the sale order line (0-100)."""

    display_name: str
    """Display name for the sale order line in the sale order."""

    @property
    def invoice_line_ids(self) -> List[int]:
        """A list of IDs for the invoice (account move) lines created
        from this sale order line.
        """
        return self._get_field("invoice_lines")

    @cached_property
    def invoice_lines(self) -> List[account_move_line.AccountMoveLine]:
        """The invoice (account move) lines created
        from this sale order line.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.account_move_lines.list(self.invoice_line_ids)

    invoice_status: Literal["no", "to invoice", "invoiced", "upselling"]
    """The current invoicing status of this sale order line.

    Values:

    * ``no`` - Nothing to invoice
    * ``to invoice`` - Has quantity that needs to be invoiced
    * ``invoiced`` - Fully invoiced
    * ``upselling`` - Upselling opportunity
    """

    is_downpayment: bool
    """Whether or not this sale order line is a downpayment."""

    is_expense: bool
    """Whether or not this sale order line is an expense."""

    name: str
    """Name assigned to the the sale order line.

    This is not the same as the product name.
    In the OpenStack Integration add-on, this is normally used to store
    the resource's name.
    """

    @property
    def order_id(self) -> int:
        """The ID for the sale order this line is linked to."""
        return self._get_ref_id("order_id")

    @property
    def order_name(self) -> str:
        """The name of the sale order this line is linked to."""
        return self._get_ref_name("order_id")

    @cached_property
    def order(self) -> sale_order.SaleOrder:
        """The sale order this line is linked to.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.sale_orders.get(self.order_id)

    @property
    def order_partner_id(self) -> int:
        """The ID for the recipient partner for the sale order."""
        return self._get_ref_id("order_partner_id")

    @property
    def order_partner_name(self) -> str:
        """The name of the recipient partner for the sale order."""
        return self._get_ref_name("order_partner_id")

    @cached_property
    def order_partner(self) -> partner.Partner:
        """The recipient partner for the sale order.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.partners.get(self.order_partner_id)

    @property
    def os_project_id(self) -> Optional[int]:
        """The ID for the the OpenStack project this sale order line was
        was generated for.
        """
        return self._get_ref_id("os_project", optional=True)

    @property
    def os_project_name(self) -> Optional[str]:
        """The name of the the OpenStack project this sale order line was
        was generated for.
        """
        return self._get_ref_name("os_project", optional=True)

    @cached_property
    def os_project(self) -> Optional[project.Project]:
        """The OpenStack project this sale order line was
        was generated for.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.os_project_id
        return (
            self._client.projects.get(record_id)
            if record_id is not None
            else None
        )

    os_region: Union[str, Literal[False]]
    """The OpenStack region the sale order line was created from."""

    os_resource_id: Union[str, Literal[False]]
    """The OpenStack resource ID for the resource that generated
    this sale order line.
    """

    os_resource_name: Union[str, Literal[False]]
    """The name of the OpenStack resource tier or flavour,
    as used by services such as Distil for rating purposes.

    For example, if this is the sale order line for a compute instance,
    this would be set to the instance's flavour name.
    """

    os_resource_type: Union[str, Literal[False]]
    """A human-readable description of the type of resource captured
    by this sale order line.
    """

    price_reduce: float
    """Base unit price, less discount (see the ``discount`` field)."""

    price_reduce_taxexcl: float
    """Actual unit price, excluding tax."""

    price_reduce_taxinc: float
    """Actual unit price, including tax."""

    price_subtotal: float
    """Subtotal price for the sale order line, excluding tax."""

    price_tax: float
    """Tax charged on the sale order line."""

    price_total: float
    """Total price for the sale order line, including tax."""

    price_unit: float
    """Base unit price, excluding tax, before any discounts."""

    @property
    def product_id(self) -> int:
        """The ID of the product charged on this sale order line."""
        return self._get_ref_id("product_id")

    @property
    def product_name(self) -> str:
        """The name of the product charged on this sale order line."""
        return self._get_ref_name("product_id")

    @cached_property
    def product(self) -> product_module.Product:
        """The product charged on this sale order line.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.products.get(self.product_id)

    @property
    def product_uom_id(self) -> int:
        """The ID for the Unit of Measure for the product being charged in
        this sale order line.
        """
        return self._get_ref_id("product_uom")

    @property
    def product_uom_name(self) -> str:
        """The name of the Unit of Measure for the product being charged in
        this sale order line.
        """
        return self._get_ref_name("product_uom")

    @cached_property
    def product_uom(self) -> uom.Uom:
        """The Unit of Measure for the product being charged in
        this sale order line.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.uoms.get(self.product_uom_id)

    product_uom_qty: float
    """The product quantity on the sale order line."""

    product_uom_readonly: bool
    """Whether or not the product quantity can still be updated
    on this sale order line.
    """

    product_updatable: bool
    """Whether or not the product can be edited on this sale order line."""

    qty_invoiced: float
    """The product quantity that has already been invoiced."""

    qty_to_invoice: float
    """The product quantity that still needs to be invoiced."""

    @property
    def salesman_id(self) -> int:
        """The ID for the salesperson partner assigned
        to this sale order line.
        """
        return self._get_ref_id("salesman_id")

    @property
    def salesman_name(self) -> str:
        """The name of the salesperson partner assigned
        to this sale order line.
        """
        return self._get_ref_name("salesman_id")

    @cached_property
    def salesman(self) -> partner.Partner:
        """The salesperson partner assigned
        to this sale order line.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.partners.get(self.salesman_id)

    state: Literal["draft", "sale", "done", "cancel"]
    """State of the sale order.

    Values:

    * ``draft`` - Draft sale order (quotation), can still be modified
    * ``sale`` - Finalised sale order, cannot be modified
    * ``done`` - Finalised and settled sale order, cannot be modified
    * ``cancel`` - Cancelled sale order, can be deleted
    """

    @property
    def tax_id(self) -> int:
        """The ID for the tax used on this sale order line."""
        return self._get_ref_id("tax_id")

    @property
    def tax_name(self) -> str:
        """The name of the tax used on this sale order line."""
        return self._get_ref_name("tax_id")

    @cached_property
    def tax(self) -> tax_module.Tax:
        """The tax used on this sale order line.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.taxes.get(self.tax_id)

    untaxed_amount_invoiced: float
    """The balance, excluding tax, on the sale order line that
    has already been invoiced.
    """

    untaxed_amount_to_invoice: float
    """The balance, excluding tax, on the sale order line that
    still needs to be invoiced.
    """

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "company": "company_id",
        "currency": "currency_id",
        "os_project_id": "os_project",
        "invoice_line_ids": "invoice_lines",
        "order": "order_id",
        "order_partner": "order_partner_id",
        "product": "product_id",
        "product_uom_id": "product_uom",
        "salesman": "salesman_id",
        "tax": "tax_id",
    }


class SaleOrderLineManager(
    record_manager_base.RecordManagerBase[SaleOrderLine],
):
    env_name = "sale.order.line"
    record_class = SaleOrderLine
