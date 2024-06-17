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
from typing import Optional

from typing_extensions import Annotated

from ..base.record import ModelRef, RecordBase
from ..base.record_manager import RecordManagerBase


class Grant(RecordBase):
    expiry_date: date
    """The date the grant expires."""

    grant_type_id: Annotated[int, ModelRef("grant_type", GrantType)]
    """The ID of the type of this grant."""

    grant_type_name: Annotated[str, ModelRef("grant_type", GrantType)]
    """The name of the type of this grant."""

    grant_type: Annotated[GrantType, ModelRef("grant_type", GrantType)]
    """The type of this grant.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    name: str
    """The automatically generated name of the grant."""

    start_date: date
    """The start date of the grant."""

    value: float
    """The value of the grant."""

    voucher_code_id: Annotated[
        Optional[int],
        ModelRef("voucher_code", VoucherCode),
    ]
    """The ID of the voucher code used when applying for the grant,
    if one was supplied.
    """

    voucher_code_name: Annotated[
        Optional[str],
        ModelRef("voucher_code", VoucherCode),
    ]
    """The name of the voucher code used when applying for the grant,
    if one was supplied.
    """

    voucher_code: Annotated[
        Optional[VoucherCode],
        ModelRef("voucher_code", VoucherCode),
    ]
    """The voucher code used when applying for the grant,
    if one was supplied.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class GrantManager(RecordManagerBase[Grant]):
    env_name = "openstack.grant"
    record_class = Grant


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .grant_type import GrantType  # noqa: E402
from .voucher_code import VoucherCode  # noqa: E402
