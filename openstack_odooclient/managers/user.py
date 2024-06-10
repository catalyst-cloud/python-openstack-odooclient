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
from typing import TYPE_CHECKING

from . import record

if TYPE_CHECKING:
    from . import company as company_module, partner as partner_module


class User(record.RecordBase):
    active: bool
    """Whether or not this user is active."""

    active_partner: bool
    """Whether or not the partner this user is associated with is active."""

    @property
    def company_id(self) -> int:
        """The ID for the default company this user is logged in as."""
        return self._get_ref_id("company_id")

    @property
    def company_name(self) -> str:
        """The name of the default company this user is logged in as."""
        return self._get_ref_name("company_id")

    @cached_property
    def company(self) -> company_module.Company:
        """The default company this user is logged in as.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.companies.get(self.company_id)

    name: str
    """User name."""

    @property
    def partner_id(self) -> int:
        """The ID for the partner that this user is associated with."""
        return self._get_ref_id("partner_id")

    @property
    def partner_name(self) -> str:
        """The name of the partner that this user is associated with."""
        return self._get_ref_name("partner_id")

    @cached_property
    def partner(self) -> partner_module.Partner:
        """The partner that this user is associated with.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.partners.get(self.partner_id)

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "company": "company_id",
        "partner": "partner_id",
    }


class UserManager(record.RecordManagerBase[User]):
    env_name = "res.users"
    record_class = User
