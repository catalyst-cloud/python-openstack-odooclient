# Users

This page documents how to use the manager and record objects
for users.

## Details

| Name            | Value            |
|-----------------|------------------|
| Odoo Modules    | Base, Accounting |
| Odoo Model Name | `res.users`      |
| Manager         | `users`          |
| Record Type     | `User`           |

## Manager

The user manager is available as the `users`
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
>>> odoo_client.users.get(1234)
User(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The user manager returns `User` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import User
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `active`

```python
active: bool
```

Whether or not this user is active (enabled).

### `active_partner`

```python
active_partner: bool
```

Whether or not the [partner](partner.md) this user is associated with is active.

### `company_id`

```python
company_id: int
```

The ID for the default [company](company.md) this user is logged in as.

### `company_name`

```python
company_name: str
```

The name of the default [company](company.md) this user is logged in as.

### `company`

```python
company: Company
```

The default [company](company.md) this user is logged in as.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `name`

```python
name: str
```

User name.

### `partner_id`

```python
partner_id: int
```

The ID for the [partner](partner.md) that this user is associated with.

### `partner_name`

```python
partner_name: str
```

The name of the [partner](partner.md) that this user is associated with.

### `partner`

```python
partner: Partner
```

The [partner](partner.md) that this user is associated with.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
