# Copyright (C) 2025 Catalyst Cloud Limited
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

from typing import Annotated, Generic

from ..base.record.base import RM, RecordProtocol
from ..base.record.types import ModelRef
from ..managers.attachment import Attachment


class RecordWithAttachmentMixin(RecordProtocol[RM], Generic[RM]):
    """A record mixin for record types with an attachment associated with it.

    Include this mixin to add the ``message_main_attachment_id``,
    ``message_main_attachment_name`` and ``message_main_attachment`` fields
    to your record class, which allow attachments associated with the record
    to be referenced.
    """

    message_main_attachment_id: Annotated[
        int | None,
        ModelRef("message_main_attachment_id", Attachment),
    ]
    """The ID of the main attachment on the record, if there is one."""

    message_main_attachment_name: Annotated[
        str | None,
        ModelRef("message_main_attachment_name", Attachment),
    ]
    """The name of the main attachment on the record, if there is one."""

    message_main_attachment: Annotated[
        Attachment | None,
        ModelRef("message_main_attachment", Attachment),
    ]
    """The main attachment on the record, if there is one.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """
