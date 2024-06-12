# Partner Categories

This page documents how to use the manager and record objects
for partner categories.

## Manager

The partner category manager is available as the `partner_categories`
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
>>> odoo_client.partner_categories.get(1234)
PartnerCategory(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The partner category manager returns `PartnerCategory` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import PartnerCategory
```

The record class currently implements the following fields and methods.

### `active`

```python
active: bool
```

Whether or not this partner category is active (enabled).

### `child_ids`

```python
child_ids: list[int]
```

A list of IDs for the child categories.

### `children`

```python
children: list[PartnerCategory]
```

The list of child categories.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `color`

```python
color: int
```

Colour index for the partner category.

### `colour`

```python
colour: int
```

Alias for [``color``](#color).

### `name`

```python
name: str
```

The name of the partner category.

### `parent_id`

```python
parent_id: int | None
```

The ID for the parent partner category, if this category
is the child of another category.

### `parent_name`

```python
parent_name: str | None
```

The name of the parent partner category, if this category
is the child of another category.

### `parent`

```python
parent: ParentCategory | None
```

The parent partner category, if this category
is the child of another category.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `parent_path`

```python
parent_path: str | Literal[False]
```

The path of the parent partner category, if there is a parent.

### `partner_ids`

```python
partner_ids: list[int]
```

A list of IDs for the [partners](partner.md) in this category.

### `partners`

```python
partners: list[Partner]
```

The list of [partners](partner.md) in this category.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.
