# Fiscal Position Tax Mappings

*Added in version 0.2.4.*

This page documents how to use the manager and record objects
for fiscal position tax mappings.

## Details

| Name            | Value                          |
|-----------------|--------------------------------|
| Odoo Modules    | Accounting                     |
| Odoo Model Name | `account.fiscal.position.tax`  |
| Manager         | `fiscal_position_tax_mappings` |
| Record Type     | `FiscalPositionTaxMapping`     |

## Manager

The fiscal position tax mapping manager is available as the `fiscal_position_tax_mappings`
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
>>> odoo_client.fiscal_position_tax_mappings.get(1234)
FiscalPositionTaxMapping(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The fiscal position tax mapping manager returns `FiscalPositionTaxMapping` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import FiscalPositionTaxMapping
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `company_id`

```python
company_id: int
```

The ID for the [company](company.md) this fiscal position tax mapping
is associated with.

### `company_name`

```python
company_name: str
```

The name of the [company](company.md) this fiscal position tax mapping
is associated with.

### `company`

```python
company: Company
```

The [company](company.md) this fiscal position tax mapping
is associated with.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `position_id`

```python
position_id: int
```

The ID for the [fiscal position](fiscal-position.md) this mapping is part of.

### `position_name`

```python
position_name: str
```

The name of the [fiscal position](fiscal-position.md) this mapping is part of.

### `position`

```python
position: FiscalPosition
```

The [fiscal position](fiscal-position.md) this mapping is part of.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `tax_src_id`

```python
tax_src_id: int
```

The ID of the [tax](tax.md) to be overridden on products.

### `tax_src_name`

```python
tax_src_name: str
```

The name of the [tax](tax.md) to be overridden on products.

### `tax_src`

```python
tax_src: Tax
```

The [tax](tax.md) to be overridden on products.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `tax_dest_id`

```python
tax_dest_id: int | None
```

The ID of the [tax](tax.md) to override the source tax with, if set.

### `tax_dest_name`

```python
tax_dest_name: str | None
```

The name of the [tax](tax.md) to override the source tax with, if set.

### `tax_dest`

```python
tax_dest: Tax | None
```

The [tax](tax.md) to override the source tax with, if set.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
