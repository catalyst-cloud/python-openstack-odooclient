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
from functools import cached_property
from typing import TYPE_CHECKING, List, Literal, Optional, Union

from . import record_base, record_manager_name_base

if TYPE_CHECKING:
    from . import (
        credit_type as credit_type_module,
        customer_group as customer_group_module,
        grant_type as grant_type_module,
        partner,
        partner_category,
    )


class VoucherCode(record_base.RecordBase):
    claimed: bool
    """Whether or not this voucher code has been claimed."""

    code: str
    """The code string for this voucher code."""

    credit_amount: float
    """The initial credit balance for the voucher code, if a credit is to be
    created by the voucher code.
    """

    @property
    def credit_type_id(self) -> Optional[int]:
        """The ID of the credit type to use, if a credit is to be
        created by this voucher code.
        """
        return self._get_ref_id("credit_type", optional=True)

    @property
    def credit_type_name(self) -> Optional[str]:
        """The name of the credit type to use, if a credit is to be
        created by this voucher code.
        """
        return self._get_ref_name("credit_type", optional=True)

    @cached_property
    def credit_type(self) -> Optional[credit_type_module.CreditType]:
        """The credit type to use, if a credit is to be
        created by this voucher code.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.credit_type_id
        return (
            self._client.credit_types.get(record_id)
            if record_id is not None
            else None
        )

    credit_duration: int
    """The duration of the credit, in days, if a credit is to be
    created by the voucher code.
    """

    @property
    def customer_group_id(self) -> Optional[int]:
        """The ID of the customer group this voucher code is available to.

        If not set, the voucher code is available to all customers.
        """
        return self._get_ref_id("customer_group", optional=True)

    @property
    def customer_group_name(self) -> Optional[str]:
        """The name of the customer group this voucher code is available to.

        If not set, the voucher code is available to all customers.
        """
        return self._get_ref_name("customer_group", optional=True)

    @cached_property
    def customer_group(self) -> Optional[customer_group_module.CustomerGroup]:
        """The customer group this voucher code is available to.

        If not set, the voucher code is available to all customers.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.customer_group_id
        return (
            self._client.customer_groups.get(record_id)
            if record_id is not None
            else None
        )

    expiry_date: date
    """The date the voucher code expires."""

    grant_amount: float
    """The value of the grant, if a grant is to be
    created by the voucher code.
    """

    @property
    def grant_type_id(self) -> Optional[int]:
        """The ID of the grant type to use, if a grant is to be
        created by this voucher code.
        """
        return self._get_ref_id("grant_type", optional=True)

    @property
    def grant_type_name(self) -> Optional[str]:
        """The name of the grant type to use, if a grant is to be
        created by this voucher code.
        """
        return self._get_ref_name("grant_type", optional=True)

    @cached_property
    def grant_type(self) -> Optional[grant_type_module.GrantType]:
        """The grant type to use, if a grant is to be
        created by this voucher code.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.grant_type_id
        return (
            self._client.grant_types.get(record_id)
            if record_id is not None
            else None
        )

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

    @property
    def sales_person_id(self) -> Optional[int]:
        """The ID for the salesperson responsible for this
        voucher code, if assigned.
        """
        return self._get_ref_id("sales_person", optional=True)

    @property
    def sales_person_name(self) -> Optional[str]:
        """The name of the salesperson responsible for this
        voucher code, if assigned.
        """
        return self._get_ref_name("sales_person", optional=True)

    @cached_property
    def sales_person(self) -> Optional[partner.Partner]:
        """The salesperson responsible for this
        voucher code, if assigned.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.sales_person_id
        return (
            self._client.partners.get(record_id)
            if record_id is not None
            else None
        )

    @property
    def tag_ids(self) -> List[int]:
        """A list of IDs for the tags (partner categories) to assign
        to partners for new accounts that signed up using this voucher code.
        """
        return self._get_field("tags")

    @cached_property
    def tags(self) -> List[partner_category.PartnerCategory]:
        """The list of tags (partner categories) to assign
        to partners for new accounts that signed up using this voucher code.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.partner_categories.list(self.tag_ids)

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "sales_person_id": "sales_person",
        "tag_ids": "tags",
    }


class VoucherCodeManager(
    record_manager_name_base.NamedRecordManagerBase[VoucherCode],
):
    env_name = "openstack.voucher_code"
    record_class = VoucherCode
