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
from functools import cached_property
from typing import TYPE_CHECKING, Optional

from . import record_base, record_manager_base

if TYPE_CHECKING:
    from . import partner as partner_module, project as project_module


class TermDiscount(record_base.RecordBase):
    discount_percent: float
    """The maximum discount percentage for this term discount (0-100)."""

    early_termination_date: Optional[date]
    """An optional early termination date for the term discount."""

    end_date: date
    """The date that the term discount expires on."""

    min_commit: float
    """The minimum commitment for this term discount to apply."""

    @property
    def partner_id(self) -> int:
        """The ID for the partner that receives this term discount."""
        return self._get_ref_id("partner_id")

    @property
    def partner_name(self) -> str:
        """The name of the partner that receives this term discount."""
        return self._get_ref_name("partner_id")

    @cached_property
    def partner(self) -> partner_module.Partner:
        """The partner that receives this term discount.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.partners.get(self.partner_id)

    @property
    def project_id(self) -> Optional[int]:
        """The ID for the project this term discount applies to,
        if it is a project-specific term discount.

        If not set, the term discount applies to all projects
        the partner owns.
        """
        return self._get_ref_id("project", optional=True)

    @property
    def project_name(self) -> Optional[str]:
        """The name of the project this term discount applies to,
        if it is a project-specific term discount.

        If not set, the term discount applies to all projects
        the partner owns.
        """
        return self._get_ref_name("project", optional=True)

    @cached_property
    def project(self) -> Optional[project_module.Project]:
        """The project this term discount applies to,
        if it is a project-specific term discount.

        If not set, the term discount applies to all projects
        the partner owns.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.project_id
        return (
            self._client.projects.get(record_id)
            if record_id is not None
            else None
        )

    start_date: date
    """The date from which this term discount starts."""

    @property
    def superseded_by_id(self) -> Optional[int]:
        """The ID for the term discount that supersedes this one,
        if superseded.
        """
        return self._get_ref_id("superseded_by", optional=True)

    @property
    def superseded_by_name(self) -> Optional[str]:
        """The name of the term discount that supersedes this one,
        if superseded.
        """
        return self._get_ref_name("superseded_by", optional=True)

    @cached_property
    def superseded_by(self) -> Optional[TermDiscount]:
        """The term discount that supersedes this one,
        if superseded.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.superseded_by_id
        return (
            self._client.term_discounts.get(record_id)
            if record_id is not None
            else None
        )

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "partner_id": "partner",
        "project_id": "project",
        "superseded_by_id": "superseded_by",
    }


class TermDiscountManager(
    record_manager_base.RecordManagerBase[TermDiscount],
):
    env_name = "openstack.term_discount"
    record_class = TermDiscount
