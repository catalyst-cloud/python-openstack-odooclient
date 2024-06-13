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
    from . import company, product_category, uom as uom_module


class Product(record_base.RecordBase):
    @property
    def categ_id(self) -> int:
        """The ID for the category this product is under."""
        return self._get_ref_id("categ_id")

    @property
    def categ_name(self) -> str:
        """The name of the category this product is under."""
        return self._get_ref_name("categ_id")

    @cached_property
    def categ(self) -> product_category.ProductCategory:
        """The category this product is under.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.product_categories.get(self.categ_id)

    @property
    def company_id(self) -> Optional[int]:
        """The ID for the company that owns this product, if set."""
        return self._get_ref_id("company_id", optional=True)

    @property
    def company_name(self) -> Optional[str]:
        """The name of the company that owns this product, if set."""
        return self._get_ref_name("company_id", optional=True)

    @cached_property
    def company(self) -> Optional[company.Company]:
        """The company that owns this product, if set.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        record_id = self.company_id
        return (
            self._client.companies.get(record_id)
            if record_id is not None
            else None
        )

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

    @property
    def uom_id(self) -> int:
        """The ID for the Unit of Measure for this product."""
        return self._get_ref_id("uom_id")

    @property
    def uom_name(self) -> str:
        """The name of the Unit of Measure for this product."""
        return self._get_ref_name("uom_id")

    @cached_property
    def uom(self) -> uom_module.Uom:
        """The Unit of Measure for this product.

        This fetches the full record from Odoo once,
        and caches it for subsequent accesses.
        """
        return self._client.uoms.get(self.uom_id)

    _alias_mapping = {
        # Key is local alias, value is remote field name.
        "categ": "categ_id",
        "company": "company_id",
        "uom": "uom_id",
    }


class ProductManager(
    record_manager_unique_field_base.RecordManagerWithUniqueFieldBase[
        Product,
        str,
    ],
):
    env_name = "product.product"
    record_class = Product

    @overload
    def get_sellable_company_products(
        self,
        company: Union[int, company.Company],
        *,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[False] = ...,
    ) -> List[Product]: ...

    @overload
    def get_sellable_company_products(
        self,
        company: Union[int, company.Company],
        *,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: Literal[True],
        as_dict: Literal[False] = ...,
    ) -> List[int]: ...

    @overload
    def get_sellable_company_products(
        self,
        company: Union[int, company.Company],
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        *,
        as_id: Literal[True],
        as_dict: Literal[True],
    ) -> List[int]: ...

    @overload
    def get_sellable_company_products(
        self,
        company: Union[int, company.Company],
        *,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: Literal[False] = ...,
        as_dict: Literal[True],
    ) -> List[Dict[str, Any]]: ...

    @overload
    def get_sellable_company_products(
        self,
        company: Union[int, company.Company],
        *,
        fields: Optional[Iterable[str]] = ...,
        order: Optional[str] = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
    ) -> Union[List[Product], List[int], Union[List[Dict[str, Any]]]]: ...

    def get_sellable_company_products(
        self,
        company: Union[int, company.Company],
        fields: Optional[Iterable[str]] = None,
        order: Optional[str] = None,
        as_id: bool = False,
        as_dict: bool = False,
    ) -> Union[List[Product], List[int], Union[List[Dict[str, Any]]]]:
        """Fetch a list of active and saleable products for the given company.

        :param company: The company to search for products (ID or object)
        :type company: int | Company
        :param fields: Fields to select, defaults to ``None`` (select all)
        :type fields: Iterable[int] or None, optional
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
        company: Union[int, company.Company],
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
        company: Union[int, company.Company],
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
        company: Union[int, company.Company],
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
        company: Union[int, company.Company],
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
        company: Union[int, company.Company],
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
        company: Union[int, company.Company],
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
        company: Union[int, company.Company],
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
        company: Union[int, company.Company],
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
        company: Union[int, company.Company],
        name: str,
        *,
        fields: Optional[Iterable[str]] = ...,
        as_id: bool = ...,
        as_dict: bool = ...,
        optional: bool = ...,
    ) -> Optional[Union[Product, int, Dict[str, Any]]]: ...

    def get_sellable_company_product_by_name(
        self,
        company: Union[int, company.Company],
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
        :type fields: Iterable[int] or None, optional
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
