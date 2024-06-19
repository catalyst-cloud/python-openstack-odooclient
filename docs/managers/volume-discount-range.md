# OpenStack Volume Discount Ranges

This page documents how to use the manager and record objects
for volume discount ranges.

## Details

| Name            | Value                             |
|-----------------|-----------------------------------|
| Odoo Modules    | OpenStack Integration             |
| Odoo Model Name | `openstack.volume_discount_range` |
| Manager         | `volume_discount_ranges`          |
| Record Type     | `VolumeDiscountRange`             |

## Manager

The volume discount range manager is available as the `volume_discount_ranges`
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
>>> odoo_client.volume_discount_ranges.get(1234)
VolumeDiscountRange(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

The following manager methods are also available, in addition to the standard methods.

### `get_for_charge`

```python
get_for_charge(
    charge: float,
    customer_group: int | CustomerGroup | None = None,
) -> VolumeDiscountRange | None
```

Return the volume discount range to apply to a given charge.

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
>>> odoo_client.volume_discount_ranges.get_for_charge(1000)
VolumeDiscountRange(record={'id': 1234, 'min': 500, ...}, fields=None)
```

If ``customer_group`` is supplied, volume discount ranges for
a specific customer group are returned. When set to ``None``
(the default), volume discount ranges for all customers are returned.

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
>>> odoo_client.volume_discount_ranges.get_for_charge(1000, customer_group=5678)
VolumeDiscountRange(record={'id': 9012, 'customer_group': [5678, 'Customer Group'], 'min': 500, ...}, fields=None)
```

If multiple volume discount ranges can be applied, the range with
the highest discount percentage is selected.
If no applicable volume discount ranges were found,
``None`` is returned.

#### Parameters

| Name             | Type                           | Description                                               | Default    |
|------------------|--------------------------------|-----------------------------------------------------------|------------|
| `charge`         | `float`                        | The charge to find the applicable discount range for      | (required) |
| `customer_group` | `int | CustomerGroup | None` | Get discount for a specific customer group (ID or object) | `None`     |

#### Returns

| Type                  | Description                                                    |
|-----------------------|----------------------------------------------------------------|
| `VolumeDiscountRange` | Highest percentage applicable volume discount range (if found) |
| `None`                | If no applicable volume discount range was found               |

## Record

The volume discount range manager returns `VolumeDiscountRange` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import VolumeDiscountRange
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `customer_group_id`

```python
customer_group_id: int | None
```

The ID for the [customer group](customer-group.md) this volume discount range
applies to, if a specific customer group is set.

If no customer group is set, this volume discount range
applies to all customers.

### `customer_group_name`

```python
customer_group_name: str | None
```

The name of the [customer group](customer-group.md) this volume discount range
applies to, if a specific customer group is set.

If no customer group is set, this volume discount range
applies to all customers.

### `customer_group`

```python
customer_group: CustomerGroup | None
```

The [customer group](customer-group.md) this volume discount range
applies to, if a specific customer group is set.

If no customer group is set, this volume discount range
applies to all customers.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `discount_percent`

```python
discount_percent: float
```

Discount percentage of this volume discount range (0-100).

### `name`

```python
name: str
```

The automatically generated name (description) of
this volume discount range.

### `max`

```python
max: float | None
```

Optional maximum charge for this volume discount range.

Intended to be used when creating tiered volume discounts for customers.

### `min`

```python
min: float
```

Minimum charge for this volume discount range.

### `use_max`

```python
use_max: bool
```

Use the [``max``](#max) field, if defined.
