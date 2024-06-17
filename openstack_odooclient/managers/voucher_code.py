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
from typing import List, Literal, Optional, Union

from typing_extensions import Annotated

from ..base.record import ModelRef, RecordBase
from ..base.record_manager_named import NamedRecordManagerBase


class VoucherCode(RecordBase):
    claimed: bool
    """Whether or not this voucher code has been claimed."""

    code: str
    """The code string for this voucher code."""

    credit_amount: float
    """The initial credit balance for the voucher code, if a credit is to be
    created by the voucher code.
    """

    credit_type_id: Annotated[
        Optional[int],
        ModelRef("credit_type", CreditType),
    ]
    """The ID of the credit type to use, if a credit is to be
    created by this voucher code.
    """

    credit_type_name: Annotated[
        Optional[str],
        ModelRef("credit_type", CreditType),
    ]
    """The name of the credit type to use, if a credit is to be
    created by this voucher code.
    """

    credit_type: Annotated[
        Optional[CreditType],
        ModelRef("credit_type", CreditType),
    ]
    """The credit type to use, if a credit is to be
    created by this voucher code.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    credit_duration: int
    """The duration of the credit, in days, if a credit is to be
    created by the voucher code.
    """

    customer_group_id: Annotated[
        Optional[int],
        ModelRef("customer_group", CustomerGroup),
    ]
    """The ID of the customer group this voucher code is available to.

    If not set, the voucher code is available to all customers.
    """

    customer_group_name: Annotated[
        Optional[str],
        ModelRef("customer_group", CustomerGroup),
    ]
    """The name of the customer group this voucher code is available to.

    If not set, the voucher code is available to all customers.
    """

    customer_group: Annotated[
        Optional[CustomerGroup],
        ModelRef("customer_group", CustomerGroup),
    ]
    """The customer group this voucher code is available to.

    If not set, the voucher code is available to all customers.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    expiry_date: date
    """The date the voucher code expires."""

    grant_amount: float
    """The value of the grant, if a grant is to be
    created by the voucher code.
    """

    grant_type_id: Annotated[Optional[int], ModelRef("grant_type", GrantType)]
    """The ID of the grant type to use, if a grant is to be
    created by this voucher code.
    """

    grant_type_name: Annotated[
        Optional[str],
        ModelRef("grant_type", GrantType),
    ]
    """The name of the grant type to use, if a grant is to be
    created by this voucher code.
    """

    grant_type: Annotated[
        Optional[GrantType],
        ModelRef("grant_type", GrantType),
    ]
    """The grant type to use, if a grant is to be
    created by this voucher code.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    grant_duration: int
    """The duration of the grant, in days, if a grant is to be
    created by the voucher code.
    """

    multi_use: bool
    """Whether or not this is a multi-use voucher code.

    A multi-use voucher code can be used an unlimited number of times
    until it expires.
    """

    name: str
    """The unique name of this voucher code.

    This uses the code specified in the record as-is.
    """

    quota: Union[str, Literal[False]]
    """The quota size to set for new projects signed up
    using this voucher code.

    If unset, use the default quota size.
    """

    sales_person_id: Annotated[
        Optional[int],
        ModelRef("sales_person", Partner),
    ]
    """The ID for the salesperson partner responsible for this
    voucher code, if assigned.
    """

    sales_person_name: Annotated[
        Optional[str],
        ModelRef("sales_person", Partner),
    ]
    """The name of the salesperson partner responsible for this
    voucher code, if assigned.
    """

    sales_person: Annotated[
        Optional[Partner],
        ModelRef("sales_person", Partner),
    ]
    """The salesperson partner responsible for this
    voucher code, if assigned.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    tag_ids: Annotated[List[int], ModelRef("tags", PartnerCategory)]
    """A list of IDs for the tags (partner categories) to assign
    to partners for new accounts that signed up using this voucher code.
    """

    tags: Annotated[List[PartnerCategory], ModelRef("tags", PartnerCategory)]
    """The list of tags (partner categories) to assign
    to partners for new accounts that signed up using this voucher code.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """


class VoucherCodeManager(NamedRecordManagerBase[VoucherCode]):
    env_name = "openstack.voucher_code"
    record_class = VoucherCode


# NOTE(callumdickinson): Import here to avoid circular imports.
from .credit_type import CreditType  # noqa: E402
from .customer_group import CustomerGroup  # noqa: E402
from .grant_type import GrantType  # noqa: E402
from .partner import Partner  # noqa: E402
from .partner_category import PartnerCategory  # noqa: E402
