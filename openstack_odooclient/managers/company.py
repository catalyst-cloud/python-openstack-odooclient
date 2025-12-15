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

from typing_extensions import Self

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase
from ..mixins.named_record import NamedRecordManagerMixin, NamedRecordMixin


class Company(
    RecordBase["CompanyManager"],
    NamedRecordMixin["CompanyManager"],
):
    active: bool
    """Whether or not this company is active (enabled)."""

    child_ids: Annotated[list[int], ModelRef("child_ids", Self)]
    """A list of IDs for the child companies."""

    children: Annotated[list[Self], ModelRef("child_ids", Self)]
    """The list of child companies.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    parent_id: Annotated[int | None, ModelRef("parent_id", Self)]
    """The ID for the parent company, if this company
    is the child of another company.
    """

    parent_name: Annotated[str | None, ModelRef("parent_id", Self)]
    """The name of the parent company, if this company
    is the child of another company.
    """

    parent: Annotated[Self | None, ModelRef("parent_id", Self)]
    """The parent company, if this company
    is the child of another company.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    parent_path: str | Literal[False]
    """The path of the parent company, if there is a parent."""

    partner_id: Annotated[int, ModelRef("partner_id", Partner)]
    """The ID for the partner for the company."""

    partner_name: Annotated[str, ModelRef("partner_id", Partner)]
    """The name of the partner for the company."""

    partner: Annotated[Partner, ModelRef("partner_id", Partner)]
    """The partner for the company.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class CompanyManager(
    RecordManagerBase[Company],
    NamedRecordManagerMixin[Company],
):
    env_name = "res.company"
    record_class = Company


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .partner import Partner  # noqa: E402
