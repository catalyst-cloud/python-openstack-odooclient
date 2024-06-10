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
from typing import TYPE_CHECKING, Any, List, Literal, Mapping, Optional

from . import record

if TYPE_CHECKING:
    from . import (
        account_move_line,
        currency as currency_module,
        partner,
        project,
    )


class AccountMove(record.RecordBase):
    amount_total: float
    """Total (taxed) amount charged on the account move (invoice)."""

    amount_untaxed: float
    """Total (untaxed) amount charged on the account move (invoice)."""

    @property
    def attention_id(self) -> Optional[int]:
        """The ID of the partner to send invoice emails to."""
        return self._get_ref_id("attention", optional=True)

    @property
    def attention_name(self) -> Optional[str]:
        """The name of the partner to send invoice emails to."""
        return self._get_ref_name("attention", optional=True)

    @cached_property
    def attention(self) -> Optional[partner.Partner]:
        """The partner to send invoice emails to.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.attention_id
        return (
            self._client.partners.get(record_id)
            if record_id is not None
            else None
        )

    @property
    def currency_id(self) -> int:
        """The ID for the currency used in this account move (invoice)."""
        return self._get_ref_id("currency_id")

    @property
    def currency_name(self) -> str:
        """The name of the currency used in this account move (invoice)."""
        return self._get_ref_name("currency_id")

    @cached_property
    def currency(self) -> currency_module.Currency:
        """The currency used in this account move (invoice).

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.currencies.get(self.currency_id)

    invoice_date: str
    """Date associated with the account move (invoice),
    in YYYY-MM-DD format.
    """

    invoice_line_ids: List[int]
    """The list of the IDs for the account move (invoice) lines
    that comprise this account move (invoice).
    """

    @cached_property
    def invoice_lines(self) -> List[account_move_line.AccountMoveLine]:
        """A list of account move (invoice) lines
        that comprise this account move (invoice).

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.account_move_lines.list(self.invoice_line_ids)

    is_move_sent: bool
    """Whether or not the account move (invoice) has been sent."""

    move_type: str
    """The type of account move (invoice)."""

    name: Optional[str]
    """Name assigned to the account move (invoice), if posted."""

    @property
    def os_project_id(self) -> int:
        """The ID of the OpenStack Project this Account Move (Invoice)
        was generated for.
        """
        return self._get_ref_id("os_project")

    @property
    def os_project_name(self) -> str:
        """The name of the OpenStack Project this Account Move (Invoice)
        was generated for.
        """
        return self._get_ref_name("os_project")

    @cached_property
    def os_project(self) -> project.Project:
        """The OpenStack Project this Account Move (Invoice)
        was generated for.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.projects.get(self.os_project_id)

    payment_state: str
    """The current payment state of the account move (invoice)."""

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

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "attention": "attention_id",
        "currency": "currency_id",
        "invoice_lines": "invoice_line_ids",
        "os_project_id": "os_project",
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


class AccountMoveManager(record.NamedRecordManagerBase[AccountMove]):
    env_name = "account.move"
    record_class = AccountMove
