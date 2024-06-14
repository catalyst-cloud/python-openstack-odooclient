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


class TermDiscount(record_base.RecordBase):
    discount_percent: float
    """The maximum discount percentage for this term discount (0-100)."""

    early_termination_date: Optional[date]
    """An optional early termination date for the term discount."""

    end_date: date
    """The date that the term discount expires on."""

    min_commit: float
    """The minimum commitment for this term discount to apply."""

    partner_id: Annotated[int, util.ModelRef("partner")]
    """The ID for the partner that receives this term discount."""

    partner_name: Annotated[str, util.ModelRef("partner")]
    """The name of the partner that receives this term discount."""

    partner: Annotated[partner_module.Partner, util.ModelRef("partner")]
    """The partner that receives this term discount.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    project_id: Annotated[Optional[int], util.ModelRef("project")]
    """The ID for the project this term discount applies to,
    if it is a project-specific term discount.

    If not set, the term discount applies to all projects
    the partner owns.
    """

    project_name: Annotated[Optional[str], util.ModelRef("project")]
    """The name of the project this term discount applies to,
    if it is a project-specific term discount.

    If not set, the term discount applies to all projects
    the partner owns.
    """

    project: Annotated[
        Optional[project_module.Project],
        util.ModelRef("project"),
    ]
    """The project this term discount applies to,
    if it is a project-specific term discount.

    If not set, the term discount applies to all projects
    the partner owns.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    start_date: date
    """The date from which this term discount starts."""

    superseded_by_id: Annotated[Optional[int], util.ModelRef("superseded_by")]
    """The ID for the term discount that supersedes this one,
    if superseded.
    """

    superseded_by_name: Annotated[
        Optional[str],
        util.ModelRef("superseded_by"),
    ]
    """The name of the term discount that supersedes this one,
    if superseded.
    """

    superseded_by: Annotated[
        Optional[TermDiscount],
        util.ModelRef("superseded_by"),
    ]
    """The term discount that supersedes this one,
    if superseded.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class TermDiscountManager(
    record_manager_base.RecordManagerBase[TermDiscount],
):
    env_name = "openstack.term_discount"
    record_class = TermDiscount


# NOTE(callumdickinson): Import here to avoid circular imports.
from . import (  # noqa :E402
    partner as partner_module,
    project as project_module,
)
