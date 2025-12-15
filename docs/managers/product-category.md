# Product Categories

This page documents how to use the manager and record objects
for product categories.

## Details

| Name            | Value                |
|-----------------|----------------------|
| Odoo Modules    | Product, Accounting  |
| Odoo Model Name | `product.category`   |
| Manager         | `product_categories` |
| Record Type     | `ProductCategory`    |

## Manager

The product category manager is available as the `product_categories`
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
>>> odoo_client.product_categories.get(1234)
ProductCategory(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The product category manager returns `ProductCategory` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import ProductCategory
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `child_id`

```python
child_id: list[int]
```

A list of IDs for the child categories.

### `child_ids`

```python
child_ids: list[int]
```

An alias for [`child_id`](#child_id).

### `children`

```python
children: list[ProductCategory]
```

The list of child categories.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `complete_name`

```python
complete_name: str
```

The complete product category tree.

### `name`

```python
name: str
```

The name of the product category.

Not guaranteed to be unique, even under the same parent category.

### `parent_id`

```python
parent_id: int | None
```

The ID for the parent product category, if this category
is the child of another category.

### `parent_id`

```python
parent_name: str | None
```

The name of the parent product category, if this category
is the child of another category.

### `parent`

```python
parent: ProductCategory | None
```

The parent product category, if this category
is the child of another category.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `parent_path`

```python
parent_path: str | Literal[False]
```

The path of the parent product category, if there is a parent.

### `product_count`

```python
product_count: int
```

The number of products under this category.
