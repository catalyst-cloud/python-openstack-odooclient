# Fiscal Positions

*Added in version 0.2.4.*

This page documents how to use the manager and record objects
for fiscal positions.

## Details

| Name            | Value                     |
|-----------------|---------------------------|
| Odoo Modules    | Accounting, Point of Sale |
| Odoo Model Name | `account.fiscal.position` |
| Manager         | `fiscal_positions`        |
| Record Type     | `FiscalPosition`          |

## Manager

The fiscal position manager is available as the `fiscal_positions`
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
>>> odoo_client.fiscal_positions.get(1234)
FiscalPosition(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The fiscal position manager returns `FiscalPosition` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import FiscalPosition
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `active`

```python
active: bool
```

Whether or not this fiscal position is active (enabled).

### `company_id`

```python
company_id: int
```

The ID for the [company](company.md) this fiscal position is associated with.

### `company_name`

```python
company_name: str
```

The name of the [company](company.md) this fiscal position is associated with.

### `company`

```python
company: Company
```

The [company](company.md) this fiscal position is associated with.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `name`

```python
name: str
```

The name of the fiscal position.

Not guaranteed to be unique.

### `tax_ids`

```python
tax_ids: list[int]
```

The list of IDs for the [tax mappings](fiscal-position-tax-mapping.md) that will be applied
to sale orders and invoices for partners using this
fiscal position.

### `taxes`

```python
taxes: list[FiscalPositionTaxMapping]
```

The list of [tax mappings](fiscal-position-tax-mapping.md) that will be applied
to sale orders and invoices for partners using this
fiscal position.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.
