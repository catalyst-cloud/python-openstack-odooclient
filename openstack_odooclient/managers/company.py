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

from . import record_base, record_manager_name_base


class Company(record_base.RecordBase):
    active: bool
    """Whether or not this company is active (enabled)."""

    child_ids: Annotated[
        List[int],
        record_base.ModelRef("child_ids", Self),
    ]
    """A list of IDs for the child companies."""

    children: Annotated[
        List[Self],
        record_base.ModelRef("child_ids", Self),
    ]
    """The list of child companies.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    name: str
    """Company name, set from the partner name."""

    parent_id: Annotated[
        Optional[int],
        record_base.ModelRef("parent_id", Self),
    ]
    """The ID for the parent company, if this company
    is the child of another company.
    """

    parent_name: Annotated[
        Optional[str],
        record_base.ModelRef("parent_id", Self),
    ]
    """The name of the parent company, if this company
    is the child of another company.
    """

    parent: Annotated[Optional[Self], record_base.ModelRef("parent_id", Self)]
    """The parent company, if this company
    is the child of another company.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    parent_path: Union[str, Literal[False]]
    """The path of the parent company, if there is a parent."""

    partner_id: Annotated[
        int,
        record_base.ModelRef("partner_id", partner_module.Partner),
    ]
    """The ID for the partner for the company."""

    partner_name: Annotated[
        str,
        record_base.ModelRef("partner_id", partner_module.Partner),
    ]
    """The name of the partner for the company."""

    partner: Annotated[
        partner_module.Partner,
        record_base.ModelRef("partner_id", partner_module.Partner),
    ]
    """The partner for the company.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class CompanyManager(
    record_manager_name_base.NamedRecordManagerBase[Company],
):
    env_name = "res.company"
    record_class = Company


# NOTE(callumdickinson): Import here to make sure circular imports work.
from . import partner as partner_module  # noqa: E402
