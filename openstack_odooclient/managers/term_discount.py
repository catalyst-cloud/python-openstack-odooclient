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
from typing import Annotated

from typing_extensions import Self

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase


class TermDiscount(RecordBase["TermDiscountManager"]):
    discount_percent: float
    """The maximum discount percentage for this term discount (0-100)."""

    early_termination_date: date | None
    """An optional early termination date for the term discount."""

    end_date: date
    """The date that the term discount expires on."""

    min_commit: float
    """The minimum commitment for this term discount to apply."""

    partner_id: Annotated[int, ModelRef("partner", Partner)]
    """The ID for the partner that receives this term discount."""

    partner_name: Annotated[str, ModelRef("partner", Partner)]
    """The name of the partner that receives this term discount."""

    partner: Annotated[Partner, ModelRef("partner", Partner)]
    """The partner that receives this term discount.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    project_id: Annotated[int | None, ModelRef("project", Project)]
    """The ID for the project this term discount applies to,
    if it is a project-specific term discount.

    If not set, the term discount applies to all projects
    the partner owns.
    """

    project_name: Annotated[str | None, ModelRef("project", Project)]
    """The name of the project this term discount applies to,
    if it is a project-specific term discount.

    If not set, the term discount applies to all projects
    the partner owns.
    """

    project: Annotated[Project | None, ModelRef("project", Project)]
    """The project this term discount applies to,
    if it is a project-specific term discount.

    If not set, the term discount applies to all projects
    the partner owns.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    start_date: date
    """The date from which this term discount starts."""

    superseded_by_id: Annotated[
        int | None,
        ModelRef("superseded_by", Self),
    ]
    """The ID for the term discount that supersedes this one,
    if superseded.
    """

    superseded_by_name: Annotated[
        str | None,
        ModelRef("superseded_by", Self),
    ]
    """The name of the term discount that supersedes this one,
    if superseded.
    """

    superseded_by: Annotated[
        Self | None,
        ModelRef("superseded_by", Self),
    ]
    """The term discount that supersedes this one,
    if superseded.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class TermDiscountManager(RecordManagerBase[TermDiscount]):
    env_name = "openstack.term_discount"
    record_class = TermDiscount


# NOTE(callumdickinson): Import here to avoid circular imports.
from .partner import Partner  # noqa: E402
from .project import Project  # noqa: E402
