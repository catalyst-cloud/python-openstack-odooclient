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

from ..base.record.base import RecordBase
from ..base.record.types import ModelRef
from ..base.record_manager.base import RecordManagerBase

if TYPE_CHECKING:
    from collections.abc import Iterable


class Product(RecordBase["ProductManager"]):
    active: bool
    """Whether or not this product is active (enabled).

    *Added in version 0.2.1.*
    """

    categ_id: Annotated[int, ModelRef("categ_id", ProductCategory)]
    """The ID for the category this product is under."""

    categ_name: Annotated[str, ModelRef("categ_id", ProductCategory)]
    """The name of the category this product is under."""

    categ: Annotated[ProductCategory, ModelRef("categ_id", ProductCategory)]
    """The category this product is under.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    company_id: Annotated[int | None, ModelRef("company_id", Company)]
    """The ID for the company that owns this product, if set."""

    company_name: Annotated[str | None, ModelRef("company_id", Company)]
    """The name of the company that owns this product, if set."""

    company: Annotated[Company | None, ModelRef("company_id", Company)]
    """The company that owns this product, if set.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    default_code: str | Literal[False]
    """The Default Code for this product, if set.

    In the OpenStack Integration add-on, this is used to store
    the rated unit for the service product.

    *Changed in version 0.2.1*: Made `default_code` optional.
    """

    description: str
    """A short description of this product."""

    display_name: str
    """The name of this product in OpenStack, and on invoices."""

    list_price: float
    """The list price of the product.

    This becomes the unit price of the product on invoices.
    """

    name: str
    """The name of the product."""

    sale_ok: bool
    """Whether or not this product is sellable.

    *Added in version 0.2.1.*
    """

    uom_id: Annotated[int, ModelRef("uom_id", Uom)]
    """The ID for the Unit of Measure for this product."""

    uom_name: Annotated[str, ModelRef("uom_id", Uom)]
    """The name of the Unit of Measure for this product."""

    uom: Annotated[Uom, ModelRef("uom_id", Uom)]
    """The Unit of Measure for this product.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class ProductManager(RecordManagerBase[Product]):
    env_name = "product.product"
    record_class = Product

    @overload
    def get_sellable_company_products(
        self,
        company: int | Company,
        *,
        fields: Iterable[str] | None = ...,
        order: str | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
    ) -> list[Product]: ...

    @overload
    def get_sellable_company_products(
        self,
        company: int | Company,
        *,
        fields: Iterable[str] | None = ...,
        order: str | None = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
    ) -> list[int]: ...

    @overload
    def get_sellable_company_products(
        self,
        company: int | Company,
        fields: Iterable[str] | None = ...,
        order: str | None = ...,
        *,
        as_id: Literal[True],
        as_dict: Literal[True],
    ) -> list[int]: ...

    @overload
    def get_sellable_company_products(
        self,
        company: int | Company,
        *,
        fields: Iterable[str] | None = ...,
        order: str | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
    ) -> list[dict[str, Any]]: ...

    @overload
    def get_sellable_company_products(
        self,
        company: int | Company,
        *,
        fields: Iterable[str] | None = ...,
        order: str | None = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
    ) -> list[Product] | list[int] | list[dict[str, Any]]: ...

    def get_sellable_company_products(
        self,
        company: int | Company,
        fields: Iterable[str] | None = None,
        order: str | None = None,
        as_id: bool = False,
        as_dict: bool = False,
    ) -> list[Product] | list[int] | list[dict[str, Any]]:
        """Fetch a list of active and saleable products for the given company.

        :param company: The company to search for products (ID or object)
        :type company: int | Company
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[str] | None, optional
        :param order: Order results by a specific field, defaults to None
        :type order: str | None, optional
        :param as_id: Return the record IDs only, defaults to False
        :type as_id: bool, optional
        :param as_dict: Return records as dictionaries, defaults to False
        :type as_dict: bool, optional
        :return: List of products
        :rtype: list[Product] | list[int] | list[dict[str, Any]]
        """
        return self.search(
            [
                ("company_id", "=", company),
                ("active", "=", True),
                ("sale_ok", "=", True),
            ],
            fields=fields,
            order=order,
            as_id=as_id,
            as_dict=as_dict,
        )

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: int | Company,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> int | None: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: int | Company,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> int | None: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: int | Company,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: int | Company,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: int | Company,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> dict[str, Any] | None: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: int | Company,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> dict[str, Any]: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: int | Company,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> Product | None: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: int | Company,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> Product: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: int | Company,
        name: str,
        *,
        fields: Iterable[str] | None = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> Product | int | dict[str, Any] | None: ...

    def get_sellable_company_product_by_name(
        self,
        company: int | Company,
        name: str,
        fields: Iterable[str] | None = None,
        as_id: bool = False,
        as_dict: bool = False,
        optional: bool = False,
    ) -> Product | int | dict[str, Any] | None:
        """Query a unique product for the given company by name.

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

        :param company: The company to search for products (ID or object)
        :type company: int | Company
        :param name: The product name
        :type name: str
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[str] | None, optional
        :param as_id: Return a record ID, defaults to False
        :type as_id: bool, optional
        :param as_dict: Return the record as a dictionary, defaults to False
        :type as_dict: bool, optional
        :param optional: Return ``None`` if not found, defaults to False
        :type optional: bool, optional
        :raises MultipleRecordsFoundError: Multiple records with the same name
        :raises RecordNotFoundError: Record with the given name not found
        :return: Product (or ``None`` if record not found and optional)
        :rtype: Record | int | dict[str, Any] | None
        """
        return self.get_by_unique_field(
            field="name",
            value=name,
            filters=[
                ("company_id", "=", company),
                ("active", "=", True),
                ("sale_ok", "=", True),
            ],
            fields=fields,
            as_id=as_id,
            as_dict=as_dict,
            optional=optional,
        )


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .company import Company  # noqa: E402
from .product_category import ProductCategory  # noqa: E402
from .uom import Uom  # noqa: E402
