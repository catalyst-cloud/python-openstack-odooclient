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

from .base.client import ClientBase
from .managers.account_move import AccountMoveManager
from .managers.account_move_line import AccountMoveLineManager
from .managers.attachment import AttachmentManager
from .managers.company import CompanyManager
from .managers.credit import CreditManager
from .managers.credit_transaction import CreditTransactionManager
from .managers.credit_type import CreditTypeManager
from .managers.currency import CurrencyManager
from .managers.customer_group import CustomerGroupManager
from .managers.grant import GrantManager
from .managers.grant_type import GrantTypeManager
from .managers.partner import PartnerManager
from .managers.partner_category import PartnerCategoryManager
from .managers.pricelist import PricelistManager
from .managers.product import ProductManager
from .managers.product_category import ProductCategoryManager
from .managers.project import ProjectManager
from .managers.project_contact import ProjectContactManager
from .managers.referral_code import ReferralCodeManager
from .managers.reseller import ResellerManager
from .managers.reseller_tier import ResellerTierManager
from .managers.sale_order import SaleOrderManager
from .managers.sale_order_line import SaleOrderLineManager
from .managers.support_subscription import SupportSubscriptionManager
from .managers.support_subscription_type import SupportSubscriptionTypeManager
from .managers.tax import TaxManager
from .managers.tax_group import TaxGroupManager
from .managers.term_discount import TermDiscountManager
from .managers.trial import TrialManager
from .managers.uom import UomManager
from .managers.uom_category import UomCategoryManager
from .managers.user import User, UserManager
from .managers.volume_discount_range import VolumeDiscountRangeManager
from .managers.voucher_code import VoucherCodeManager


class Client(ClientBase):
    """A client for managing the OpenStack Odoo ERP.

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
    :type hostname: str | None, optional
    :param database: Database name, required if ``odoo`` is not set
    :type database: str | None, optional
    :param username: Username, required if ``odoo`` is not set
    :type username: str | None, optional
    :param password: Password (or API key), required if ``odoo`` is not set
    :type password: str | None, optional
    :param protocol: Communication protocol, defaults to ``jsonrpc``
    :type protocol: str, optional
    :param port: Access port, defaults to ``8069``
    :type port: int, optional
    :param verify: Configure SSL cert verification, defaults to ``True``
    :type verify: bool | str | Path
    :param version: Server version, defaults to ``None`` (auto-detect)
    :type version: str | None, optional
    """

    account_moves: AccountMoveManager
    """Account move (invoice) manager."""

    account_move_lines: AccountMoveLineManager
    """Account move (invoice) line manager."""

    attachments: AttachmentManager
    """Attachment manager."""

    companies: CompanyManager
    """Company manager."""

    credits: CreditManager
    """OpenStack credit manager."""

    credit_transactions: CreditTransactionManager
    """OpenStack credit transaction manager."""

    credit_types: CreditTypeManager
    """OpenStack credit type manager."""

    currencies: CurrencyManager
    """Currency manager."""

    customer_groups: CustomerGroupManager
    """OpenStack customer group manager."""

    grants: GrantManager
    """OpenStack grant manager."""

    grant_types: GrantTypeManager
    """OpenStack grant type manager."""

    partners: PartnerManager
    """Partner manager."""

    partner_categories: PartnerCategoryManager
    """Partner category manager."""

    pricelists: PricelistManager
    """Pricelist manager."""

    products: ProductManager
    """Product manager."""

    product_categories: ProductCategoryManager
    """Product category manager."""

    projects: ProjectManager
    """OpenStack project manager."""

    project_contacts: ProjectContactManager
    """OpenStack project contact manager."""

    referral_codes: ReferralCodeManager
    """OpenStack referral code manager."""

    resellers: ResellerManager
    """OpenStack reseller manager."""

    reseller_tiers: ResellerTierManager
    """OpenStack reseller tier manager."""

    sale_orders: SaleOrderManager
    """Sale order manager."""

    sale_order_lines: SaleOrderLineManager
    """Sale order line manager."""

    support_subscriptions: SupportSubscriptionManager
    """OpenStack support subscription manager."""

    support_subscription_types: SupportSubscriptionTypeManager
    """OpenStack support subscription type manager."""

    taxes: TaxManager
    """Tax manager."""

    tax_groups: TaxGroupManager
    """Tax Group manager."""

    term_discounts: TermDiscountManager
    """OpenStack term discount manager."""

    trials: TrialManager
    """OpenStack trial manager."""

    uoms: UomManager
    """Unit of Measure (UoM) manager."""

    uom_categories: UomCategoryManager
    """Unit of Measure (UoM) category manager."""

    users: UserManager
    """User manager."""

    volume_discount_ranges: VolumeDiscountRangeManager
    """OpenStack volume discount range manager."""

    voucher_codes: VoucherCodeManager
    """Voucher code manager."""

    @property
    def user(self) -> User:
        """The currently logged in user.

        This fetches the full record from Odoo.
        """
        return self.users.get(self.user_id)
