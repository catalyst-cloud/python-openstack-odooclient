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
from typing import TYPE_CHECKING, List, Optional

from . import record

if TYPE_CHECKING:
    from . import partner, pricelist as pricelist_module


class CustomerGroup(record.RecordBase):
    name: str
    """The name of the customer group."""

    @property
    def partner_ids(self) -> List[int]:
        """A list of IDs for the partners that are part
        of this customer group.
        """
        return self._get_field("partners")

    @cached_property
    def partners(self) -> List[partner.Partner]:
        """The partners that are part of this customer group.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.partners.list(self.partner_ids)

    @property
    def pricelist_id(self) -> Optional[int]:
        """The ID for the pricelist this customer group uses,
        if not the default one.
        """
        return self._get_ref_id("pricelist", optional=True)

    @property
    def pricelist_name(self) -> Optional[str]:
        """The name of the pricelist this customer group uses,
        if not the default one.
        """
        return self._get_ref_name("pricelist", optional=True)

    @cached_property
    def pricelist(self) -> Optional[pricelist_module.Pricelist]:
        """The pricelist this customer group uses, if not the default one.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.pricelist_id
        return (
            self._client.pricelists.get(record_id)
            if record_id is not None
            else None
        )

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "partner_ids": "partners",
        "pricelist_id": "pricelist",
    }


class CustomerGroupManager(record.NamedRecordManagerBase[CustomerGroup]):
    env_name = "openstack.customer_group"
    record_class = CustomerGroup
