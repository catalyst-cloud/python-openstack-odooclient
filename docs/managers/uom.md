# Units of Measure (UoM)

This page documents how to use the manager and record objects
for Units of Measure (UoM).

## Details

| Name            | Value                           |
|-----------------|---------------------------------|
| Odoo Modules    | Units of Measure (UoM), Product |
| Odoo Model Name | `uom.uom`                       |
| Manager         | `uoms`                          |
| Record Type     | `Uom`                           |

## Manager

The Unit of Measure (UoM) manager is available as the `uoms`
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
>>> odoo_client.uoms.get(1234)
Uom(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The Unit of Measure (UoM) manager returns `Uom` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Uom
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `active`

```python
active: bool
```

Whether or not this Unit of Measure is active (enabled).

### `category_id`

```python
category_id: int
```

The ID for the [category](uom-category.md) this Unit of Measure is classified as.

### `category_name`

```python
category_name: str
```

The name of the [category](uom-category.md) this Unit of Measure is classified as.

### `category`

```python
category: UomCategory
```

The [category](uom-category.md) this Unit of Measure is classified as.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `factor`

```python
factor: float
```

How much bigger or smaller this unit is compared to the reference
Unit of Measure (UoM) for the classified category.

### `factor_inv`

```python
factor_inv: float
```

How many times this Unit of Measure is bigger than the reference
Unit of Measure (UoM) for the classified category.

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

The type of category this Unit of Measure (UoM) is classified as.

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

Unit of Measure (UoM) name.

### `uom_type`

```python
uom_type: Literal["bigger", "reference", "smaller"]
```

The type of the Unit of Measure (UoM).

This determines its relationship with other UoMs in the same category.

Values:

* ``bigger`` - Bigger than the reference Unit of Measure
* ``reference`` - Reference Unit of Measure for the selected category
* ``smaller`` - Smaller than the reference Unit of Measure
