# Products

This page documents how to use the manager and record objects
for products.

## Details

| Name            | Value                      |
|-----------------|----------------------------|
| Odoo Modules    | Product, Accounting, Sales |
| Odoo Model Name | `product.product`          |
| Manager         | `products`                 |
| Record Type     | `Product`                  |

## Manager

The product manager is available as the `products`
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
>>> odoo_client.products.get(1234)
Product(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

The following manager methods are also available, in addition to the standard methods.

### `get_sellable_company_products`

```python
get_sellable_company_products(
    company: int | Company,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = False,
) -> list[Product]
```

```python
get_sellable_company_products(
    company: int | Company,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = True,
    as_dict: bool = False,
) -> list[int]
```

```python
get_sellable_company_products(
    company: int | Company,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = True,
) -> list[dict[str, Any]]
```

Fetch a list of active and saleable products for the given company.

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
>>> odoo_client.products.get_sellable_company_products(
...     company=1234,  # ID or object
... )
[Product(record={'id': 5678, ...}, fields=None), ...]
```

#### Parameters

| Name      | Type                   | Description                                       | Default    |
|-----------|------------------------|---------------------------------------------------|------------|
| `company` | `int | Company`        | The company to search for products (ID or object) | (required) |
| `fields`  | `Iterable[str] | None` | Fields to select, defaults to `None` (select all) | `None`     |
| `order`   | `str | None`           | Order results by a specific field                 | `None`     |
| `as_id`   | `bool`                 | Return the record IDs only                        | `False`    |
| `as_dict` | `bool`                 | Return records as dictionaries                    | `False`    |

#### Returns

| Type                   | Description                                             |
|------------------------|---------------------------------------------------------|
| `list[Product]`        | List of product objects (default)                       |
| `list[int]`            | List of product IDs (when `as_id` is `True`)            |
| `list[dict[str, Any]]` | List of product dictionaries (when `as_dict` is `True`) |

### `get_sellable_company_product_by_name`

```python
get_sellable_company_product_by_name(
    company: int | Company,
    name: str,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = False,
    optional: bool = False,
) -> Product
```

```python
get_sellable_company_product_by_name(
    company: int | Company,
    name: str,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = False,
    optional: bool = True,
) -> Product | None
```

```python
get_sellable_company_product_by_name(
    company: int | Company,
    name: str,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = True,
    as_dict: bool = False,
    optional: bool = False,
) -> int
```

```python
get_sellable_company_product_by_name(
    company: int | Company,
    name: str,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = True,
    as_dict: bool = False,
    optional: bool = True,
) -> int | None
```

```python
get_sellable_company_product_by_name(
    company: int | Company,
    name: str,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = True,
    optional: bool = False,
) -> dict[str, Any]
```

```python
get_sellable_company_product_by_name(
    company: int | Company,
    name: str,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = True,
    optional: bool = True,
) -> dict[str, Any] | None
```

Query a unique product for the given company by name.

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
>>> odoo_client.products.get_sellable_company_product_by_name(
...     company=1234,
...     name="RegionOne.m1.small",
... )
Product(record={'id': 5678, 'name': 'RegionOne.m1.small', ...}, fields=None)
```

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

#### Parameters

| Name       | Type                   | Description                                       | Default    |
|------------|------------------------|---------------------------------------------------|------------|
| `company`  | `int | Company`        | The company to search for products (ID or object) | (required) |
| `name`     | `str`                  | The product name                                  | (required) |
| `fields`   | `Iterable[str] | None` | Fields to select, defaults to `None` (select all) | `None`     |
| `as_id`    | `bool`                 | Return a record ID                                | `False`    |
| `as_dict`  | `bool`                 | Return the record as a dictionary                 | `False`    |
| `optional` | `bool`                 | Return `None` if not found                        | `False`    |

#### Raises

| Type                        | Description                                                       |
|-----------------------------|-------------------------------------------------------------------|
| `MultipleRecordsFoundError` | Multiple records with the same name were found                    |
| `RecordNotFoundError`       | Record with the given name not found (when `optional` is `False`) |

#### Returns

| Type             | Description                                                                |
|------------------|----------------------------------------------------------------------------|
| `Product`        | Product object (default)                                                   |
| `int`            | Product ID (when `as_id` is `True`)                                        |
| `dict[str, Any]` | Product dictionary (when `as_dict` is `True`)                              |
| `None`           | If a product with the given name was not found (when `optional` is `True`) |

## Record

The product manager returns `Product` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Product
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `active`

```python
active: bool
```

Whether or not this product is active (enabled).

*Added in version 0.2.1.*

### `categ_id`

```python
categ_id: int
```

The ID for the [category](product-category.md) this product is under.

### `categ_name`

```python
categ_name: str
```

The name of the [category](product-category.md) this product is under.

### `categ`

```python
categ: ProductCategory
```

The [category](product-category.md) this product is under.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `company_id`

```python
company_id: int | None
```

The ID for the [company](company.md) that owns this product, if set.

### `company_name`

```python
company_name: str | None
```

The name of the [company](company.md) that owns this product, if set.

### `company`

```python
company: Company | None
```

The [company](company.md) that owns this product, if set.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `default_code`

```python
default_code: str | Literal[False]
```

The Default Code for this product, if set.

In the OpenStack Integration add-on, this is used to store
the rated unit for the service product.

*Changed in version 0.2.1*: Made `default_code` optional.

### `description`

```python
description: str
```

A short description of this product.

### `display_name`

```python
display_name: str
```

The name of this product in OpenStack, and on invoices.

### `list_price`

```python
list_price: float
```

The list price of the product.

This becomes the unit price of the product on invoices.

### `name`

```python
name: str
```

The name of the product.

### `sale_ok`

```python
sale_ok: bool
```

Whether or not this product is sellable.

*Added in version 0.2.1.*

### `uom_id`

```python
uom_id: int
```

The ID for the [Unit of Measure](uom.md) for this product.

### `uom_name`

```python
uom_name: str
```

The name of the [Unit of Measure](uom.md) for this product.

### `uom`

```python
uom: Uom
```

The [Unit of Measure](uom.md) for this product.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
