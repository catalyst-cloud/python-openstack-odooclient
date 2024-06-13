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
from typing import TYPE_CHECKING, Literal

from . import record_base, record_manager_base

if TYPE_CHECKING:
    from . import uom_category


class Uom(record_base.RecordBase):
    active: bool
    """Whether or not this Unit of Measure is active (enabled)."""

    @property
    def category_id(self) -> int:
        """The ID for the category this Unit of Measure is classified as."""
        return self._get_ref_id("category_id")

    @property
    def category_name(self) -> str:
        """The name of the category this Unit of Measure is classified as."""
        return self._get_ref_name("category_id")

    @cached_property
    def category(self) -> uom_category.UomCategory:
        """The category this Unit of Measure is classified as.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.uom_categories.get(self.category_id)

    factor: float
    """How much bigger or smaller this unit is compared to the reference
    Unit of Measure (UoM) for the classified category.
    """

    factor_inv: float
    """How many times this Unit of Measure is bigger than the reference
    Unit of Measure (UoM) for the classified category.
    """

    measure_type: Literal[
        "unit",
        "weight",
        "working_time",
        "length",
        "volume",
    ]
    """The type of category this Unit of Measure (UoM) is classified as.

    This field no longer exists from Odoo 14 onwards.

    Values:

    * ``unit`` - Default Units
    * ``weight`` - Default Weight
    * ``working_time`` - Default Working Time
    * ``length`` - Default Length
    * ``volume`` - Default Volume
    """

    name: str
    """Unit of Measure (UoM) name."""

    uom_type: Literal["bigger", "reference", "smaller"]
    """The type of the Unit of Measure (UoM).
    This determines its relationship with other UoMs in the same category.

    Values:

    * ``bigger`` - Bigger than the reference Unit of Measure
    * ``reference`` - Reference Unit of Measure for the selected category
    * ``smaller`` - Smaller than the reference Unit of Measure
    """

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "category": "category_id",
    }


class UomManager(record_manager_base.RecordManagerBase[Uom]):
    env_name = "uom.uom"
    record_class = Uom
