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

from typing import TYPE_CHECKING, Annotated, Any, Literal, overload

from typing_extensions import Self

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase

if TYPE_CHECKING:
    from collections.abc import Iterable


class Project(RecordBase["ProjectManager"]):
    billing_type: Literal["customer", "internal"]
    """Billing type for this project.

    Values:

    * ``customer`` - Customer project (should be charged)
    * ``internal`` - Internal project (should not be charged)
    """

    display_name: str
    """The automatically generated display name for the project."""

    enabled: bool
    """Whether or not the project is enabled in Odoo."""

    group_invoices: bool
    """Whether or not to group invoices together for this project."""

    name: str
    """OpenStack project name."""

    os_id: str
    """OpenStack project ID."""

    override_po_number: bool
    """Whether or not to override the PO number with the value
    set on this Project.
    """

    owner_id: Annotated[int, ModelRef("owner", Partner)]
    """The ID for the partner that owns this project."""

    owner_name: Annotated[str, ModelRef("owner", Partner)]
    """The name of the partner that owns this project."""

    owner: Annotated[Partner, ModelRef("owner", Partner)]
    """The partner that owns this project.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    parent_id: Annotated[int | None, ModelRef("parent", Self)]
    """The ID for the parent project, if this project
    is the child of another project.
    """

    parent_name: Annotated[str | None, ModelRef("parent", Self)]
    """The name of the parent project, if this project
    is the child of another project.
    """

    parent: Annotated[Self | None, ModelRef("parent", Self)]
    """The parent project, if this project
    is the child of another project.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    payment_method: Literal["invoice", "credit_card"]
    """Payment method configured on the project.

    Values:

    * ``invoice`` - Project is paid by invoice
    * ``credit_card`` - Project is paid by credit card
    """

    po_number: str | Literal[False]
    """The PO number set for this specific project (if set)."""

    project_contact_ids: Annotated[
        list[int],
        ModelRef("project_contacts", ProjectContact),
    ]
    """A list of IDs for the contacts for this project."""

    project_contacts: Annotated[
        list[ProjectContact],
        ModelRef("project_contacts", ProjectContact),
    ]
    """The contacts for this project.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    project_credit_ids: Annotated[
        list[int],
        ModelRef("project_credits", Credit),
    ]
    """A list of IDs for the credits that apply to this project."""

    project_credits: Annotated[
        list[Credit],
        ModelRef("project_credits", Credit),
    ]
    """The credits that apply to this project.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    project_grant_ids: Annotated[list[int], ModelRef("project_grants", Grant)]
    """A list of IDs for the grants that apply to this project."""

    project_grants: Annotated[list[Grant], ModelRef("project_grants", Grant)]
    """The grants that apply to this project.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    stripe_card_id: str | Literal[False]
    """The card ID used for credit card payments on this project
    using Stripe, if the payment method is set to ``credit_card``.

    If a credit card has not been assigned to this project,
    this field will be set to ``False``.
    """

    support_subscription_id: Annotated[
        int | None,
        ModelRef("support_subscription", SupportSubscription),
    ]
    """The ID for the support subscription for this project,
    if the project has one.
    """

    support_subscription_name: Annotated[
        str | None,
        ModelRef("support_subscription", SupportSubscription),
    ]
    """The name of the support subscription for this project,
    if the project has one.
    """

    support_subscription: Annotated[
        SupportSubscription | None,
        ModelRef("support_subscription", SupportSubscription),
    ]
    """The support subscription for this project,
    if the project has one.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    term_discount_ids: Annotated[
        list[int],
        ModelRef("term_discounts", TermDiscount),
    ]
    """A list of IDs for the term discounts that apply to this project."""

    term_discounts: Annotated[
        list[TermDiscount],
        ModelRef("term_discounts", TermDiscount),
    ]
    """The term discounts that apply to this project.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """


class ProjectManager(RecordManagerBase[Project]):
    env_name = "openstack.project"
    record_class = Project

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> int | None: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> int | None: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> dict[str, Any] | None: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> dict[str, Any]: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> Project | None: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> Project: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> Project | int | dict[str, Any] | None: ...

    def get_by_os_id(
        self,
        os_id: str,
        fields: Iterable[str] | None = None,
        as_id: bool = False,
        as_dict: bool = False,
        optional: bool = False,
    ) -> Project | int | dict[str, Any] | None:
        """Query a unique record by OpenStack project ID.

        A number of parameters are available to configure the return type,
        and what happens when a result is not found.

        By default all fields available on the record model
        will be selected, but this can be filtered using the
        ``fields`` parameter.

        Use the ``as_id`` parameter to return the ID of the record,
        instead of the record object.

        Use the ``as_dict`` parameter to return the record as
        a ``dict`` object, instead of a record object.

        When ``optional`` is ``True``, ``None`` is returned if a record
        with the given name does not exist, instead of raising an error.

        :param os_id: The OpenStack project ID to search for
        :type os_id: str
        :param as_id: Return a record ID, defaults to False
        :type as_id: bool, optional
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[str] | None, optional
        :param as_dict: Return the record as a dictionary, defaults to False
        :type as_dict: bool, optional
        :param optional: Return ``None`` if not found, defaults to False
        :type optional: bool, optional
        :raises MultipleRecordsFoundError: Multiple with matching project IDs
        :raises RecordNotFoundError: No record with the given project ID found
        :return: Query result (or ``None`` if record not found and optional)
        :rtype: Project | int | dict[str, Any] | None
        """
        return self.get_by_unique_field(
            field="os_id",
            value=os_id,
            fields=fields,
            as_id=as_id,
            as_dict=as_dict,
            optional=optional,
        )


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .credit import Credit  # noqa: E402
from .grant import Grant  # noqa: E402
from .partner import Partner  # noqa: E402
from .project_contact import ProjectContact  # noqa: E402
from .support_subscription import SupportSubscription  # noqa: E402
from .term_discount import TermDiscount  # noqa: E402
