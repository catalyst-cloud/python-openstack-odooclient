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
from typing import Annotated, Literal

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase
from ..mixins.coded_record import CodedRecordManagerMixin, CodedRecordMixin


class VoucherCode(
    RecordBase["VoucherCodeManager"],
    CodedRecordMixin["VoucherCodeManager"],
):
    claimed: bool
    """Whether or not this voucher code has been claimed."""

    credit_amount: float | Literal[False]
    """The initial credit balance for the voucher code, if a credit is to be
    created by the voucher code.
    """

    credit_type_id: Annotated[
        int | None,
        ModelRef("credit_type", CreditType),
    ]
    """The ID of the credit type to use, if a credit is to be
    created by this voucher code.
    """

    credit_type_name: Annotated[
        str | None,
        ModelRef("credit_type", CreditType),
    ]
    """The name of the credit type to use, if a credit is to be
    created by this voucher code.
    """

    credit_type: Annotated[
        CreditType | None,
        ModelRef("credit_type", CreditType),
    ]
    """The credit type to use, if a credit is to be
    created by this voucher code.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    credit_duration: int | Literal[False]
    """The duration of the credit, in days, if a credit is to be
    created by the voucher code.
    """

    customer_group_id: Annotated[
        int | None,
        ModelRef("customer_group", CustomerGroup),
    ]
    """The ID of the customer group to add the customer to, if set."""

    customer_group_name: Annotated[
        str | None,
        ModelRef("customer_group", CustomerGroup),
    ]
    """The name of the customer group to add the customer to, if set."""

    customer_group: Annotated[
        CustomerGroup | None,
        ModelRef("customer_group", CustomerGroup),
    ]
    """The customer group to add the customer to, if set.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    expiry_date: date | Literal[False]
    """The date the voucher code expires."""

    grant_duration: int | Literal[False]
    """The duration of the grant, in days, if a grant is to be
    created by the voucher code.
    """

    grant_type_id: Annotated[int | None, ModelRef("grant_type", GrantType)]
    """The ID of the grant type to use, if a grant is to be
    created by this voucher code.
    """

    grant_type_name: Annotated[
        str | None,
        ModelRef("grant_type", GrantType),
    ]
    """The name of the grant type to use, if a grant is to be
    created by this voucher code.
    """

    grant_type: Annotated[GrantType | None, ModelRef("grant_type", GrantType)]
    """The grant type to use, if a grant is to be
    created by this voucher code.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    grant_value: float | Literal[False]
    """The value of the grant, if a grant is to be
    created by the voucher code.
    """

    multi_use: bool
    """Whether or not this is a multi-use voucher code.

    A multi-use voucher code can be used an unlimited number of times
    until it expires.
    """

    name: str
    """The automatically generated name of this voucher code.

    This uses the code specified in the record as-is.
    """

    quota_size: str | Literal[False]
    """The default quota size for new projects signed up
    using this voucher code.

    If unset, use the default quota size.
    """

    sales_person_id: Annotated[
        int | None,
        ModelRef("sales_person", Partner),
    ]
    """The ID for the salesperson partner responsible for this
    voucher code, if assigned.
    """

    sales_person_name: Annotated[
        str | None,
        ModelRef("sales_person", Partner),
    ]
    """The name of the salesperson partner responsible for this
    voucher code, if assigned.
    """

    sales_person: Annotated[
        Partner | None,
        ModelRef("sales_person", Partner),
    ]
    """The salesperson partner responsible for this
    voucher code, if assigned.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    tag_ids: Annotated[list[int], ModelRef("tags", PartnerCategory)]
    """A list of IDs for the tags (partner categories) to assign
    to partners for new accounts that signed up using this voucher code.
    """

    tags: Annotated[list[PartnerCategory], ModelRef("tags", PartnerCategory)]
    """The list of tags (partner categories) to assign
    to partners for new accounts that signed up using this voucher code.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """


class VoucherCodeManager(
    RecordManagerBase[VoucherCode],
    CodedRecordManagerMixin[VoucherCode],
):
    env_name = "openstack.voucher_code"
    record_class = VoucherCode


# NOTE(callumdickinson): Import here to avoid circular imports.
from .credit_type import CreditType  # noqa: E402
from .customer_group import CustomerGroup  # noqa: E402
from .grant_type import GrantType  # noqa: E402
from .partner import Partner  # noqa: E402
from .partner_category import PartnerCategory  # noqa: E402
