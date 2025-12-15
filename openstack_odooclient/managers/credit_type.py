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
from ..mixins.named_record import NamedRecordManagerMixin, NamedRecordMixin


class CreditType(
    RecordBase["CreditTypeManager"],
    NamedRecordMixin["CreditTypeManager"],
):
    credit_ids: Annotated[list[int], ModelRef("credits", Credit)]
    """A list of IDs for the credits which are of this credit type."""

    credits: Annotated[list[Credit], ModelRef("credits", Credit)]
    """A list of credits which are of this credit type.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    only_for_product_ids: Annotated[
        list[int],
        ModelRef("only_for_products", Product),
    ]
    """A list of IDs for the products this credit applies to.

    Mutually exclusive with
    ``only_for_product_category_ids``/``only_for_product_categories``.
    If none of these values are specified, the credit applies to all products.
    """

    only_for_products: Annotated[
        list[Product],
        ModelRef("only_for_products", Product),
    ]
    """A list of products which this credit applies to.

    Mutually exclusive with
    ``only_for_product_category_ids``/``only_for_product_categories``.
    If none of these values are specified, the credit applies to all products.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    only_for_product_category_ids: Annotated[
        list[int],
        ModelRef("only_for_product_categories", ProductCategory),
    ]
    """A list of IDs for the product categories this credit applies to.

    Mutually exclusive with ``only_for_product_ids``/``only_for_products``.
    If none of these values are specified, the credit applies to all products.
    """

    only_for_product_categories: Annotated[
        list[ProductCategory],
        ModelRef("only_for_product_categories", ProductCategory),
    ]
    """A list of product categories which this credit applies to.

    Mutually exclusive with ``only_for_product_ids``/``only_for_products``.
    If none of these values are specified, the credit applies to all products.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

    product_id: Annotated[int, ModelRef("product", Product)]
    """The ID of the product to use when applying
    the credit to invoices.
    """

    product_name: Annotated[str, ModelRef("product", Product)]
    """The name of the product to use when applying
    the credit to invoices.
    """

    product: Annotated[Product, ModelRef("product", Product)]
    """The product to use when applying the credit to invoices.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

    refundable: bool
    """Whether or not the credit is refundable."""


class CreditTypeManager(
    RecordManagerBase[CreditType],
    NamedRecordManagerMixin[CreditType],
):
    env_name = "openstack.credit.type"
    record_class = CreditType


# NOTE(callumdickinson): Import here to make sure circular imports work.
from .credit import Credit  # noqa: E402
from .product import Product  # noqa: E402
from .product_category import ProductCategory  # noqa: E402
