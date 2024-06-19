# OpenStack Grants

This page documents how to use the manager and record objects
for grants.

## Details

| Name            | Value                 |
|-----------------|-----------------------|
| Odoo Modules    | OpenStack Integration |
| Odoo Model Name | `openstack.grant`     |
| Manager         | `grants`              |
| Record Type     | `Grant`               |

## Manager

The grant manager is available as the `grants`
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
>>> odoo_client.grants.get(1234)
Grant(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The grant manager returns `Grant` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Grant
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `expiry_date`

```python
expiry_date: date
```

The date the grant expires.

### `grant_type_id`

```python
grant_type_id: int
```

The ID of the [type of this grant](grant-type.md).

### `grant_type_name`

```python
grant_type_name: str
```

The name of the [type of this grant](grant-type.md).

### `grant_type`

```python
grant_type: GrantType
```

The [type of this grant](grant-type.md).

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `name`

```python
name: str
```

The automatically generated name of the grant.

### `start_date`

```python
start_date: date
```

The start date of the grant.

### `value`

```python
value: float
```

The value of this grant.

### `voucher_code_id`

```python
voucher_code_id: int | None
```

The ID of the [voucher code](voucher-code.md) used when applying for the grant,
if one was supplied.

### `voucher_code_name`

```python
voucher_code_name: str | None
```

The name of the [voucher code](voucher-code.md) used when applying for the grant,
if one was supplied.

### `voucher_code`

```python
voucher_code: VoucherCode | None
```

The [voucher code](voucher-code.md) used when applying for the grant,
if one was supplied.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
