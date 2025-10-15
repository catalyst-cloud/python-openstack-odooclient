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

import base64

from typing import TYPE_CHECKING, Annotated, Any, Literal

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase

if TYPE_CHECKING:
    from ..base.client import ClientBase


class Attachment(RecordBase["AttachmentManager"]):
    access_token: str | Literal[False]
    """An access token that can be used to
    fetch the attachment, if defined.
    """

    checksum: str
    """A SHA1 checksum of the attachment contents."""

    company_id: Annotated[int | None, ModelRef("company_id", Company)]
    """The ID for the company that owns this attachment, if set."""

    company_name: Annotated[str | None, ModelRef("company_id", Company)]
    """The name of the company that owns this attachment, if set."""

    company: Annotated[Company | None, ModelRef("company_id", Company)]
    """The company that owns this attachment, if set.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    datas: str | Literal[False]
    """The contents of the attachment, encoded in base64.

    Only applies when ``type`` is set to ``binary``.

    **This field is not fetched by default.** To make this field available,
    use the ``fields`` parameter on the ``get`` or ``list`` methods to select
    the ``datas`` field.
    """

    description: str | Literal[False]
    """A description of the file, if defined."""

    index_content: str
    """The index content value computed from the attachment contents.

    **This field is not fetched by default.** To make this field available,
    use the ``fields`` parameter on the ``get`` or ``list`` methods to select
    the ``index_content`` field.
    """

    mimetype: str
    """MIME type of the attached file."""

    name: str
    """The name of the attachment.

    Usually matches the filename of the attached file.
    """

    public: bool
    """Whether or not the attachment is publicly accessible."""

    res_field: str | Literal[False]
    """The name of the field used to refer to this attachment
    on the linked record's model, if set.
    """

    res_id: int | Literal[False]
    """The ID of the record this attachment is linked to, if set."""

    res_model: str | Literal[False]
    """The name of the model of the record this attachment
    is linked to, if set.
    """

    res_name: str | Literal[False]
    """The name of the record this attachment is linked to, if set."""

    store_fname: str | Literal[False]
    """The stored filename for this attachment, if set."""

    type: Literal["binary", "url"]
    """The type of the attachment.

    When set to ``binary``, the contents of the attachment are available
    using the ``datas`` field. When set to ``url``, the attachment can be
    downloaded from the URL configured in the ``url`` field.

    Values:

    * ``binary`` - Stored internally as binary data
    * ``url`` - Stored externally, accessible using a URL
    """

    url: str | Literal[False]
    """The URL the contents of the attachment are available from.

    Only applies when ``type`` is set to ``url``.
    """

    @property
    def res_model_manager(self) -> RecordManagerBase[Any] | None:
        """The manager for the model of the record
        this attachment is linked to.
        """
        if not self.res_model:
            return None
        return get_res_model_manager(
            client=self._client,
            res_model=self.res_model,
        )

    def download(self) -> bytes:
        """Download this attachment, and return the contents as bytes.

        :return: Attachment contents
        :rtype: bytes
        """
        return download(manager=self._manager, attachment_id=self.id)

    def reupload(self, data: bytes, **fields: Any) -> None:
        """Reupload a new version of the contents of this attachment,
        and update the attachment in place.

        Other fields can be updated at the same time by passing them
        as keyword arguments. Any keyword arguments passed to this
        method are passed to the attachment record as fields.

        Note that this attachment object not updated in place by
        this method. If you need an updated version of the attachment
        object, use the `refresh` method to fetch the latest version.

        :param data: Contents of the attachment
        :type data: bytes
        """
        reupload(
            manager=self._manager,
            attachment_id=self.id,
            data=data,
            **fields,
        )

    def register_as_main_attachment(self, force: bool = True) -> None:
        """Register this attachment as the main attachment
        of the record it is attached to.

        The model of the attached record must have the
        ``message_main_attachment_id`` field defined.

        :param force: Overwrite if already set, defaults to True
        :type force: bool, optional
        """
        self._env.register_as_main_attachment(self.id, force=force)


class AttachmentManager(RecordManagerBase[Attachment]):
    env_name = "ir.attachment"
    record_class = Attachment
    default_fields = (
        "access_token",
        "checksum",
        "company_id",
        # datas not fetched by default
        "description",
        # index_content not fetched by default
        "mimetype",
        "name",
        "public",
        "res_field",
        "res_id",
        "res_model",
        "res_name",
        "store_fname",
        "type",
        "url",
    )

    def upload(
        self,
        name: str,
        data: bytes,
        *,
        record: RecordBase[Any] | None = None,
        res_id: int | None = None,
        res_model: str | None = None,
        **fields: Any,
    ) -> int:
        """Upload an attachment and associate it with the given record.

        One of ``record`` or ``res_id`` must be set to specify the record
        to link the attachment to. When ``res_id`` is used, ``res_model``
        (and in some cases, ``res_field``) must also be specified to define
        the model of the record.

        When ``record`` is used, this is not necessary.

        Any keyword arguments passed to this method are passed to
        the attachment record as fields.

        :param name: The name of the attachment
        :type name: str
        :param data: The contents of the attachment
        :type data: bytes
        :param record: The linked record, defaults to None
        :type record: RecordBase[Any] | None, optional
        :param res_id: The ID of the linked record, defaults to None
        :type res_id: int | None, optional
        :param res_model: The model of the linked record, defaults to None
        :type res_model: str | None, optional
        :return: The record ID of the newly uploaded attachment
        :rtype: int
        """
        return upload(
            manager=self,
            name=name,
            data=data,
            record=record,
            res_id=res_id,
            res_model=res_model,
            **fields,
        )

    def download(self, attachment: int | Attachment) -> bytes:
        """Download a given attachment, and return the contents as bytes.

        :param attachment: Attachment (ID or object)
        :type attachment: int | Attachment
        :return: Attachment contents
        :rtype: bytes
        """
        return download(
            manager=self,
            attachment_id=(
                attachment.id
                if isinstance(attachment, Attachment)
                else attachment
            ),
        )

    def reupload(
        self,
        attachment: int | Attachment,
        data: bytes,
        **fields: Any,
    ) -> None:
        """Reupload a new version of the contents of the given attachment,
        and update the attachment in place.

        Other fields can be updated at the same time by passing them
        as keyword arguments. Any keyword arguments passed to this
        method are passed to the attachment record as fields.

        :param data: Contents of the attachment
        :type data: bytes
        """
        reupload(
            manager=self,
            attachment_id=(
                attachment.id
                if isinstance(attachment, Attachment)
                else attachment
            ),
            data=data,
            **fields,
        )

    def register_as_main_attachment(
        self,
        attachment: int | Attachment,
        force: bool = True,
    ) -> None:
        """Register the given attachment as the main attachment
        of the record it is attached to.

        The model of the attached record must have the
        ``message_main_attachment_id`` field defined.

        :param attachment: Attachment (ID or object)
        :type attachment: int | Attachment
        :param force: Overwrite if already set, defaults to True
        :type force: bool, optional
        """
        self._env.register_as_main_attachment(
            (
                attachment.id
                if isinstance(attachment, Attachment)
                else attachment
            ),
            force=force,
        )


def get_res_model_manager(
    client: ClientBase,
    res_model: str,
) -> RecordManagerBase[Any]:
    """Return the manager for the given model.

    :param client: Odoo client object
    :type client: ClientBase
    :param res_model: Model name
    :type res_model: str
    :return: Model manager
    :rtype: RecordManagerBase[Any]
    """

    return client._env_manager_mapping[res_model]


def upload(
    *,
    manager: AttachmentManager,
    name: str,
    data: bytes,
    record: RecordBase[Any] | None = None,
    res_id: int | None = None,
    res_model: str | None = None,
    **fields: Any,
) -> int:
    """Upload an attachment and associate it with the given record.

    One of ``record`` or ``res_id`` must be set to specify the record
    to link the attachment to. When ``res_id`` is used, ``res_model``
    must also be specified to define the model of the record.

    When ``record`` is used, this is not necessary.

    Any keyword arguments passed to this method are passed to
    the attachment record as fields.

    :param manager: Attachment manager
    :type manager: AttachmentManager
    :param name: The name of the attachment
    :type name: str
    :param data: The contents of the attachment
    :type data: bytes
    :param record: The linked record, defaults to None
    :type record: RecordBase[Any] | None, optional
    :param res_id: The ID of the linked record, defaults to None
    :type res_id: int | None, optional
    :param res_model: The model of the linked record, defaults to None
    :type res_model: str | None, optional
    :return: The record ID of the newly uploaded attachment
    :rtype: int
    """

    if record:
        res_id = record.id
        res_model = record._manager.env_name
    elif not res_id:
        raise ValueError(
            (
                "Either record or res_id must be specified "
                f"when uploading attachment: {name}"
            ),
        )

    if not res_model:
        raise ValueError(
            (
                "res_model must be specified for a record reference using "
                f"res_id {res_id} when uploading attachment: {name}"
            ),
        )

    fields["type"] = "binary"
    fields.pop("datas", None)
    fields.pop("url", None)

    return manager.create(
        name=name,
        res_id=res_id,
        res_model=res_model,
        datas=base64.b64encode(data).decode(encoding="ascii"),
        **fields,
    )


def download(manager: AttachmentManager, attachment_id: int) -> bytes:
    """Download an attachment by ID, and return the contents as bytes.

    :param manager: Attachment manager
    :type manager: AttachmentManager
    :param attachment_id: ID of the attachment to download
    :type attachment_id: int
    :return: Attachment contents
    :rtype: bytes
    """

    return base64.b64decode(
        manager._env.read(attachment_id, fields=["datas"])[0]["datas"],
    )


def reupload(
    *,
    manager: AttachmentManager,
    attachment_id: int,
    data: bytes,
    **fields: Any,
) -> None:
    """Reupload a new version of the contents of the given attachment,
    and update the attachment in place.

    Other fields can be updated at the same time by passing them
    as keyword arguments. Any keyword arguments passed to this
    method are passed to the attachment record as fields.

    :param manager: Attachment manager
    :type manager: AttachmentManager
    :param attachment_id: Attachment ID
    :type attachment_id: int
    :param data: The contents of the attachment
    :type data: bytes
    """

    fields.pop("type", None)
    fields.pop("datas", None)
    fields.pop("url", None)

    return manager.update(
        attachment_id,
        datas=base64.b64encode(data).decode(encoding="ascii"),
        **fields,
    )


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .company import Company  # noqa: E402
