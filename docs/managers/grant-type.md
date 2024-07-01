# OpenStack Grant Types

This page documents how to use the manager and record objects
for grant types.

## Details

| Name            | Value                  |
|-----------------|------------------------|
| Odoo Modules    | OpenStack Integration  |
| Odoo Model Name | `openstack.grant.type` |
| Manager         | `grant_types`          |
| Record Type     | `GrantType`            |

## Manager

The grant type manager is available as the `grant_types`
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
>>> odoo_client.grant_types.get(1234)
GrantType(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The grant type manager returns `GrantType` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import GrantType
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `grant_ids`

```python
grant_ids: list[int]
```

A list of IDs for the [grants](grant.md) which are of this grant type.

### `grants`

```python
grants: list[Grant]
```

A list of [grants](grant.md) which are of this grant type.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `name`

```python
name: str
```

Name of the Grant Type.

### `only_for_product_ids`

```python
only_for_product_ids: list[int]
```

A list of IDs for the [products](product.md) this grant applies to.

Mutually exclusive with [`only_for_product_category_ids`](#only_for_product_category_ids).
If neither are specified, the grant applies to all products.

### `only_for_products`

```python
only_for_products: list[Product]
```

A list of [products](product.md) which this grant applies to.

Mutually exclusive with [`only_for_product_categories`](#only_for_product_categories).
If neither are specified, the grant applies to all products.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `only_for_product_category_ids`

```python
only_for_product_category_ids: list[int]
```

A list of IDs for the [product categories](product-category.md) this grant applies to.

Mutually exclusive with [`only_for_product_ids`](#only_for_product_ids).
If neither are specified, the grant applies to all product
categories.

### `only_for_product_categories`

```python
only_for_product_categories: list[ProductCategory]
```

A list of [product categories](product-category.md) which this grant applies to.

Mutually exclusive with [`only_for_products`](#only_for_products).
If neither are specified, the grant applies to all product
categories.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `only_on_group_root`

```python
only_on_group_root: bool
```

When set to ``True``, this grant type is only allowed to be
part of an invoice grouping if it is on the group root project.

### `product_id`

```python
product_id: int
```

The ID of the [product](product.md) to use when applying
the grant to invoices.

### `product_name`

```python
product_name: str
```

The name of the [product](product.md) to use when applying
the grant to invoices.

### `product`

```python
product: Product
```

The [product](product.md) to use when applying the grant to invoices.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
