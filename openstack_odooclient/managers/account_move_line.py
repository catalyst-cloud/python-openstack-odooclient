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
from typing import TYPE_CHECKING, Literal, Optional, Union

from . import record

if TYPE_CHECKING:
    from . import (
        currency as currency_module,
        product as product_module,
        project,
    )


class AccountMoveLine(record.RecordBase):
    @property
    def currency_id(self) -> int:
        """The ID for the currency used in this
        account move (invoice) line.
        """
        return self._get_ref_id("currency_id")

    @property
    def currency_name(self) -> str:
        """The name of the currency used in this
        account move (invoice) line.
        """
        return self._get_ref_name("currency_id")

    @cached_property
    def currency(self) -> currency_module.Currency:
        """The currency used in this
        account move (invoice) line.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.currencies.get(self.currency_id)

    line_tax_amount: float
    """Amount charged in tax on the account move (invoice) line."""

    name: str
    """Name of the product charged on the account move (invoice) line."""

    @property
    def os_project_id(self) -> Optional[int]:
        """The ID for the OpenStack project this account move (invoice) line
        was generated for.
        """
        return self._get_ref_id("os_project", optional=True)

    @property
    def os_project_name(self) -> Optional[str]:
        """The name of the OpenStack project this account move (invoice) line
        was generated for.
        """
        return self._get_ref_name("os_project", optional=True)

    @cached_property
    def os_project(self) -> Optional[project.Project]:
        """The OpenStack project this account move (invoice) line
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
    """The OpenStack region the account move (invoice) line
    was created from.
    """

    os_resource_id: Union[str, Literal[False]]
    """The OpenStack resource ID for the resource that generated
    this account move (invoice) line.
    """

    os_resource_name: Union[str, Literal[False]]
    """The name of the OpenStack resource tier or flavour,
    as used by services such as Distil for rating purposes.

    For example, if this is the account move (invoice) line
    for a compute instance, this would be set to the instance's flavour name.
    """

    os_resource_type: Union[str, Literal[False]]
    """A human-readable description of the type of resource captured
    by this account move (invoice) line.
    """

    price_subtotal: float
    """Amount charged for the product (untaxed) on the
    account move (invoice) line.
    """

    price_unit: float
    """Unit price for the product used on the account move (invoice) line."""

    @property
    def product_id(self) -> int:
        """The ID for the product charged on the
        account move (invoice) line.
        """
        return self._get_ref_id("product_id")

    @property
    def product_name(self) -> str:
        """The name of the product charged on the
        account move (invoice) line.
        """
        return self._get_ref_name("product_id")

    @cached_property
    def product(self) -> product_module.Product:
        """The product charged on the
        account move (invoice) line.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.products.get(self.product_id)

    quantity: float
    """Quantity of product charged on the account move (invoice) line."""

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "currency": "currency_id",
        "os_project_id": "os_project",
        "product": "product_id",
    }


class AccountMoveLineManager(record.RecordManagerBase[AccountMoveLine]):
    env_name = "account.move.line"
    record_class = AccountMoveLine
