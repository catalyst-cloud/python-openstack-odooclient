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

from . import record_base, record_manager_base, util


class Grant(record_base.RecordBase):
    expiry_date: date
    """The date the grant expires."""

    grant_type_id: Annotated[int, util.ModelRef("grant_type")]
    """The ID of the type of this grant."""

    grant_type_name: Annotated[str, util.ModelRef("grant_type")]
    """The name of the type of this grant."""

    grant_type: Annotated[
        grant_type_module.GrantType,
        util.ModelRef("grant_type"),
    ]
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

    voucher_code_id: Annotated[Optional[int], util.ModelRef("voucher_code")]
    """The ID of the voucher code used when applying for the grant,
    if one was supplied.
    """

    voucher_code_name: Annotated[Optional[str], util.ModelRef("voucher_code")]
    """The name of the voucher code used when applying for the grant,
    if one was supplied.
    """

    voucher_code: Annotated[
        Optional[voucher_code_module.VoucherCode],
        util.ModelRef("voucher_code"),
    ]
    """The voucher code used when applying for the grant,
    if one was supplied.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class GrantManager(record_manager_base.RecordManagerBase[Grant]):
    env_name = "openstack.grant"
    record_class = Grant


# NOTE(callumdickinson): Import here to make sure circular imports work.
from . import (  # noqa: E402
    grant_type as grant_type_module,
    voucher_code as voucher_code_module,
)
