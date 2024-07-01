# OpenStack Credit Transactions

This page documents how to use the manager and record objects
for credit transactions.

## Details

| Name            | Value                          |
|-----------------|--------------------------------|
| Odoo Modules    | OpenStack Integration          |
| Odoo Model Name | `openstack.credit.transaction` |
| Manager         | `credit_transactions`          |
| Record Type     | `CreditTransaction`            |

## Manager

The credit transaction manager is available as the `credit_transactions`
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
>>> odoo_client.credit_transactions.get(1234)
CreditTransaction(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The credit transaction manager returns `CreditTransaction` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import CreditTransaction
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `credit_id`

```python
credit_id: int
```

The ID of the [credit](credit.md) this transaction was made against.

### `credit_name`

```python
credit_name: str
```

The name of the [credit](credit.md) this transaction was made against.

### `credit`

```python
credit: Credit
```
The [credit](credit.md) this transaction was made against.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `description`

```python
description: str
```

A description of this credit transaction.

### `value`

```python
value: float
```

The value of the credit transaction.
