# Unit of Measure (UoM) Categories

This page documents how to use the manager and record objects
for Unit of Measure (UoM) categories.

## Details

| Name            | Value                  |
|-----------------|------------------------|
| Odoo Modules    | Units of Measure (UoM) |
| Odoo Model Name | `uom.uom.category`     |
| Manager         | `uom_categories`       |
| Record Type     | `UomCategory`          |

## Manager

The Unit of Measure (UoM) category manager is available as the `uom_categories`
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
>>> odoo_client.uom_categories.get(1234)
UomCategory(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The Unit of Measure (UoM) category manager returns `UomCategory` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import UomCategory
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `measure_type`

```python
measure_type: Literal[
    "unit",
    "weight",
    "working_time",
    "length",
    "volume",
]
```

The type of Unit of Measure (UoM) category.

This field no longer exists from Odoo 14 onwards.

Values:

* ``unit`` - Default Units
* ``weight`` - Default Weight
* ``working_time`` - Default Working Time
* ``length`` - Default Length
* ``volume`` - Default Volume

### `name`

```python
name: str
```

The name of the Unit of Measure (UoM) category.
