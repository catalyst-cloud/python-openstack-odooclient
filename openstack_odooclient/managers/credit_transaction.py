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

from typing import Annotated

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase


class CreditTransaction(RecordBase["CreditTransactionManager"]):
    credit_id: Annotated[int, ModelRef("credit", Credit)]
    """The ID of the credit this transaction was made against."""

    credit_name: Annotated[str, ModelRef("credit", Credit)]
    """The name of the credit this transaction was made against."""

    credit: Annotated[Credit, ModelRef("credit", Credit)]
    """The credit this transaction was made against.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    description: str
    """A description of this credit transaction."""

    value: float
    """The value of the credit transaction."""


class CreditTransactionManager(RecordManagerBase[CreditTransaction]):
    env_name = "openstack.credit.transaction"
    record_class = CreditTransaction


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .credit import Credit  # noqa: E402
