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


class AccountMoveLine(RecordBase["AccountMoveLineManager"]):
    currency_id: Annotated[int, ModelRef("currency_id", Currency)]
    """The ID for the currency used in this
    account move (invoice) line.
    """

    currency_name: Annotated[int, ModelRef("currency_id", Currency)]
    """The name of the currency used in this
    account move (invoice) line.
    """

    currency: Annotated[Currency, ModelRef("currency_id", Currency)]
    """The currency used in this
    account move (invoice) line.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    line_tax_amount: float
    """Amount charged in tax on the account move (invoice) line."""

    move_id: Annotated[int, ModelRef("move_id", AccountMove)]
    """The ID for the account move (invoice) this line is part of."""

    move_name: Annotated[str, ModelRef("move_id", AccountMove)]
    """The name of the account move (invoice) this line is part of."""

    move: Annotated[AccountMove, ModelRef("move_id", AccountMove)]
    """The account move (invoice) this line is part of.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    name: str
    """Name of the product charged on the account move (invoice) line."""

    os_project_id: Annotated[int | None, ModelRef("os_project", Project)]
    """The ID for the OpenStack project this account move (invoice) line
    was generated for.
    """

    os_project_name: Annotated[str | None, ModelRef("os_project", Project)]
    """The name of the OpenStack project this account move (invoice) line
    was generated for.
    """

    os_project: Annotated[Project | None, ModelRef("os_project", Project)]
    """The OpenStack project this account move (invoice) line
    was generated for.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    os_region: str | Literal[False]
    """The OpenStack region the account move (invoice) line
    was created from.
    """

    os_resource_id: str | Literal[False]
    """The OpenStack resource ID for the resource that generated
    this account move (invoice) line.
    """

    os_resource_name: str | Literal[False]
    """The name of the OpenStack resource tier or flavour,
    as used by services such as Distil for rating purposes.

    For example, if this is the account move (invoice) line
    for a compute instance, this would be set to the instance's flavour name.
    """

    os_resource_type: str | Literal[False]
    """A human-readable description of the type of resource captured
    by this account move (invoice) line.
    """

    price_subtotal: float
    """Amount charged for the product (untaxed) on the
    account move (invoice) line.
    """

    price_unit: float
    """Unit price for the product used on the account move (invoice) line."""

    product_id: Annotated[int, ModelRef("product_id", Product)]
    """The ID for the product charged on the
    account move (invoice) line.
    """

    product_name: Annotated[str, ModelRef("product_id", Product)]
    """The name of the product charged on the
    account move (invoice) line.
    """

    product: Annotated[Product, ModelRef("product_id", Product)]
    """The product charged on the
    account move (invoice) line.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    quantity: float
    """Quantity of product charged on the account move (invoice) line."""


class AccountMoveLineManager(RecordManagerBase[AccountMoveLine]):
    env_name = "account.move.line"
    record_class = AccountMoveLine


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .account_move import AccountMove  # noqa: E402
from .currency import Currency  # noqa: E402
from .product import Product  # noqa: E402
from .project import Project  # noqa: E402
