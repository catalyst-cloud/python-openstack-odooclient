# OpenStack Term Discounts

This page documents how to use the manager and record objects
for term discounts.

## Details

| Name            | Value                     |
|-----------------|---------------------------|
| Odoo Modules    | OpenStack Integration     |
| Odoo Model Name | `openstack.term_discount` |
| Manager         | `term_discounts`          |
| Record Type     | `TermDiscount`            |

## Manager

The term discount manager is available as the `term_discounts`
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
>>> odoo_client.term_discounts.get(1234)
TermDiscount(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The term discount manager returns `TermDiscount` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import TermDiscount
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `discount_percent`

```python
discount_percent: float
```

The maximum discount percentage for this term discount (0-100).

### `early_termination_date`

```python
early_termination_date: date | None
```

An optional early termination date for the term discount.

### `end_date`

```python
end_date: date
```

The date that the term discount expires on.

### `min_commit`

```python
min_commit: float
```

The minimum commitment for this term discount to apply.

### `partner_id`

```python
partner_id: int
```

The ID for the [partner](partner.md) that receives this term discount.

### `partner_name`

```python
partner_name: str
```

The name of the [partner](partner.md) that receives this term discount.

### `partner`

```python
partner: Partner
```

The [partner](partner.md) that receives this term discount.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `project_id`

```python
project_id: int | None
```

The ID for the [project](project.md) this term discount applies to,
if it is a project-specific term discount.

If not set, the term discount applies to all projects
the partner owns.

### `project_name`

```python
project_name: str | None
```

The name of the [project](project.md) this term discount applies to,
if it is a project-specific term discount.

If not set, the term discount applies to all projects
the partner owns.

### `project`

```python
project: Project | None
```

The [project](project.md) this term discount applies to,
if it is a project-specific term discount.

If not set, the term discount applies to all projects
the partner owns.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `start_date`

```python
start_date: date
```

The date from which this term discount starts.

### `superseded_by_id`

```python
superseded_by_id: int | None
```

The ID for the term discount that supersedes this one,
if superseded.


### `superseded_by_name`

```python
superseded_by_name: str | None
```

The name of the term discount that supersedes this one,
if superseded.


### `superseded_by`

```python
superseded_by: TermDiscount | None
```

The term discount that supersedes this one,
if superseded.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
