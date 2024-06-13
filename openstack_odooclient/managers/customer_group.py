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

from typing import List, Optional

from typing_extensions import Annotated

from . import record_base, record_manager_name_base, util


class CustomerGroup(record_base.RecordBase):
    name: str
    """The name of the customer group."""

    partner_ids: Annotated[List[int], util.ModelRef("partners")]
    """A list of IDs for the partners that are part
    of this customer group.
    """

    partners: Annotated[List[partner.Partner], util.ModelRef("partners")]
    """The partners that are part of this customer group.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    pricelist_id: Annotated[Optional[int], util.ModelRef("pricelist")]
    """The ID for the pricelist this customer group uses,
    if not the default one.
    """

    pricelist_name: Annotated[Optional[str], util.ModelRef("pricelist")]
    """The name of the pricelist this customer group uses,
    if not the default one.
    """

    pricelist: Annotated[
        Optional[pricelist_module.Pricelist],
        util.ModelRef("pricelist"),
    ]
    """The pricelist this customer group uses, if not the default one.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class CustomerGroupManager(
    record_manager_name_base.NamedRecordManagerBase[CustomerGroup],
):
    env_name = "openstack.customer_group"
    record_class = CustomerGroup


# NOTE(callumdickinson): Import here to make sure circular imports work.
from . import partner, pricelist as pricelist_module  # noqa: E402
