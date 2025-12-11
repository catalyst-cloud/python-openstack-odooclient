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

from typing import Literal

from ..base.record.base import RecordBase
from ..base.record_manager.base import RecordManagerBase


class UomCategory(RecordBase["UomCategoryManager"]):
    measure_type: Literal[
        "unit",
        "weight",
        "working_time",
        "length",
        "volume",
    ]
    """The type of Unit of Measure (UoM) category.

    This field no longer exists from Odoo 14 onwards.

    Values:

    * ``unit`` - Default Units
    * ``weight`` - Default Weight
    * ``working_time`` - Default Working Time
    * ``length`` - Default Length
    * ``volume`` - Default Volume
    """

    name: str
    """The name of the Unit of Measure (UoM) category."""


class UomCategoryManager(RecordManagerBase[UomCategory]):
    env_name = "uom.category"
    record_class = UomCategory
