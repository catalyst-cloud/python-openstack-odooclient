# OpenStack Resellers

This page documents how to use the manager and record objects
for resellers.

## Details

| Name            | Value                 |
|-----------------|-----------------------|
| Odoo Modules    | OpenStack Integration |
| Odoo Model Name | `openstack.reseller`  |
| Manager         | `resellers`           |
| Record Type     | `Reseller`            |

## Manager

The reseller manager is available as the `resellers`
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
>>> odoo_client.resellers.get(1234)
Reseller(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The reseller manager returns `Reseller` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Reseller
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `alternative_billing_url`

```python
alternative_billing_url: str | None
```

The URL to the cloud billing page for the reseller, if available.

### `alternative_support_url`

```python
alternative_support_url: str | None
```

The URL to the cloud support centre for the reseller, if available.

### `demo_project_id`

```python
demo_project_id: int | None
```

The ID for the optional demo [project](project.md) belonging to the reseller.

### `demo_project_name`

```python
demo_project_name: str | None
```

The name of the optional demo project belonging to the reseller.

### `demo_project`

```python
demo_project: Project | None
```

An optional demo [project](project.md) belonging to the reseller.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `hide_billing`

```python
hide_billing: bool
```

Whether or not the billing URL should be hidden.

### `hide_support`

```python
hide_support: bool
```

Whether or not the support URL should be hidden.

### `name`

```python
name: str
```

The automatically generated reseller name.

This is set to the [reseller partner's](#partner) name.

### `partner_id`

```python
partner_id: int
```

The ID for the reseller [partner](partner.md).

### `partner_name`

```python
partner_name: str
```

The name of the reseller [partner](partner.md).

### `partner`

```python
partner: Partner
```

The reseller [partner](partner.md).

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `tier_id`

```python
tier_id: int
```

The ID for the [tier](reseller-tier.md) this reseller is under.

### `tier_name`

```python
tier_name: str
```

The name of the [tier](reseller-tier.md) this reseller is under.

### `tier`

```python
tier: ResellerTier
```

The [tier](reseller-tier.md) this reseller is under.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
