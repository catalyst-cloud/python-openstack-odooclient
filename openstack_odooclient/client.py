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

import ssl
import urllib.request

from pathlib import Path
from typing import TYPE_CHECKING, overload

from odoorpc import ODOO  # type: ignore[import]
from packaging.version import Version

from .base import record
from .managers import (
    account_move,
    account_move_line,
    company,
    credit,
    credit_transaction,
    credit_type,
    currency,
    customer_group,
    grant,
    grant_type,
    partner,
    partner_category,
    pricelist,
    product,
    product_category,
    project,
    project_contact,
    referral_code,
    reseller,
    reseller_tier,
    sale_order,
    sale_order_line,
    support_subscription,
    support_subscription_type,
    tax,
    tax_group,
    term_discount,
    trial,
    uom,
    uom_category,
    user,
    volume_discount_range,
    voucher_code,
)

if TYPE_CHECKING:
    from typing import Dict, Literal, Optional, Type, Union

    from odoorpc.db import DB  # type: ignore[import]
    from odoorpc.env import Environment  # type: ignore[import]
    from odoorpc.report import Report  # type: ignore[import]

    from .managers import record_manager_base


class Client:
    """A client class for managing the OpenStack Odoo ERP.

    Connect to an Odoo server by either passing the required
    connection and authentication information,
    or passing in a pre-existing OdooRPC ``ODOO`` object.

    When connecting to an Odoo server using SSL, set ``protocol``
    to ``jsonrpc+ssl``. SSL certificate verification can be disabled
    by setting ``verify`` to ``False``. If a custom CA certificate
    is required to verify the Odoo server's host certificate,
    this can be configured by passing the certificate path to ``verify``.

    All parameters must be specified as keyword arguments.

    :param hostname: Server hostname, required if ``odoo`` is not set
    :type hostname: Optional[str], optional
    :param database: Database name, required if ``odoo`` is not set
    :type database: Optional[str], optional
    :param username: Username, required if ``odoo`` is not set
    :type username: Optional[str], optional
    :param password: Password (or API key), required if ``odoo`` is not set
    :type password: Optional[str], optional
    :param protocol: Communication protocol, defaults to ``jsonrpc``
    :type protocol: str, optional
    :param port: Access port, defaults to ``8069``
    :type port: int, optional
    :param verify: Configure SSL cert verification, defaults to ``True``
    :type verify: Union[bool, Path, str]
    :param version: Server version, defaults to ``None`` (auto-detect)
    :type version: Optional[str], optional
    """

    # TODO(callumdickinson): Use type hints to define managers,
    # to allow for easy expansion of the Odoo client class.

    @overload
    def __init__(
        self,
        *,
        hostname: Optional[str] = ...,
        database: Optional[str] = ...,
        username: Optional[str] = ...,
        password: Optional[str] = ...,
        protocol: str = "jsonrpc",
        port: int = 8069,
        verify: Union[bool, Path, str] = ...,
        version: Optional[str] = ...,
        odoo: ODOO,
    ) -> None: ...

    @overload
    def __init__(
        self,
        *,
        hostname: str,
        database: str,
        username: str,
        password: str,
        protocol: str = "jsonrpc",
        port: int = 8069,
        verify: Union[bool, Path, str] = ...,
        version: Optional[str] = ...,
        odoo: Literal[None] = ...,
    ) -> None: ...

    @overload
    def __init__(
        self,
        *,
        hostname: Optional[str] = ...,
        database: Optional[str] = ...,
        username: Optional[str] = ...,
        password: Optional[str] = ...,
        protocol: str = "jsonrpc",
        port: int = 8069,
        verify: Union[bool, Path, str] = ...,
        version: Optional[str] = ...,
        odoo: Optional[ODOO] = ...,
    ) -> None: ...

    def __init__(
        self,
        *,
        hostname: Optional[str] = None,
        database: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        protocol: str = "jsonrpc",
        port: int = 8069,
        verify: Union[bool, Path, str] = True,
        version: Optional[str] = None,
        odoo: Optional[ODOO] = None,
    ) -> None:
        # If an OdooRPC object is provided, use that directly.
        # Otherwise, make a new one with the provided settings.
        if odoo:
            self._odoo = odoo
        else:
            opener = None
            if protocol.endswith("+ssl"):
                ssl_verify = verify is not False
                ssl_cafile = (
                    str(verify) if isinstance(verify, (Path, str)) else None
                )
                if not ssl_verify or ssl_cafile:
                    ssl_context = ssl.create_default_context(cafile=ssl_cafile)
                    if not ssl_verify:
                        ssl_context.check_hostname = False
                        ssl_context.verify_mode = ssl.CERT_NONE
                    opener = urllib.request.build_opener(
                        urllib.request.HTTPSHandler(context=ssl_context),
                        urllib.request.HTTPCookieProcessor(),
                    )
            self._odoo = ODOO(
                protocol=protocol,
                host=hostname,
                port=port,
                version=version,
                opener=opener,
            )
            self._odoo.login(database, username, password)
        # Create an internal mapping between record classes and their managers.
        # This is populated by the manager classes themselves when created,
        # and used when converting model references on record objects into
        # # new record objects.
        self._record_manager_mapping: Dict[
            Type[record.RecordBase],
            record_manager_base.RecordManagerBase,
        ] = {}
        # Create record managers.
        self.account_moves = account_move.AccountMoveManager(self)
        """Account Move (Invoice) manager."""
        self.account_move_lines = account_move_line.AccountMoveLineManager(
            self,
        )
        """Company manager."""
        self.companies = company.CompanyManager(self)
        """Account Move (Invoice) Line manager."""
        self.credits = credit.CreditManager(self)
        """Credit manager."""
        self.credit_transactions = credit_transaction.CreditTransactionManager(
            self
        )
        """Credit Transaction manager."""
        self.credit_types = credit_type.CreditTypeManager(self)
        """Credit Type manager."""
        self.currencies = currency.CurrencyManager(self)
        """Currency manager."""
        self.customer_groups = customer_group.CustomerGroupManager(self)
        """Customer Group manager."""
        self.grants = grant.GrantManager(self)
        """Grant manager."""
        self.grant_types = grant_type.GrantTypeManager(self)
        """Grant Type manager."""
        self.partners = partner.PartnerManager(self)
        """Partner manager."""
        self.partner_categories = partner_category.PartnerCategoryManager(
            self,
        )
        """Partner Category manager."""
        self.pricelists = pricelist.PricelistManager(self)
        """Pricelist manager."""
        self.products = product.ProductManager(self)
        """Product manager."""
        self.product_categories = product_category.ProductCategoryManager(
            self,
        )
        """Product Category manager."""
        self.projects = project.ProjectManager(self)
        """OpenStack Project manager."""
        self.project_contacts = project_contact.ProjectContactManager(self)
        """Project Contact manager."""
        self.referral_codes = referral_code.ReferralCodeManager(self)
        """Referral Code manager."""
        self.resellers = reseller.ResellerManager(self)
        """Reseller manager."""
        self.reseller_tiers = reseller_tier.ResellerTierManager(self)
        """Reseller Tier manager."""
        self.sale_orders = sale_order.SaleOrderManager(self)
        """Sale Order manager."""
        self.sale_order_lines = sale_order_line.SaleOrderLineManager(self)
        """Sale Order Line manager."""
        self.support_subscriptions = (
            support_subscription.SupportSubscriptionManager(self)
        )
        """Support Subscription manager."""
        self.support_subscription_types = (
            support_subscription_type.SupportSubscriptionTypeManager(self)
        )
        self.taxes = tax.TaxManager(self)
        """Tax manager."""
        self.tax_groups = tax_group.TaxGroupManager(self)
        """Tax Group manager."""
        """Support Subscription Type manager."""
        self.term_discounts = term_discount.TermDiscountManager(self)
        """Term Discount manager."""
        self.trials = trial.TrialManager(self)
        """Trial manager."""
        self.uoms = uom.UomManager(self)
        """Unit of Measure (UoM) manager."""
        self.uom_categories = uom_category.UomCategoryManager(self)
        """Unit of Measure (UoM) Category manager."""
        self.users = user.UserManager(self)
        """User manager."""
        self.volume_discount_ranges = (
            volume_discount_range.VolumeDiscountRangeManager(self)
        )
        """Volume Discount Range manager."""
        self.voucher_codes = voucher_code.VoucherCodeManager(self)
        """Voucher Code manager."""

    @property
    def db(self) -> DB:
        """The database management service."""
        return self._odoo.db

    @property
    def report(self) -> Report:
        """The report management service."""
        return self._odoo.report

    @property
    def env(self) -> Environment:
        """The OdooRPC environment wrapper object.

        This allows interacting with models that do not have managers
        within this Odoo client.
        Usage is the same as on a native ``odoorpc.ODOO`` object.
        """
        return self._odoo.env

    @property
    def user_id(self) -> int:
        """The ID for the currently logged in user."""
        return self._odoo.env.uid

    @property
    def user(self) -> user.User:
        """The currently logged in user."""
        return self.users.get(self.user_id)

    @property
    def version(self) -> Version:
        """The version of the server,
        as a comparable ``packaging.version.Version`` object.
        """
        return Version(self._odoo.version)

    @property
    def version_str(self) -> str:
        """The version of the server, as a string."""
        return self._odoo.version
