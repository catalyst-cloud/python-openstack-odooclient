# Account Move (Invoice) Lines

This page documents how to use the manager and record objects
for account move (invoice) lines.

## Details

| Name            | Value                             |
|-----------------|-----------------------------------|
| Odoo Modules    | Accounting, OpenStack Integration |
| Odoo Model Name | `account.move.line`               |
| Manager         | `account_move_lines`              |
| Record Type     | `AccountMoveLine`                 |

## Manager

The account move (invoice) line manager is available as the `account_move_lines`
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
>>> odoo_client.account_move_lines.get(1234)
AccountMoveLine(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The account move (invoice) line manager returns `AccountMoveLine` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import AccountMoveLine
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `currency_id`

```python
currency_id: int
```

The ID for the [currency](currency.md) used in this account move (invoice) line.

### `currency_name`

```python
currency_name: str
```

The name of the [currency](currency.md) used in this account move (invoice) line.

### `currency`

```python
currency: Currency
```

The [currency](currency.md) used in this account move (invoice) line.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `line_tax_amount`

```python
line_tax_amount: float
```

Amount charged in tax on the account move (invoice) line.

### `move_id`

```python
move_id: int
```

The ID for the [account move (invoice)](account-move.md) this line is part of.

### `move_name`

```python
move_name: str
```

The name of the [account move (invoice)](account-move.md) this line is part of.

### `move`

```python
move: AccountMove
```

The [account move (invoice)](account-move.md) this line is part of.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `name`

```python
name: str
```

Name of the product charged on the account move (invoice) line.

### `os_project_id`

```python
os_project_id: int | None
```

The ID for the [OpenStack project](project.md) this account move (invoice) line
was generated for.

### `os_project_name`

```python
os_project_name: str | None
```

The name of the [OpenStack project](project.md) this account move (invoice) line
was generated for.

### `os_project`

```python
os_project: Project | None
```

The [OpenStack project](project.md) this account move (invoice) line
was generated for.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `os_region`

```python
os_region: str | Literal[False]
```

The OpenStack region the account move (invoice) line
was created from.

### `os_resource_id`

```python
os_resource_id: str | Literal[False]
```

The OpenStack resource ID for the resource that generated
this account move (invoice) line.

### `os_resource_name`

```python
os_resource_name: str | Literal[False]
```

The name of the OpenStack resource tier or flavour,
as used by services such as Distil for rating purposes.

For example, if this is the account move (invoice) line
for a compute instance, this would be set to the instance's flavour name.

### `os_resource_type`

```python
os_resource_type: str | Literal[False]
```

A human-readable description of the type of resource captured
by this account move (invoice) line.

### `price_subtotal`

```python
price_subtotal: float
```

Amount charged for the product (untaxed) on the
account move (invoice) line.

### `price_unit`

```python
price_unit: float
```

Unit price for the [product](product.md) used on the account move (invoice) line.

### `product_id`

```python
product_id: int
```

The ID for the [product](product.md) charged on the
account move (invoice) line.

### `product_name`

```python
product_name: int
```

The name of the [product](product.md) charged on the
account move (invoice) line.

### `product`

```python
product: Product
```

The [product](product.md) charged on the
account move (invoice) line.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `quantity`

```python
quantity: float
```

Quantity of product charged on the account move (invoice) line.
