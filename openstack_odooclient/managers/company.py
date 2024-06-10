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
from typing import TYPE_CHECKING, List, Literal, Optional, Union

from . import record

if TYPE_CHECKING:
    from . import partner as partner_module


class Company(record.RecordBase):
    active: bool
    """Whether or not this company is active (enabled)."""

    child_ids: List[int]
    """A list of IDs for the child companies."""

    @cached_property
    def children(self) -> List[Company]:
        """The list of child companies.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.companies.list(self.child_ids)

    name: str
    """Company name, set from the partner name."""

    @property
    def parent_id(self) -> Optional[int]:
        """The ID for the parent company, if this company
        is the child of another company.
        """
        return self._get_ref_id("parent_id", optional=True)

    @property
    def parent_name(self) -> Optional[str]:
        """The name of the parent company, if this company
        is the child of another company.
        """
        return self._get_ref_name("parent_id", optional=True)

    @cached_property
    def parent(self) -> Optional[Company]:
        """The parent company, if this company
        is the child of another company.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.parent_id
        return (
            self._client.companies.get(record_id)
            if record_id is not None
            else None
        )

    parent_path: Union[str, Literal[False]]
    """The path of the parent company, if there is a parent."""

    @property
    def partner_id(self) -> int:
        """The ID for the partner for the company."""
        return self._get_ref_id("partner_id")

    @property
    def partner_name(self) -> str:
        """The name of the partner for the company."""
        return self._get_ref_name("partner_id")

    @cached_property
    def partner(self) -> partner_module.Partner:
        """The partner for the company.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.partners.get(self.partner_id)

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "children": "child_ids",
        "company": "company_id",
        "parent": "parent_id",
        "partner": "partner_id",
    }


class CompanyManager(record.NamedRecordManagerBase[Company]):
    env_name = "res.company"
    record_class = Company
