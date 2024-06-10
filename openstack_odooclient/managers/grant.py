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
from typing import TYPE_CHECKING, Optional

from . import record

if TYPE_CHECKING:
    from . import (
        grant_type as grant_type_module,
        voucher_code as voucher_code_module,
    )


class Grant(record.RecordBase):
    expiry_date: date
    """The date the grant expires."""

    @property
    def grant_type_id(self) -> int:
        """The ID of the type of this grant."""
        return self._get_ref_id("grant_type")

    @property
    def grant_type_name(self) -> str:
        """The name of this type of grant."""
        return self._get_ref_name("grant_type")

    @cached_property
    def grant_type(self) -> grant_type_module.GrantType:
        """The type of this grant.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.grant_types.get(self.grant_type_id)

    name: str
    """The automatically generated name of the grant."""

    start_date: date
    """The start date of the grant."""

    value: float
    """The value of the grant."""

    @property
    def voucher_code_id(self) -> Optional[int]:
        """The ID of the voucher code used when applying for the grant,
        if one was supplied.
        """
        return self._get_ref_id("voucher_code", optional=True)

    @property
    def voucher_code_name(self) -> Optional[str]:
        """The name of the voucher code used when applying for the grant,
        if one was supplied.
        """
        return self._get_ref_name("voucher_code", optional=True)

    @cached_property
    def voucher_code(self) -> Optional[voucher_code_module.VoucherCode]:
        """Voucher code used when applying for the grant,
        if one was supplied.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.voucher_code_id
        return (
            self._client.voucher_codes.get(record_id)
            if record_id is not None
            else None
        )

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "grant_type_id": "grant_type",
        "voucher_code_id": "voucher_code",
    }


class GrantManager(record.RecordManagerBase[Grant]):
    env_name = "openstack.grant"
    record_class = Grant
