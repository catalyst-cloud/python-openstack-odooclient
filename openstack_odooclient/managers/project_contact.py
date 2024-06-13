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
from typing import TYPE_CHECKING, Literal, Optional

from . import record_base, record_manager_base

if TYPE_CHECKING:
    from . import partner as partner_module, project as project_module


class ProjectContact(record_base.RecordBase):
    contact_type: Literal[
        "primary",
        "billing",
        "technical",
        "legal",
        "reseller customer",
    ]
    """The contact type to assign the partner as on the project."""

    inherit: bool
    """Whether or not this contact should be inherited by child projects."""

    @property
    def partner_id(self) -> int:
        """The ID for the partner linked to this project contact."""
        return self._get_ref_id("partner")

    @property
    def partner_name(self) -> str:
        """The name of the partner linked to this project contact."""
        return self._get_ref_name("partner")

    @cached_property
    def partner(self) -> partner_module.Partner:
        """The partner linked to this project contact.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.partners.get(self.partner_id)

    @property
    def project_id(self) -> Optional[int]:
        """The ID for the project this contact is linked to, if set."""
        return self._get_ref_id("project", optional=True)

    @property
    def project_name(self) -> Optional[str]:
        """The name of the project this contact is linked to, if set."""
        return self._get_ref_name("project", optional=True)

    @cached_property
    def project(self) -> Optional[project_module.Project]:
        """The project this contact is linked to, if set.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.project_id
        return (
            self._client.projects.get(record_id)
            if record_id is not None
            else None
        )

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "partner_id": "partner",
        "project_id": "project",
    }


class ProjectContactManager(
    record_manager_base.RecordManagerBase[ProjectContact],
):
    env_name = "openstack.project_contact"
    record_class = ProjectContact
