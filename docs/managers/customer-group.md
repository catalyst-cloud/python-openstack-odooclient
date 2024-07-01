# OpenStack Customer Groups

This page documents how to use the manager and record objects
for customer groups.

## Details

| Name            | Value                      |
|-----------------|----------------------------|
| Odoo Modules    | OpenStack Integration      |
| Odoo Model Name | `openstack.customer_group` |
| Manager         | `customer_groups`          |
| Record Type     | `CustomerGroup`            |

## Manager

The customer group manager is available as the `customer_groups`
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
>>> odoo_client.customer_groups.get(1234)
CustomerGroup(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The customer group manager returns `CustomerGroup` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import CustomerGroup
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `name`

```python
name: str
```

The name of the customer group.

### `partner_ids`

```python
partner_ids: list[int]
```

A list of IDs for the [partners](partner.md) that are part
of this customer group.

### `partners`

```python
partners: list[partner.Partner]
```

The [partners](partner.md) that are part of this customer group.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `pricelist_id`

```python
pricelist_id: int | None
```

The ID for the [pricelist](pricelist.md) this customer group uses,
if not the default one.

### `pricelist_name`

```python
pricelist_name: str | None
```

The name of the [pricelist](pricelist.md) this customer group uses,
if not the default one.

### `pricelist`

```python
pricelist: Pricelist | None
```

The [pricelist](pricelist.md) this customer group uses, if not the default one.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
