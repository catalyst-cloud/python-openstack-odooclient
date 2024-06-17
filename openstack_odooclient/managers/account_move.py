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
from typing import Any, List, Literal, Mapping, Optional, Union

from typing_extensions import Annotated

from ..base.record import ModelRef, RecordBase
from ..base.record_manager_named import NamedRecordManagerBase


class AccountMove(RecordBase):
    amount_total: float
    """Total (taxed) amount charged on the account move (invoice)."""

    amount_untaxed: float
    """Total (untaxed) amount charged on the account move (invoice)."""

    currency_id: Annotated[int, ModelRef("currency_id", Currency)]
    """The ID for the currency used in this account move (invoice)."""

    currency_name: Annotated[str, ModelRef("currency_id", Currency)]
    """The name of the currency used in this account move (invoice)."""

    currency: Annotated[Currency, ModelRef("currency_id", Currency)]
    """The currency used in this account move (invoice).

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    invoice_date: date
    """Date associated with the account move (invoice)."""

    invoice_line_ids: Annotated[
        List[int],
        ModelRef("invoice_line_ids", AccountMoveLine),
    ]
    """The list of the IDs for the account move (invoice) lines
    that comprise this account move (invoice).
    """

    invoice_lines: Annotated[
        List[AccountMoveLine],
        ModelRef("invoice_line_ids", AccountMoveLine),
    ]
    """A list of account move (invoice) lines
    that comprise this account move (invoice).

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    is_move_sent: bool
    """Whether or not the account move (invoice) has been sent."""

    move_type: Literal[
        "entry",
        "out_invoice",
        "out_refund",
        "in_invoice",
        "in_refund",
        "out_receipt",
        "in_receipt",
    ]
    """The type of account move (invoice).

    Values:

    * ``entry`` - Journal Entry
    * ``out_invoice`` - Customer Invoice
    * ``out_refund`` - Customer Credit Note
    * ``in_invoice`` - Vendor Bill
    * ``in_refund`` - Vendor Credit Note
    * ``out_receipt`` - Sales Receipt
    * ``in_receipt`` - Purchase Receipt
    """

    name: Union[str, Literal[False]]
    """Name assigned to the account move (invoice), if posted."""

    os_project_id: Annotated[Optional[int], ModelRef("os_project", Project)]
    """The ID of the OpenStack project this account move (invoice)
    was generated for, if this is an invoice for OpenStack project usage.
    """

    os_project_name: Annotated[Optional[str], ModelRef("os_project", Project)]
    """The name of the OpenStack project this account move (invoice)
    was generated for, if this is an invoice for OpenStack project usage.
    """

    os_project: Annotated[Optional[Project], ModelRef("os_project", Project)]
    """The OpenStack project this account move (invoice)
    was generated for, if this is an invoice for OpenStack project usage.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    payment_state: Literal[
        "not_paid",
        "in_payment",
        "paid",
        "partial",
        "reversed",
        "invoicing_legacy",
    ]
    """
    The current payment state of the account move (invoice).

    Values:

    * ``not_paid`` - Not Paid
    * ``in_payment`` - In Payment
    * ``paid`` - Paid
    * ``partial`` - Partially Paid
    * ``reversed`` - Reversed
    * ``invoicing_legacy`` - Invoicing App Legacy
    """

    state: Literal["draft", "posted", "cancel"]
    """The current state of the account move (invoice).

    Values:

    * ``draft`` - Draft invoice
    * ``posted`` - Posted (finalised) invoice
    * ``cancel`` - Cancelled invoice
    """

    _field_mapping = {
        # Odoo version.
        "13.0": {
            # Key is local value, value is remote value.
            "move_type": "type",
            "is_move_sent": "invoice_sent",
            "payment_state": "invoice_payment_state",
        },
    }

    def action_post(self) -> None:
        """Change a draft account move (invoice) into "posted" state."""
        self._env.action_post(self.id)

    def send_openstack_invoice_email(
        self,
        email_ctx: Optional[Mapping[str, Any]] = None,
    ) -> None:
        """Send an OpenStack invoice email for this account move (invoice).

        :param email_ctx: Optional email context, defaults to None
        :type email_ctx: Optional[Mapping[str, Any]], optional
        """
        self._env.send_openstack_invoice_email(
            self.id,
            email_ctx=dict(email_ctx) if email_ctx else None,
        )


class AccountMoveManager(NamedRecordManagerBase[AccountMove]):
    env_name = "account.move"
    record_class = AccountMove


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .account_move_line import AccountMoveLine  # noqa: E402
from .currency import Currency  # noqa: E402
from .project import Project  # noqa: E402
