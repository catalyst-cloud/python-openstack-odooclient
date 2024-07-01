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

from datetime import date, datetime
from typing import List, Literal, Optional, Union

from typing_extensions import Annotated

from ..base.record import FieldAlias, ModelRef, RecordBase
from ..base.record_manager_named import NamedRecordManagerBase


class SaleOrder(RecordBase["SaleOrderManager"]):
    amount_untaxed: float
    """The untaxed total cost of the sale order."""

    amount_tax: float
    """The amount in taxes on this sale order."""

    amount_total: float
    """The taxed total cost of the sale order."""

    client_order_ref: Union[str, Literal[False]]
    """The customer reference for this sale order, if defined."""

    currency_id: Annotated[int, ModelRef("currency_id", Currency)]
    """The ID for the currency used in this sale order."""

    currency_name: Annotated[str, ModelRef("currency_id", Currency)]
    """The name of the currency used in this sale order."""

    currency: Annotated[Currency, ModelRef("currency_id", Currency)]
    """The currency used in this sale order.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    date_order: datetime
    """The time the sale order was created."""

    display_name: str
    """The display name of the sale order."""

    invoice_status: Literal["no", "to invoice", "invoiced", "upselling"]
    """The current invoicing status of this sale order.

    Values:

    * ``no`` - Nothing to invoice
    * ``to invoice`` - Has line items that need to be invoiced
    * ``invoiced`` - Fully invoiced
    * ``upselling`` - Upselling opportunity
    """

    name: str
    """The name assigned to the sale order."""

    note: str
    """A note attached to the sale order.

    Generally used for terms and conditions.
    """

    order_line_ids: Annotated[
        List[int],
        ModelRef("order_line", SaleOrderLine),
    ]
    """A list of IDs for the lines added to the sale order."""

    order_line: Annotated[
        List[SaleOrderLine],
        ModelRef("order_line", SaleOrderLine),
    ]
    """The lines added to the sale order.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    order_lines: Annotated[List[SaleOrderLine], FieldAlias("order_line")]
    """An alias for ``order_line``."""

    os_invoice_date: date
    """The invoicing date for the invoice that is created
    from the sale order.
    """

    os_invoice_due_date: date
    """The due date for the invoice that is created
    from the sale order.
    """

    os_project_id: Annotated[Optional[int], ModelRef("os_project", Project)]
    """The ID for the the OpenStack project this sale order was
    was generated for.
    """

    os_project_name: Annotated[Optional[str], ModelRef("os_project", Project)]
    """The name of the the OpenStack project this sale order was
    was generated for.
    """

    os_project: Annotated[Optional[Project], ModelRef("os_project", Project)]
    """The OpenStack project this sale order was
    was generated for.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    partner_id: Annotated[int, ModelRef("partner_id", Partner)]
    """The ID for the recipient partner for the sale order."""

    partner_name: Annotated[str, ModelRef("partner_id", Partner)]
    """The name of the recipient partner for the sale order."""

    partner: Annotated[Partner, ModelRef("partner_id", Partner)]
    """The recipient partner for the sale order.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    state: Literal["draft", "sale", "done", "cancel"]
    """State of the sale order.

    Values:

    * ``draft`` - Draft sale order (quotation), can still be modified
    * ``sale`` - Finalised sale order, cannot be modified
    * ``done`` - Finalised and settled sale order, cannot be modified
    * ``cancel`` - Cancelled sale order, can be deleted in most cases
    """

    def action_confirm(self) -> None:
        """Confirm this sale order."""
        self._env.action_confirm(self.id)

    def create_invoices(self) -> None:
        """Create invoices from this sale order."""
        self._env.create_invoices(self.id)


class SaleOrderManager(NamedRecordManagerBase[SaleOrder]):
    env_name = "sale.order"
    record_class = SaleOrder

    def action_confirm(self, sale_order: Union[int, SaleOrder]) -> None:
        """Confirm the given sale order.

        :param sale_order: The sale order to confirm
        :type sale_order: Union[int, SaleOrder]
        """
        self._env.action_confirm(
            (
                sale_order.id
                if isinstance(sale_order, SaleOrder)
                else sale_order
            ),
        )

    def create_invoices(self, sale_order: Union[int, SaleOrder]) -> None:
        """Create invoices from the given sale order.

        :param sale_order: The sale order to create invoices from
        :type sale_order: Union[int, SaleOrder]
        """
        self._env.create_invoices(
            (
                sale_order.id
                if isinstance(sale_order, SaleOrder)
                else sale_order
            ),
        )


# NOTE(callumdickinson): Import here to avoid circular imports.
from .currency import Currency  # noqa: E402
from .partner import Partner  # noqa: E402
from .project import Project  # noqa: E402
from .sale_order_line import SaleOrderLine  # noqa: E402
