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
from .base.record import FieldAlias, ModelRef, RecordBase
from .base.record_manager import RecordManagerBase
from .base.record_manager_coded import CodedRecordManagerBase
from .base.record_manager_named import NamedRecordManagerBase
from .base.record_manager_with_unique_field import (
    RecordManagerWithUniqueFieldBase,
)
from .client import Client
from .exceptions import (
    ClientError,
    MultipleRecordsFoundError,
    RecordNotFoundError,
)
from .managers.account_move import AccountMove, AccountMoveManager
from .managers.account_move_line import (
    AccountMoveLine,
    AccountMoveLineManager,
)
from .managers.company import Company, CompanyManager
from .managers.credit import Credit, CreditManager
from .managers.credit_transaction import (
    CreditTransaction,
    CreditTransactionManager,
)
from .managers.credit_type import CreditType, CreditTypeManager
from .managers.currency import Currency, CurrencyManager
from .managers.customer_group import CustomerGroup, CustomerGroupManager
from .managers.grant import Grant, GrantManager
from .managers.grant_type import GrantType, GrantTypeManager
from .managers.partner import Partner, PartnerManager
from .managers.partner_category import PartnerCategory, PartnerCategoryManager
from .managers.pricelist import Pricelist, PricelistManager
from .managers.product import Product, ProductManager
from .managers.product_category import ProductCategory, ProductCategoryManager
from .managers.project import Project, ProjectManager
from .managers.project_contact import ProjectContact, ProjectContactManager
from .managers.referral_code import ReferralCode, ReferralCodeManager
from .managers.reseller import Reseller, ResellerManager
from .managers.reseller_tier import ResellerTier, ResellerTierManager
from .managers.sale_order import SaleOrder, SaleOrderManager
from .managers.sale_order_line import SaleOrderLine, SaleOrderLineManager
from .managers.support_subscription import (
    SupportSubscription,
    SupportSubscriptionManager,
)
from .managers.support_subscription_type import (
    SupportSubscriptionType,
    SupportSubscriptionTypeManager,
)
from .managers.tax import Tax, TaxManager
from .managers.tax_group import TaxGroup, TaxGroupManager
from .managers.term_discount import TermDiscount, TermDiscountManager
from .managers.trial import Trial, TrialManager
from .managers.uom import Uom, UomManager
from .managers.uom_category import UomCategory, UomCategoryManager
from .managers.user import User, UserManager
from .managers.volume_discount_range import (
    VolumeDiscountRange,
    VolumeDiscountRangeManager,
)
from .managers.voucher_code import VoucherCode, VoucherCodeManager

__all__ = [
    "ClientBase",
    "RecordBase",
    "FieldAlias",
    "ModelRef",
    "RecordManagerBase",
    "CodedRecordManagerBase",
    "NamedRecordManagerBase",
    "RecordManagerWithUniqueFieldBase",
    "Client",
    "AccountMove",
    "AccountMoveManager",
    "AccountMoveLine",
    "AccountMoveLineManager",
    "Company",
    "CompanyManager",
    "Credit",
    "CreditManager",
    "CreditTransaction",
    "CreditTransactionManager",
    "CreditType",
    "CreditTypeManager",
    "Currency",
    "CurrencyManager",
    "CustomerGroup",
    "CustomerGroupManager",
    "Grant",
    "GrantManager",
    "GrantType",
    "GrantTypeManager",
    "Partner",
    "PartnerManager",
    "PartnerCategory",
    "PartnerCategoryManager",
    "Pricelist",
    "PricelistManager",
    "Product",
    "ProductManager",
    "ProductCategory",
    "ProductCategoryManager",
    "Project",
    "ProjectManager",
    "ProjectContact",
    "ProjectContactManager",
    "ReferralCode",
    "ReferralCodeManager",
    "Reseller",
    "ResellerManager",
    "ResellerTier",
    "ResellerTierManager",
    "SaleOrder",
    "SaleOrderManager",
    "SaleOrderLine",
    "SaleOrderLineManager",
    "SupportSubscription",
    "SupportSubscriptionManager",
    "SupportSubscriptionType",
    "SupportSubscriptionTypeManager",
    "Tax",
    "TaxManager",
    "TaxGroup",
    "TaxGroupManager",
    "TermDiscount",
    "TermDiscountManager",
    "Trial",
    "TrialManager",
    "Uom",
    "UomManager",
    "UomCategory",
    "UomCategoryManager",
    "User",
    "UserManager",
    "VolumeDiscountRange",
    "VolumeDiscountRangeManager",
    "VoucherCode",
    "VoucherCodeManager",
    "ClientError",
    "MultipleRecordsFoundError",
    "RecordNotFoundError",
]
