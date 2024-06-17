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

from typing import List

from typing_extensions import Annotated

from . import (
    product as product_module,
    product_category,
    record_base,
    record_manager_name_base,
)


class CreditType(record_base.RecordBase):
    credit_ids: Annotated[
        List[int],
        record_base.ModelRef("credits", credit.Credit),
    ]
    """A list of IDs for the credits which are of this credit type."""

    credits: Annotated[
        List[credit.Credit],
        record_base.ModelRef("credits", credit.Credit),
    ]
    """A list of credits which are of this credit type.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    name: str
    """Name of the Credit Type."""

    only_for_product_ids: Annotated[
        List[int],
        record_base.ModelRef("only_for_products", product_module.Product),
    ]
    """A list of IDs for the products this credit applies to.

    Mutually exclusive with ``only_for_product_category_ids``.
    If neither are specified, the credit applies to all products.
    """

    only_for_products: Annotated[
        List[product_module.Product],
        record_base.ModelRef("only_for_products", product_module.Product),
    ]
    """A list of products which this credit applies to.

    Mutually exclusive with ``only_for_product_categories``.
    If neither are specified, the credit applies to all products.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    only_for_product_category_ids: Annotated[
        List[int],
        record_base.ModelRef(
            "only_for_product_categories",
            product_category.ProductCategory,
        ),
    ]
    """A list of IDs for the product categories this credit applies to.

    Mutually exclusive with ``only_for_product_ids``.
    If neither are specified, the credit applies to all product
    categories.
    """

    only_for_product_categories: Annotated[
        List[product_category.ProductCategory],
        record_base.ModelRef(
            "only_for_product_categories",
            product_category.ProductCategory,
        ),
    ]
    """A list of product categories which this credit applies to.

    Mutually exclusive with ``only_for_products``.
    If neither are specified, the credit applies to all product
    categories.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    product_id: Annotated[
        int,
        record_base.ModelRef("product", product_module.Product),
    ]
    """The ID of the product to use when applying
    the credit to invoices.
    """

    product_name: Annotated[
        str,
        record_base.ModelRef("product", product_module.Product),
    ]
    """The name of the product to use when applying
    the credit to invoices.
    """

    product: Annotated[
        product_module.Product,
        record_base.ModelRef("product", product_module.Product),
    ]
    """The product to use when applying the credit to invoices.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    refundable: bool
    """Whether or not the credit is refundable."""


class CreditTypeManager(
    record_manager_name_base.NamedRecordManagerBase[CreditType],
):
    env_name = "openstack.credit.type"
    record_class = CreditType


# NOTE(callumdickinson): Import here to make sure circular imports work.
from . import credit  # noqa: E402
