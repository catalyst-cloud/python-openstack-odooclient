# Copyright (C) 2026 Catalyst Cloud Limited
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


class FiscalPosition(RecordBase["FiscalPositionManager"]):
    active: bool
    """Whether or not this fiscal position is active (enabled)."""

    company_id: Annotated[int, ModelRef("company_id", Company)]
    """The ID for the company this fiscal position is associated with."""

    company_name: Annotated[str, ModelRef("company_id", Company)]
    """The name of the company this fiscal position is associated with."""

    company: Annotated[Company, ModelRef("company_id", Company)]
    """The company this fiscal position is associated with.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    name: str
    """The name of the fiscal position.

    Not guaranteed to be unique.
    """

    tax_ids: Annotated[
        list[int],
        ModelRef("tax_ids", FiscalPositionTaxMapping),
    ]
    """The list of IDs for the tax mappings that will be applied to
    sale orders and invoices for partners using this fiscal position.
    """

    taxes: Annotated[
        list[FiscalPositionTaxMapping],
        ModelRef("tax_ids", FiscalPositionTaxMapping),
    ]
    """The list of tax mappings that will be applied to
    sale orders and invoices for partners using this fiscal position.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """


class FiscalPositionManager(RecordManagerBase[FiscalPosition]):
    env_name = "account.fiscal.position"
    record_class = FiscalPosition


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .company import Company  # noqa: E402
from .fiscal_position_tax_mapping import FiscalPositionTaxMapping  # noqa: E402
