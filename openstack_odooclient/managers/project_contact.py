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

from typing import Annotated, Literal

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase


class ProjectContact(RecordBase["ProjectContactManager"]):
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

    partner_id: Annotated[int, ModelRef("partner", Partner)]
    """The ID for the partner linked to this project contact."""

    partner_name: Annotated[str, ModelRef("partner", Partner)]
    """The name of the partner linked to this project contact."""

    partner: Annotated[Partner, ModelRef("partner", Partner)]
    """The partner linked to this project contact.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    project_id: Annotated[int | None, ModelRef("project", Project)]
    """The ID for the project this contact is linked to, if set."""

    project_name: Annotated[str | None, ModelRef("project", Project)]
    """The name of the project this contact is linked to, if set."""

    project: Annotated[Project | None, ModelRef("project", Project)]
    """The project this contact is linked to, if set.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class ProjectContactManager(RecordManagerBase[ProjectContact]):
    env_name = "openstack.project_contact"
    record_class = ProjectContact


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .partner import Partner  # noqa: E402
from .project import Project  # noqa: E402
