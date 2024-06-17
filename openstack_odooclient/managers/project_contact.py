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

from typing import Literal, Optional

from typing_extensions import Annotated

from . import record_base, record_manager_base


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

    partner_id: Annotated[
        int,
        record_base.ModelRef("partner", partner_module.Partner),
    ]
    """The ID for the partner linked to this project contact."""

    partner_name: Annotated[
        str,
        record_base.ModelRef("partner", partner_module.Partner),
    ]
    """The name of the partner linked to this project contact."""

    partner: Annotated[
        partner_module.Partner,
        record_base.ModelRef("partner", partner_module.Partner),
    ]
    """The partner linked to this project contact.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    project_id: Annotated[
        Optional[int],
        record_base.ModelRef("project", project_module.Project),
    ]
    """The ID for the project this contact is linked to, if set."""

    project_name: Annotated[
        Optional[str],
        record_base.ModelRef("project", project_module.Project),
    ]
    """The name of the project this contact is linked to, if set."""

    project: Annotated[
        Optional[project_module.Project],
        record_base.ModelRef("project", project_module.Project),
    ]
    """The project this contact is linked to, if set.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class ProjectContactManager(
    record_manager_base.RecordManagerBase[ProjectContact],
):
    env_name = "openstack.project_contact"
    record_class = ProjectContact


# NOTE(callumdickinson): Import here to make sure circular imports work.
from . import (  # noqa: E402
    partner as partner_module,
    project as project_module,
)
