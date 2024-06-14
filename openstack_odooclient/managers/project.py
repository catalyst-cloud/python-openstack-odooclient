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

from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Union,
    overload,
)

from typing_extensions import Annotated

from . import record_base, record_manager_unique_field_base, util


class Project(record_base.RecordBase):
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

    owner_id: Annotated[int, util.ModelRef("owner")]
    """The ID for the partner that owns this project."""

    owner_name: Annotated[str, util.ModelRef("owner")]
    """The name of the partner that owns this project."""

    owner: Annotated[partner_module.Partner, util.ModelRef("owner")]
    """The partner that owns this project.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    parent_id: Annotated[Optional[int], util.ModelRef("parent")]
    """The ID for the parent project, if this project
    is the child of another project.
    """

    parent_name: Annotated[Optional[str], util.ModelRef("parent")]
    """The name of the parent project, if this project
    is the child of another project.
    """

    parent: Annotated[Optional[Project], util.ModelRef("parent")]
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

    po_number: Union[str, Literal[False]]
    """The PO number set for this specific Project (if set)."""

    project_contact_ids: Annotated[
        List[int],
        util.ModelRef("project_contacts"),
    ]
    """A list of IDs for the contacts for this project."""

    project_contacts: Annotated[
        List[project_contact.ProjectContact],
        util.ModelRef("project_contacts"),
    ]
    """The contacts for this project.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    project_credit_ids: Annotated[List[int], util.ModelRef("project_credits")]
    """A list of IDs for the credits that apply to this project."""

    project_credits: Annotated[
        List[credit.Credit],
        util.ModelRef("project_credits"),
    ]
    """The credits that apply to this project.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    project_grant_ids: Annotated[List[int], util.ModelRef("project_grants")]
    """A list of IDs for the grants that apply to this project."""

    project_grants: Annotated[
        List[grant.Grant],
        util.ModelRef("project_grants"),
    ]
    """The grants that apply to this project.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    stripe_card_id: Union[str, Literal[False]]
    """The card ID used for credit card payments on this project
    using Stripe, if the payment method is set to ``credit_card``.

    If a credit card has not been assigned to this project,
    this field will be set to ``False``.
    """

    support_subscription_id: Annotated[
        Optional[int],
        util.ModelRef("support_subscription"),
    ]
    """The ID for the support subscription for this project,
    if the project has one.
    """

    support_subscription_name: Annotated[
        Optional[str],
        util.ModelRef("support_subscription"),
    ]
    """The name of the support subscription for this project,
    if the project has one.
    """

    support_subscription: Annotated[
        Optional[support_subscription_module.SupportSubscription],
        util.ModelRef("support_subscription"),
    ]
    """The support subscription for this project,
    if the project has one.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    term_discount_ids: Annotated[List[int], util.ModelRef("term_discounts")]
    """A list of IDs for the term discounts that apply to this project."""

    term_discounts: Annotated[
        List[term_discount.TermDiscount],
        util.ModelRef("term_discounts"),
    ]
    """The term discounts that apply to this project.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """


class ProjectManager(
    record_manager_unique_field_base.RecordManagerWithUniqueFieldBase[
        Project,
        str,
    ],
):
    env_name = "openstack.project"
    record_class = Project

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> Optional[int]: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> Optional[int]: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> Optional[Dict[str, Any]]: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> Dict[str, Any]: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> Optional[Project]: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> Project: ...

    @overload
    def get_by_os_id(
        self,
        os_id: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> Optional[Union[Project, int, Dict[str, Any]]]: ...

    def get_by_os_id(
        self,
        os_id: str,
        fields: Optional[Iterable[str]] = None,
        as_id: bool = False,
        as_dict: bool = False,
        optional: bool = False,
    ) -> Optional[Union[Project, int, Dict[str, Any]]]:
        """Query a unique record by OpenStack project ID.

        A number of parameters are available to configure the return type,
        and what happens when a result is not found.

        :param name: The record name
        :type name: str
        :param as_id: Return a record ID, defaults to False
        :type as_id: bool, optional
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[int] or None, optional
        :param as_dict: Return the record as a dictionary, defaults to False
        :type as_dict: bool, optional
        :param optional: Return ``None`` if not found, defaults to False
        :type optional: bool, optional
        :raises MultipleRecordsFoundError: Multiple records with the same name
        :raises RecordNotFoundError: Record with the given name not found
        :return: Query result (or ``None`` if record not found and optional)
        :rtype: Optional[Union[Project, int, Dict[str, Any]]]
        """
        return self._get_by_unique_field(
            field="os_id",
            value=os_id,
            fields=fields,
            as_id=as_id,
            as_dict=as_dict,
            optional=optional,
        )


# NOTE(callumdickinson): Import here to make sure circular imports work.
from . import (  # noqa: E402
    credit,
    grant,
    partner as partner_module,
    project_contact,
    support_subscription as support_subscription_module,
    term_discount,
)
