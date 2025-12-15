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

from typing import Annotated

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase
from ..mixins.named_record import NamedRecordManagerMixin, NamedRecordMixin


class CustomerGroup(
    RecordBase["CustomerGroupManager"],
    NamedRecordMixin["CustomerGroupManager"],
):
    partner_ids: Annotated[list[int], ModelRef("partners", Partner)]
    """A list of IDs for the partners that are part
    of this customer group.
    """

    partners: Annotated[list[Partner], ModelRef("partners", Partner)]
    """The partners that are part of this customer group.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    pricelist_id: Annotated[int | None, ModelRef("pricelist", Pricelist)]
    """The ID for the pricelist this customer group uses,
    if not the default one.
    """

    pricelist_name: Annotated[str | None, ModelRef("pricelist", Pricelist)]
    """The name of the pricelist this customer group uses,
    if not the default one.
    """

    pricelist: Annotated[Pricelist | None, ModelRef("pricelist", Pricelist)]
    """The pricelist this customer group uses, if not the default one.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class CustomerGroupManager(
    RecordManagerBase[CustomerGroup],
    NamedRecordManagerMixin[CustomerGroup],
):
    env_name = "openstack.customer_group"
    record_class = CustomerGroup


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .partner import Partner  # noqa: E402
from .pricelist import Pricelist  # noqa: E402
