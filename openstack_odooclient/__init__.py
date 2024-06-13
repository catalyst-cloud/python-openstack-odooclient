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

from .client import Client
from .exceptions import (
    ClientError,
    MultipleRecordsFoundError,
    RecordNotFoundError,
)
from .managers.account_move import AccountMove
from .managers.account_move_line import AccountMoveLine
from .managers.company import Company
from .managers.credit import Credit
from .managers.credit_transaction import CreditTransaction
from .managers.credit_type import CreditType
from .managers.currency import Currency
from .managers.customer_group import CustomerGroup
from .managers.grant import Grant
from .managers.grant_type import GrantType
from .managers.partner import Partner
from .managers.partner_category import PartnerCategory
from .managers.pricelist import Pricelist
from .managers.product import Product
from .managers.product_category import ProductCategory
from .managers.project import Project
from .managers.project_contact import ProjectContact
from .managers.record_base import RecordBase
from .managers.record_manager_base import RecordManagerBase
from .managers.record_manager_code_base import CodedRecordManagerBase
from .managers.record_manager_name_base import NamedRecordManagerBase
from .managers.record_manager_unique_field_base import (
    RecordManagerWithUniqueFieldBase,
)
from .managers.referral_code import ReferralCode
from .managers.reseller import Reseller
from .managers.reseller_tier import ResellerTier
from .managers.sale_order import SaleOrder
from .managers.sale_order_line import SaleOrderLine
from .managers.support_subscription import SupportSubscription
from .managers.support_subscription_type import SupportSubscriptionType
from .managers.tax import Tax
from .managers.tax_group import TaxGroup
from .managers.term_discount import TermDiscount
from .managers.trial import Trial
from .managers.uom import Uom
from .managers.uom_category import UomCategory
from .managers.user import User
from .managers.util import FieldAlias, ModelRef
from .managers.volume_discount_range import VolumeDiscountRange
from .managers.voucher_code import VoucherCode

__all__ = [
    "Client",
    "ClientError",
    "MultipleRecordsFoundError",
    "RecordNotFoundError",
    "AccountMove",
    "AccountMoveLine",
    "Company",
    "Credit",
    "CreditTransaction",
    "CreditType",
    "Currency",
    "CustomerGroup",
    "Grant",
    "GrantType",
    "Partner",
    "PartnerCategory",
    "Pricelist",
    "Product",
    "ProductCategory",
    "Project",
    "ProjectContact",
    "RecordBase",
    "RecordManagerBase",
    "CodedRecordManagerBase",
    "NamedRecordManagerBase",
    "RecordManagerWithUniqueFieldBase",
    "ReferralCode",
    "Reseller",
    "ResellerTier",
    "SaleOrder",
    "SaleOrderLine",
    "SupportSubscription",
    "SupportSubscriptionType",
    "Tax",
    "TaxGroup",
    "TermDiscount",
    "Trial",
    "Uom",
    "UomCategory",
    "User",
    "FieldAlias",
    "ModelRef",
    "VolumeDiscountRange",
    "VoucherCode",
]
