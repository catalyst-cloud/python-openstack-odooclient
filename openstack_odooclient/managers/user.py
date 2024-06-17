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

from typing_extensions import Annotated

from . import (
    company as company_module,
    record_base,
    record_manager_base,
)


class User(record_base.RecordBase):
    active: bool
    """Whether or not this user is active."""

    active_partner: bool
    """Whether or not the partner this user is associated with is active."""

    company_id: Annotated[
        int,
        record_base.ModelRef("company_id", company_module.Company),
    ]
    """The ID for the default company this user is logged in as."""

    company_name: Annotated[
        str,
        record_base.ModelRef("company_id", company_module.Company),
    ]
    """The name of the default company this user is logged in as."""

    company: Annotated[
        company_module.Company,
        record_base.ModelRef("company_id", company_module.Company),
    ]
    """The default company this user is logged in as.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    name: str
    """User name."""

    partner_id: Annotated[
        int,
        record_base.ModelRef("partner_id", partner_module.Partner),
    ]
    """The ID for the partner that this user is associated with."""

    partner_name: Annotated[
        str,
        record_base.ModelRef("partner_id", partner_module.Partner),
    ]
    """The name of the partner that this user is associated with."""

    partner: Annotated[
        partner_module.Partner,
        record_base.ModelRef("partner_id", partner_module.Partner),
    ]
    """The partner that this user is associated with.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class UserManager(record_manager_base.RecordManagerBase[User]):
    env_name = "res.users"
    record_class = User


# NOTE(callumdickinson): Import here to make sure circular imports work.
from . import partner as partner_module  # noqa: E402
