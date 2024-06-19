# Pricelists

This page documents how to use the manager and record objects
for pricelists.

## Details

| Name            | Value               |
|-----------------|---------------------|
| Odoo Modules    | Product             |
| Odoo Model Name | `product.pricelist` |
| Manager         | `pricelists`        |
| Record Type     | `Pricelist`         |

## Manager

The partner manager is available as the `pricelists`
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
>>> odoo_client.pricelists.get(1234)
Pricelist(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

The following manager methods are also available, in addition to the standard methods.

### `get_price`

```python
def get_price(
    pricelist: int | Pricelist,
    product: int | Product,
    qty: float,
) -> float
```

Get the price to charge for a given pricelist, product
and quantity.

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
>>> odoo_client.pricelists.get_price(
...     pricelist=1234,  # ID or object
...     product=5678,  # ID or object
...     qty=100,
... )
2.5
```

#### Parameters

| Name        | Type              | Description                                 | Default    |
|-------------|-------------------|---------------------------------------------|------------|
| `pricelist` | `int | Pricelist` | Pricelist to reference (ID or object)       | (required) |
| `product`   | `int | Product`   | Product to get the price for (ID or object) | (required) |
| `qty`       | `float`           | Quantity to charge for                      | (required) |

#### Returns

| Type    | Description     |
|---------|-----------------|
| `float` | Price to charge |

## Record

The partner manager returns `Partner` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Partner
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `active`

```python
active: bool
```

Whether or not this partner is active (enabled).

### `company_id`

```python
company_id: int | None
```

The ID for the [company](company.md) for this pricelist, if set.

### `company_name`

```python
company_name: str | None
```

The name of the [company](company.md) for this pricelist, if set.

### `company`

```python
company: Company | None
```

The [company](company.md) for this pricelist, if set.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `currency_id`

```python
currency_id: int
```

The ID for the [currency](currency.md) used in this pricelist.

### `currency_name`

```python
currency_name: str
```

The name of the [currency](currency.md) used in this pricelist.

### `currency`

```python
currency: Currency
```

The [currency](currency.md) used in this pricelist.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `discount_policy`

```python
discount_policy: Literal["with_discount", "without_discount"]
```

Discount policy for the pricelist.

Values:

* ``with_discount`` - Discount included in the price
* ``without_discount`` - Show public price & discount to the customer

### `name`

```python
name: str
```

The name of this pricelist.

### `get_price`

```python
def get_price(
    product: int | Product,
    qty: float,
) -> float
```

Get the price to charge for a given product and quantity.

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
>>> pricelist = odoo_client.pricelists.get(1234)
>>> pricelist.get_price(
...     product=5678,  # ID or object
...     qty=100,
... )
2.5
```

#### Parameters

| Name        | Type               | Description                                 | Default    |
|-------------|--------------------|---------------------------------------------|------------|
| `product`   | `int | Product`   | Product to get the price for (ID or object) | (required) |
| `qty`       | `float`            | Quantity to charge for                      | (required) |

#### Returns

| Type    | Description     |
|---------|-----------------|
| `float` | Price to charge |
