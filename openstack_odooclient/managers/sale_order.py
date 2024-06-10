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

from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING, List, Literal, Union

from . import record

if TYPE_CHECKING:
    from . import (
        currency as currency_module,
        partner as partner_module,
        sale_order_line,
    )


class SaleOrder(record.RecordBase):
    amount_untaxed: float
    """The untaxed total cost of the sale order."""

    amount_tax: float
    """The amount in taxes on this sale order."""

    amount_total: float
    """The taxed total cost of the sale order."""

    client_order_ref: Union[str, Literal[False]]
    """The customer reference for this sale order, if defined."""

    @property
    def currency_id(self) -> int:
        """The ID for the currency used in this sale order."""
        return self._get_ref_id("currency_id")

    @property
    def currency_name(self) -> str:
        """The name of the currency used in this sale order."""
        return self._get_ref_name("currency_id")

    @cached_property
    def currency(self) -> currency_module.Currency:
        """The currency used in this sale order.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.currencies.get(self.currency_id)

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

    @property
    def order_line_ids(self) -> List[int]:
        """A list of IDs for the lines added to the sale order."""
        return self._get_field("order_line")

    @cached_property
    def order_line(self) -> List[sale_order_line.SaleOrderLine]:
        """The lines added to the sale order.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.sale_order_lines.list(self.order_line_ids)

    @property
    def order_lines(self) -> List[sale_order_line.SaleOrderLine]:
        """An alias for ``order_line``."""
        return self.order_line

    @property
    def partner_id(self) -> int:
        """The ID for the recipient partner for the sale order."""
        return self._get_ref_id("partner_id")

    @property
    def partner_name(self) -> str:
        """The name of the recipient partner for the sale order."""
        return self._get_ref_name("partner_id")

    @cached_property
    def partner(self) -> partner_module.Partner:
        """The recipient partner for the sale order.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.partners.get(self.partner_id)

    state: Literal["draft", "sale", "done", "cancel"]
    """State of the sale order.

    Values:

    * ``draft`` - Draft sale order (quotation), can still be modified
    * ``sale`` - Finalised sale order, cannot be modified
    * ``done`` - Finalised and settled sale order, cannot be modified
    * ``cancel`` - Cancelled sale order, can be deleted
    """

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "currency": "currency_id",
        "order_line_ids": "order_line",
        "order_lines": "order_line",
        "partner": "partner_id",
    }

    def action_confirm(self) -> None:
        """Confirm the sale order."""
        self._client.sale_orders.action_confirm(self)

    def create_invoices(self) -> None:
        """Create invoices from this sale order."""
        self._client.sale_orders.create_invoices(self)


class SaleOrderManager(record.NamedRecordManagerBase[SaleOrder]):
    env_name = "sale.order"
    record_class = SaleOrder

    def action_confirm(self, sale_order: Union[int, SaleOrder]) -> None:
        """Confirm the given sale order.

        :param sale_order: Sale order to confirm
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
        """Create invoices from this sale order.

        :param sale_order: Sale order to create invoices for
        :type sale_order: Union[int, SaleOrder]
        """
        self._env.create_invoices(
            (
                sale_order.id
                if isinstance(sale_order, SaleOrder)
                else sale_order
            ),
        )
