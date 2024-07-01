# Tax Groups

This page documents how to use the manager and record objects
for tax groups.

## Details

| Name            | Value               |
|-----------------|---------------------|
| Odoo Modules    | Accounting          |
| Odoo Model Name | `account.tax.group` |
| Manager         | `tax_groups`        |
| Record Type     | `TaxGroup`          |

## Manager

The tax group manager is available as the `tax_groups`
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
>>> odoo_client.tax_groups.get(1234)
TaxGroup(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The tax group manager returns `TaxGroup` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import TaxGroup
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `name`

```python
name: str
```

Name of the tax group.
