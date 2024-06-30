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

from typing import List, Literal, Optional, Union

from typing_extensions import Annotated, Self

from ..base.record import FieldAlias, ModelRef, RecordBase
from ..base.record_manager_named import NamedRecordManagerBase


class PartnerCategory(RecordBase["PartnerCategoryManager"]):
    active: bool
    """Whether or not the partner category is active (enabled)."""

    child_ids: Annotated[List[int], ModelRef("child_id", Self)]
    """A list of IDs for the child categories."""

    children: Annotated[List[Self], ModelRef("child_id", Self)]
    """The list of child categories.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    color: int
    """Colour index for the partner category."""

    colour: Annotated[int, FieldAlias("color")]
    """Alias for ``color``."""

    name: str
    """The name of the partner category."""

    parent_id: Annotated[Optional[int], ModelRef("parent_id", Self)]
    """The ID for the parent partner category, if this category
    is the child of another category.
    """

    parent_name: Annotated[Optional[str], ModelRef("parent_id", Self)]
    """The name of the parent partner category, if this category
    is the child of another category.
    """

    parent: Annotated[Optional[Self], ModelRef("parent_id", Self)]
    """The parent partner category, if this category
    is the child of another category.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    parent_path: Union[str, Literal[False]]
    """The path of the parent partner category, if there is a parent."""

    partner_ids: Annotated[List[int], ModelRef("partner_id", Partner)]
    """A list of IDs for the partners in this category."""

    partners: Annotated[List[Partner], ModelRef("partner_id", Partner)]
    """The list of partners in this category.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """


class PartnerCategoryManager(NamedRecordManagerBase[PartnerCategory]):
    env_name = "res.partner.category"
    record_class = PartnerCategory


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .partner import Partner  # noqa: E402
