# OpenStack Reseller Tiers

This page documents how to use the manager and record objects
for reseller tiers.

## Details

| Name            | Value                     |
|-----------------|---------------------------|
| Odoo Modules    | OpenStack Integration     |
| Odoo Model Name | `openstack.reseller.tier` |
| Manager         | `reseller_tiers`          |
| Record Type     | `ResellerTier`            |

## Manager

The reseller tier manager is available as the `reseller_tiers`
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
>>> odoo_client.reseller_tiers.get(1234)
ResellerTier(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The reseller tier manager returns `ResellerTier` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import ResellerTier
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `discount_percent`

```python
discount_percent: float
```

The maximum discount percentage for this reseller tier (0-100).

### `discount_product_id`

```python
discount_product_id: int
```

The ID of the discount [product](product.md) for the reseller tier.

### `discount_product_name`

```python
discount_product_name: str
```

The name of the discount [product](product.md) for the reseller tier.

### `discount_product`

```python
discount_product: Product
```

The discount [product](product.md) for the reseller tier.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `free_monthly_credit`

```python
free_monthly_credit: float
```

The amount the reseller gets monthly in credit for demo projects.

### `free_monthly_credit_product_id`

```python
free_monthly_credit_product_id: int
```

The ID of the [product](product.md) to use when adding the free monthly credit
to demo project invoices.

### `free_monthly_credit_product_name`

```python
free_monthly_credit_product_name: str
```

The name of the [product](product.md) to use when adding the free monthly credit
to demo project invoices.

### `free_monthly_credit_product`

```python
free_monthly_credit_product: Product
```

The [product](product.md) to use when adding the free monthly credit
to demo project invoices.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `free_support_hours`

```python
free_support_hours: int
```

The amount of free support hours the reseller is entitled to
under this tier.

### `name`

```python
name: str
```

Reseller tier name.

### `name`

```python
min_usage_threshold: float
```

The minimum required usage amount for the reseller tier.
