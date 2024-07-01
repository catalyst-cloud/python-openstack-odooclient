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

from typing import List, Optional, Union

from typing_extensions import Annotated

from ..base.record import ModelRef, RecordBase
from ..base.record_manager import RecordManagerBase


class VolumeDiscountRange(RecordBase["VolumeDiscountRangeManager"]):
    customer_group_id: Annotated[
        Optional[int],
        ModelRef("customer_group", CustomerGroup),
    ]
    """The ID for the customer group this volume discount range
    applies to, if a specific customer group is set.

    If no customer group is set, this volume discount range
    applies to all customers.
    """

    customer_group_name: Annotated[
        Optional[str],
        ModelRef("customer_group", CustomerGroup),
    ]
    """The name of the customer group this volume discount range
    applies to, if a specific customer group is set.

    If no customer group is set, this volume discount range
    applies to all customers.
    """

    customer_group: Annotated[
        Optional[CustomerGroup],
        ModelRef("customer_group", CustomerGroup),
    ]
    """The customer group this volume discount range
    applies to, if a specific customer group is set.

    If no customer group is set, this volume discount range
    applies to all customers.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    discount_percent: float
    """Discount percentage of this volume discount range (0-100)."""

    name: str
    """The automatically generated name (description) of
    this volume discount range.
    """

    max: Optional[float]
    """Optional maximum charge for this volume discount range.

    Intended to be used when creating tiered volume discounts for customers.
    """

    min: float
    """Minimum charge for this volume discount range."""

    use_max: bool
    """Use the ``max`` field, if defined."""


class VolumeDiscountRangeManager(RecordManagerBase[VolumeDiscountRange]):
    env_name = "openstack.volume_discount_range"
    record_class = VolumeDiscountRange

    def get_for_charge(
        self,
        charge: float,
        customer_group: Optional[Union[int, CustomerGroup]] = None,
    ) -> Optional[VolumeDiscountRange]:
        """Return the volume discount range to apply to a given charge.

        If ``customer_group`` is supplied, volume discount ranges for
        a specific customer group are returned. When set to ``None``
        (the default), volume discount ranges for all customers are returned.

        If multiple volume discount ranges can be applied, the range with
        the highest discount percentage is selected.
        If no applicable volume discount ranges were found,
        ``None`` is returned.

        :param charge: The charge to find the applicable discount range for
        :type charge: float
        :param customer_group: Get discount for a specific customer group
        :type customer_group: Optional[Union[int, CustomerGroup]], optional
        :return: Highest percentage applicable discount range (if found)
        :rtype: Optional[VolumeDiscountRange]
        """
        ranges = self.search(
            [("customer_group", "=", customer_group or False)],
        )
        found_ranges: List[VolumeDiscountRange] = []
        for vol_range in ranges:
            if charge < vol_range.min:
                continue
            if vol_range.use_max and vol_range.max and charge >= vol_range.max:
                continue
            found_ranges.append(vol_range)
        if not found_ranges:
            return None
        return sorted(found_ranges, key=lambda r: r.discount_percent)[-1]


# NOTE(callumdickinson): Import here to avoid circular imports.
from .customer_group import CustomerGroup  # noqa: E402
