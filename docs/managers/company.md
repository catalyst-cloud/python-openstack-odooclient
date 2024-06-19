# Companies

This page documents how to use the manager and record objects
for companies.

## Details

| Name            | Value                |
|-----------------|----------------------|
| Odoo Modules    | Base, Product, Sales |
| Odoo Model Name | `res.company`        |
| Manager         | `companies`          |
| Record Type     | `Company`            |

## Manager

The company manager is available as the `companies`
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
>>> odoo_client.companies.get(1234)
Company(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The company manager returns `Company` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Company
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

#### `active`

```python
active: bool
```

Whether or not this company is active (enabled).

#### `child_ids`

```python
child_ids: list[int]
```

A list of IDs for the child companies.

#### `children`

```python
children: list[Company]
```

The list of child companies.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

#### `name`

```python
name: str
```

Company name, set from the partner name.

#### `parent_id`

```python
parent_id: int | None
```

The ID for the parent company, if this company
is the child of another company.

#### `parent_name`

```python
parent_name: str | None
```

The name of the parent company, if this company
is the child of another company.

#### `parent`

```python
parent: Company | None
```

The parent company, if this company
is the child of another company.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

#### `parent_path`

```python
parent_path: str | Literal[False]
```

The path of the parent company, if there is a parent.

#### `partner_id`

```python
partner_id: int
```

The ID for the partner for the company.

#### `partner_name`

```python
partner_name: str
```

The name of the partner for the company.

#### `partner`

```python
partner: Partner
```

The partner for the company.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
