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

from functools import cached_property
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Union,
    overload,
)

from . import record_base, record_manager_unique_field_base

if TYPE_CHECKING:
    from . import (
        credit,
        grant,
        partner as partner_module,
        project_contact,
        support_subscription as support_subscription_module,
        term_discount,
    )


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

    @property
    def owner_id(self) -> int:
        """The ID for the partner that owns this project."""
        return self._get_ref_id("owner")

    @property
    def owner_name(self) -> str:
        """The name of the partner that owns this project."""
        return self._get_ref_name("owner")

    @cached_property
    def owner(self) -> partner_module.Partner:
        """The partner that owns this project.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.partners.get(self.owner_id)

    @property
    def parent_id(self) -> Optional[int]:
        """The ID for the parent project, if this project
        is the child of another project.
        """
        return self._get_ref_id("parent", optional=True)

    @property
    def parent_name(self) -> Optional[str]:
        """The name of the parent project, if this project
        is the child of another project.
        """
        return self._get_ref_name("parent", optional=True)

    @cached_property
    def parent(self) -> Optional[Project]:
        """The parent project, if this project
        is the child of another project.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.parent_id
        return (
            self._client.projects.get(record_id)
            if record_id is not None
            else None
        )

    payment_method: Literal["invoice", "credit_card"]
    """Payment method configured on the project.

    Values:

    * ``invoice`` - Project is paid by invoice
    * ``credit_card`` - Project is paid by credit card
    """

    po_number: Union[str, Literal[False]]
    """The PO number set for this specific Project (if set)."""

    @property
    def project_contact_ids(self) -> List[int]:
        """A list of IDs for the contacts for this project."""
        return self._get_field("project_contacts")

    @cached_property
    def project_contacts(self) -> List[project_contact.ProjectContact]:
        """The contacts for this project.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.project_contacts.list(self.project_contact_ids)

    @property
    def project_credit_ids(self) -> List[int]:
        """A list of IDs for the credits that apply to this project."""
        return self._get_field("project_credits")

    @cached_property
    def project_credits(self) -> List[credit.Credit]:
        """The credits that apply to this project.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.credits.list(self.project_credit_ids)

    @property
    def project_grant_ids(self) -> List[int]:
        """A list of IDs for the grants that apply to this project."""
        return self._get_field("project_grants")

    @cached_property
    def project_grants(self) -> List[grant.Grant]:
        """The grants that apply to this project.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.grants.list(self.project_grant_ids)

    stripe_card_id: Union[str, Literal[False]]
    """The card ID used for credit card payments on this project
    using Stripe, if the payment method is set to ``credit_card``.

    If a credit card has not been assigned to this project,
    this field will be set to ``False``.
    """

    @property
    def support_subscription_id(self) -> Optional[int]:
        """The ID for the support subscription for this project,
        if the project has one.
        """
        return self._get_ref_id("support_subscription", optional=True)

    @property
    def support_subscription_name(self) -> Optional[str]:
        """The name of the support subscription for this project,
        if the project has one.
        """
        return self._get_ref_name("support_subscription", optional=True)

    @cached_property
    def support_subscription(
        self,
    ) -> Optional[support_subscription_module.SupportSubscription]:
        """The support subscription for this project,
        if the project has one.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.support_subscription_id
        return (
            self._client.support_subscriptions.get(record_id)
            if record_id is not None
            else None
        )

    @property
    def term_discount_ids(self) -> List[int]:
        """A list of IDs for the term discounts that apply to this project."""
        return self._get_field("term_discounts")

    @cached_property
    def term_discounts(self) -> List[term_discount.TermDiscount]:
        """The term discounts that apply to this project.

        This fetches the full records from Odoo once,
        and caches them for subsequent accesses.
        """
        return self._client.term_discounts.list(self.term_discount_ids)

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "owner_id": "owner",
        "parent_id": "parent",
        "project_contact_ids": "project_contacts",
        "project_credit_ids": "project_credits",
        "project_grant_ids": "project_grants",
        "support_subcription_id": "support_subscription",
        "term_discount_ids": "term_discounts",
    }


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
