# OpenStack Credit Types

This page documents how to use the manager and record objects
for credit types.

## Details

| Name            | Value                   |
|-----------------|-------------------------|
| Odoo Modules    | OpenStack Integration   |
| Odoo Model Name | `openstack.credit.type` |
| Manager         | `credit_types`          |
| Record Type     | `CreditType`            |

## Manager

The credit type manager is available as the `credit_types`
attribute on the Odoo client object.

```python
>>> from openstack_odooclient import Client as OdooClient
>>> odoo_client = OdooClient(
...     hostname="localhost",
...     port=8069,
...     protocol="jsonrpc",
...     database="odoodb",
...     user="test-user",
...     password="<password>",
... )
>>> odoo_client.credit_types.get(1234)
CreditType(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The credit type manager returns `CreditType` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import CreditType
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `credit_ids`

```python
credit_ids: list[int]
```

A list of IDs for the [credits](credit.md) which are of this credit type.

### `credits`

```python
credits: list[Credit]
```

A list of [credits](credit.md) which are of this credit type.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `name`

```python
name: str
```

Name of the Credit Type.

### `only_for_product_ids`

```python
only_for_product_ids: list[int]
```

A list of IDs for the [products](product.md) this credit applies to.

Mutually exclusive with
[`only_for_product_category_ids`](#only_for_product_category_ids)/[`only_for_product_categories`](#only_for_product_categories).
If none of these values are specified, the credit applies to all products.

### `only_for_products`

```python
only_for_products: list[Product]
```

A list of [products](product.md) which this credit applies to.

Mutually exclusive with
[`only_for_product_category_ids`](#only_for_product_category_ids)/[`only_for_product_categories`](#only_for_product_categories).
If none of these values are specified, the credit applies to all products.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `only_for_product_category_ids`

```python
only_for_product_category_ids: list[int]
```

A list of IDs for the [product categories](product-category.md) this credit applies to.

Mutually exclusive with
[`only_for_product_ids`](#only_for_product_ids)/[`only_for_products`](#only_for_products).
If none of these values are specified, the credit applies to all products.

### `only_for_product_categories`

```python
only_for_product_categories: list[ProductCategory]
```

A list of [product categories](product-category.md) which this credit applies to.

Mutually exclusive with
[`only_for_product_ids`](#only_for_product_ids)/[`only_for_products`](#only_for_products).
If none of these values are specified, the credit applies to all products.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `product_id`

```python
product_id: int
```

The ID of the [product](product.md) to use when applying
the credit to invoices.

### `product_name`

```python
product_name: str
```

The name of the [product](product.md) to use when applying
the credit to invoices.

### `product`

```python
product: Product
```

The [product](product.md) to use when applying the credit to invoices.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `refundable`

```python
refundable: bool
```

Whether or not the credit is refundable.
