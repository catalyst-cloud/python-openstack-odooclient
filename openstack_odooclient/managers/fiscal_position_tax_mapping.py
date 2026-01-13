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


class FiscalPositionTaxMapping(RecordBase["FiscalPositionTaxMappingManager"]):
    company_id: Annotated[int, ModelRef("company_id", Company)]
    """The ID for the company this fiscal position tax mapping
    is associated with.
    """

    company_name: Annotated[str, ModelRef("company_id", Company)]
    """The name of the company this fiscal position tax mapping
    is associated with.
    """

    company: Annotated[Company, ModelRef("company_id", Company)]
    """The company this fiscal position tax mapping
    is associated with.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    position_id: Annotated[int, ModelRef("position_id", FiscalPosition)]
    """The ID for the fiscal position this mapping is part of."""

    position_name: Annotated[str, ModelRef("position_id", FiscalPosition)]
    """The name of the fiscal position this mapping is part of."""

    position: Annotated[
        FiscalPosition,
        ModelRef("position_id", FiscalPosition),
    ]
    """The fiscal position this mapping is part of.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    tax_src_id: Annotated[int, ModelRef("tax_src_id", Tax)]
    """The ID of the tax to be overridden on products."""

    tax_src_name: Annotated[str, ModelRef("tax_src_id", Tax)]
    """The name of the tax to be overridden on products."""

    tax_src: Annotated[Tax, ModelRef("tax_src_id", Tax)]
    """The tax to be overridden on products.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    tax_dest_id: Annotated[int | None, ModelRef("tax_dest_id", Tax)]
    """The ID of the tax to override the source tax with, if set."""

    tax_dest_name: Annotated[str | None, ModelRef("tax_dest_id", Tax)]
    """The name of the tax to override the source tax with, if set."""

    tax_dest: Annotated[Tax | None, ModelRef("tax_dest_id", Tax)]
    """The tax to override the source tax with, if set.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class FiscalPositionTaxMappingManager(
    RecordManagerBase[FiscalPositionTaxMapping],
):
    env_name = "account.fiscal.position.tax"
    record_class = FiscalPositionTaxMapping


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .company import Company  # noqa: E402
from .fiscal_position import FiscalPosition  # noqa: E402
from .tax import Tax  # noqa: E402
