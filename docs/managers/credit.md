# OpenStack Credits

This page documents how to use the manager and record objects
for credits.

## Details

| Name            | Value                 |
|-----------------|-----------------------|
| Odoo Modules    | OpenStack Integration |
| Odoo Model Name | `openstack.credit`    |
| Manager         | `credits`             |
| Record Type     | `Credit`              |

## Manager

The credit manager is available as the `credits`
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
>>> odoo_client.credits.get(1234)
Credit(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The credit manager returns `Credit` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Credit
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `credit_type_id`

```python
credit_type_id: int
```

The ID of the [type of this credit](credit-type.md).

### `credit_type_name`

```python
credit_type_name: str
```

The name of the [type of this credit](credit-type.md).

### `credit_type`

```python
credit_type: CreditType
```

The [type of this credit](credit-type.md).

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `current_balance`

```python
current_balance: float
```

The current remaining balance on the credit.

### `expiry_date`

```python
expiry_date: date
```

The date the credit expires.

### `initial_balance`

```python
initial_balance: float
```

The initial balance this credit started off with.

### `name`

```python
name: str
```

The automatically generated name of the credit.

### `start_date`

```python
start_date: date
```

The start date of the credit.

### `transaction_ids`

```python
transaction_ids: list[int]
```

A list of IDs for the [transactions](credit-transaction.md) that have been made
using this credit.

### `transactions`

```python
transactions: list[CreditTransaction]
```

The [transactions](credit-transaction.md) that have been made using this credit.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.


### `voucher_code_id`

```python
voucher_code_id: int | None
```

The ID of the [voucher code](voucher-code.md) used when applying for the credit,
if one was supplied.

### `voucher_code_name`

```python
voucher_code_name: str | None
```

The name of the [voucher code](voucher-code.md) used when applying for the credit,
if one was supplied.

### `voucher_code`

```python
voucher_code: VoucherCode | None
```

The [voucher code](voucher-code.md) used when applying for the credit,
if one was supplied.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
