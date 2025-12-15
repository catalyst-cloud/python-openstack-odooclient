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


class User(RecordBase["UserManager"]):
    active: bool
    """Whether or not this user is active (enabled)."""

    active_partner: bool
    """Whether or not the partner this user is associated with is active."""

    company_id: Annotated[int, ModelRef("company_id", Company)]
    """The ID for the default company this user is logged in as."""

    company_name: Annotated[str, ModelRef("company_id", Company)]
    """The name of the default company this user is logged in as."""

    company: Annotated[Company, ModelRef("company_id", Company)]
    """The default company this user is logged in as.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    name: str
    """User name."""

    partner_id: Annotated[int, ModelRef("partner_id", Partner)]
    """The ID for the partner that this user is associated with."""

    partner_name: Annotated[str, ModelRef("partner_id", Partner)]
    """The name of the partner that this user is associated with."""

    partner: Annotated[Partner, ModelRef("partner_id", Partner)]
    """The partner that this user is associated with.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class UserManager(RecordManagerBase[User]):
    env_name = "res.users"
    record_class = User


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .company import Company  # noqa: E402
from .partner import Partner  # noqa: E402
