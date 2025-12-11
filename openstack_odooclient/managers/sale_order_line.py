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


class SaleOrderLine(RecordBase["SaleOrderLineManager"]):
    company_id: Annotated[int, ModelRef("company_id", Company)]
    """The ID for the company this sale order line
    was generated for.
    """

    company_name: Annotated[str, ModelRef("company_id", Company)]
    """The name of the company this sale order line
    was generated for.
    """

    company: Annotated[Company, ModelRef("company_id", Company)]
    """The company this sale order line
    was generated for.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    currency_id: Annotated[int, ModelRef("currency_id", Currency)]
    """The ID for the currency used in this sale order line."""

    currency_name: Annotated[str, ModelRef("currency_id", Currency)]
    """The name of the currency used in this sale order line."""

    currency: Annotated[Currency, ModelRef("currency_id", Currency)]
    """The currency used in this sale order line.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    discount: float
    """Discount percentage on the sale order line (0-100)."""

    display_name: str
    """Display name for the sale order line in the sale order."""

    invoice_line_ids: Annotated[
        list[int],
        ModelRef("invoice_lines", AccountMoveLine),
    ]
    """A list of IDs for the account move (invoice) lines created
    from this sale order line.
    """

    invoice_lines: Annotated[
        list[AccountMoveLine],
        ModelRef("invoice_lines", AccountMoveLine),
    ]
    """The account move (invoice) lines created
    from this sale order line.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

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

    order_id: Annotated[int, ModelRef("order_id", SaleOrder)]
    """The ID for the sale order this line is linked to."""

    order_name: Annotated[str, ModelRef("order_id", SaleOrder)]
    """The name of the sale order this line is linked to."""

    order: Annotated[SaleOrder, ModelRef("order_id", SaleOrder)]
    """The sale order this line is linked to.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    order_partner_id: Annotated[int, ModelRef("order_partner_id", Partner)]
    """The ID for the recipient partner for the sale order."""

    order_partner_name: Annotated[str, ModelRef("order_partner_id", Partner)]
    """The name of the recipient partner for the sale order."""

    order_partner: Annotated[Partner, ModelRef("order_partner_id", Partner)]
    """The recipient partner for the sale order.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    os_project_id: Annotated[int | None, ModelRef("os_project", Project)]
    """The ID for the the OpenStack project this sale order line was
    was generated for.
    """

    os_project_name: Annotated[str | None, ModelRef("os_project", Project)]
    """The name of the the OpenStack project this sale order line was
    was generated for.
    """

    os_project: Annotated[Project | None, ModelRef("os_project", Project)]
    """The OpenStack project this sale order line was
    was generated for.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    os_region: str | Literal[False]
    """The OpenStack region the sale order line was created from."""

    os_resource_id: str | Literal[False]
    """The OpenStack resource ID for the resource that generated
    this sale order line.
    """

    os_resource_name: str | Literal[False]
    """The name of the OpenStack resource tier or flavour,
    as used by services such as Distil for rating purposes.

    For example, if this is the sale order line for a compute instance,
    this would be set to the instance's flavour name.
    """

    os_resource_type: str | Literal[False]
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

    product_id: Annotated[int, ModelRef("product_id", Product)]
    """The ID of the product charged on this sale order line."""

    product_name: Annotated[str, ModelRef("product_id", Product)]
    """The name of the product charged on this sale order line."""

    product: Annotated[Product, ModelRef("product_id", Product)]
    """The product charged on this sale order line.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    product_uom_id: Annotated[int, ModelRef("product_uom", Uom)]
    """The ID for the Unit of Measure for the product being charged in
    this sale order line.
    """

    product_uom_name: Annotated[str, ModelRef("product_uom", Uom)]
    """The name of the Unit of Measure for the product being charged in
    this sale order line.
    """

    product_uom: Annotated[Uom, ModelRef("product_uom", Uom)]
    """The Unit of Measure for the product being charged in
    this sale order line.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

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

    salesman_id: Annotated[int, ModelRef("salesman_id", Partner)]
    """The ID for the salesperson partner assigned
    to this sale order line.
    """

    salesman_name: Annotated[str, ModelRef("salesman_id", Partner)]
    """The name of the salesperson partner assigned
    to this sale order line.
    """

    salesman: Annotated[Partner, ModelRef("salesman_id", Partner)]
    """The salesperson partner assigned
    to this sale order line.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    state: Literal["draft", "sale", "done", "cancel"]
    """State of the sale order.

    Values:

    * ``draft`` - Draft sale order (quotation), can still be modified
    * ``sale`` - Finalised sale order, cannot be modified
    * ``done`` - Finalised and settled sale order, cannot be modified
    * ``cancel`` - Cancelled sale order, can be deleted
    """

    tax_id: Annotated[int, ModelRef("tax_id", Tax)]
    """The ID for the tax used on this sale order line."""

    tax_name: Annotated[str, ModelRef("tax_id", Tax)]
    """The name of the tax used on this sale order line."""

    tax: Annotated[Tax, ModelRef("tax_id", Tax)]
    """The tax used on this sale order line.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    untaxed_amount_invoiced: float
    """The balance, excluding tax, on the sale order line that
    has already been invoiced.
    """

    untaxed_amount_to_invoice: float
    """The balance, excluding tax, on the sale order line that
    still needs to be invoiced.
    """


class SaleOrderLineManager(RecordManagerBase[SaleOrderLine]):
    env_name = "sale.order.line"
    record_class = SaleOrderLine


# NOTE(callumdickinson): Import here to avoid circular imports.
from .account_move_line import AccountMoveLine  # noqa: E402
from .company import Company  # noqa: E402
from .currency import Currency  # noqa: E402
from .partner import Partner  # noqa: E402
from .product import Product  # noqa: E402
from .project import Project  # noqa: E402
from .sale_order import SaleOrder  # noqa: E402
from .tax import Tax  # noqa: E402
from .uom import Uom  # noqa: E402
