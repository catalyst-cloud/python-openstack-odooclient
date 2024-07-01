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

from ..base.record import ModelRef, RecordBase
from ..base.record_manager_with_unique_field import (
    RecordManagerWithUniqueFieldBase,
)


class Product(RecordBase["ProductManager"]):
    categ_id: Annotated[int, ModelRef("categ_id", ProductCategory)]
    """The ID for the category this product is under."""

    categ_name: Annotated[str, ModelRef("categ_id", ProductCategory)]
    """The name of the category this product is under."""

    categ: Annotated[ProductCategory, ModelRef("categ_id", ProductCategory)]
    """The category this product is under.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    company_id: Annotated[Optional[int], ModelRef("company_id", Company)]
    """The ID for the company that owns this product, if set."""

    company_name: Annotated[Optional[str], ModelRef("company_id", Company)]
    """The name of the company that owns this product, if set."""

    company: Annotated[Optional[Company], ModelRef("company_id", Company)]
    """The company that owns this product, if set.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    default_code: str
    """The Default Code for this product.

    In the OpenStack Integration add-on, this is used to store
    the rated unit for the service product.
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

    uom_id: Annotated[int, ModelRef("uom_id", Uom)]
    """The ID for the Unit of Measure for this product."""

    uom_name: Annotated[str, ModelRef("uom_id", Uom)]
    """The name of the Unit of Measure for this product."""

    uom: Annotated[Uom, ModelRef("uom_id", Uom)]
    """The Unit of Measure for this product.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """


class ProductManager(RecordManagerWithUniqueFieldBase[Product, str]):
    env_name = "product.product"
    record_class = Product

    @overload
    def get_sellable_company_products(
        self,
        company: Union[int, Company],
        *,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
    ) -> List[Product]: ...

    @overload
    def get_sellable_company_products(
        self,
        company: Union[int, Company],
        *,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
    ) -> List[int]: ...

    @overload
    def get_sellable_company_products(
        self,
        company: Union[int, Company],
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        *,
        as_id: Literal[True],
        as_dict: Literal[True],
    ) -> List[int]: ...

    @overload
    def get_sellable_company_products(
        self,
        company: Union[int, Company],
        *,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
    ) -> List[Dict[str, Any]]: ...

    @overload
    def get_sellable_company_products(
        self,
        company: Union[int, Company],
        *,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
    ) -> Union[List[Product], List[int], Union[List[Dict[str, Any]]]]: ...

    def get_sellable_company_products(
        self,
        company: Union[int, Company],
        fields: Optional[Iterable[str]] = None,
        order: Optional[str] = None,
        as_id: bool = False,
        as_dict: bool = False,
    ) -> Union[List[Product], List[int], Union[List[Dict[str, Any]]]]:
        """Fetch a list of active and saleable products for the given company.

        :param company: The company to search for products (ID or object)
        :type company: int | Company
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[str] or None, optional
        :param order: Order results by a specific field, defaults to None
        :type order: Optional[str], optional
        :param as_id: Return the record IDs only, defaults to False
        :type as_id: bool, optional
        :param as_dict: Return records as dictionaries, defaults to False
        :type as_dict: bool, optional
        :return: List of products
        :rtype: Union[List[Product], List[int], Union[Dict[str, Any]]]
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
        company: Union[int, Company],
        name: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> Optional[int]: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: Union[int, Company],
        name: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> Optional[int]: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: Union[int, Company],
        name: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: Union[int, Company],
        name: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> int: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: Union[int, Company],
        name: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[True],
    ) -> Optional[Dict[str, Any]]: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: Union[int, Company],
        name: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
        optional: Literal[False] = ...,
    ) -> Dict[str, Any]: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: Union[int, Company],
        name: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[True],
    ) -> Optional[Product]: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: Union[int, Company],
        name: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
        optional: Literal[False] = ...,
    ) -> Product: ...

    @overload
    def get_sellable_company_product_by_name(
        self,
        company: Union[int, Company],
        name: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> Optional[Union[Product, int, Dict[str, Any]]]: ...

    def get_sellable_company_product_by_name(
        self,
        company: Union[int, Company],
        name: str,
        fields: Optional[Iterable[str]] = None,
        as_id: bool = False,
        as_dict: bool = False,
        optional: bool = False,
    ) -> Optional[Union[Product, int, Dict[str, Any]]]:
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
        :type fields: Iterable[str] or None, optional
        :param as_id: Return a record ID, defaults to False
        :type as_id: bool, optional
        :param as_dict: Return the record as a dictionary, defaults to False
        :type as_dict: bool, optional
        :param optional: Return ``None`` if not found, defaults to False
        :type optional: bool, optional
        :raises MultipleRecordsFoundError: Multiple records with the same name
        :raises RecordNotFoundError: Record with the given name not found
        :return: Product (or ``None`` if record not found and optional)
        :rtype: Optional[Union[Record, int, Dict[str, Any]]]
        """
        return self._get_by_unique_field(
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
