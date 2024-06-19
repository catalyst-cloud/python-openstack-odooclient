# OpenStack Project Contacts

This page documents how to use the manager and record objects
for project contacts.

## Details

| Name            | Value                       |
|-----------------|-----------------------------|
| Odoo Modules    | OpenStack Integration       |
| Odoo Model Name | `openstack.project_contact` |
| Manager         | `project_contacts`          |
| Record Type     | `ProjectContact`            |

## Manager

The project contact manager is available as the `project_contacts`
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
>>> odoo_client.project_contacts.get(1234)
ProjectContact(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The project contact manager returns `ProjectContact` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import ProjectContact
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `contact_type`

```python
contact_type: Literal[
    "primary",
    "billing",
    "technical",
    "legal",
    "reseller customer",
]
```

The contact type to assign the partner as on the project.

### `inherit`

```python
inherit: bool
```

Whether or not this contact should be inherited by child projects.

### `partner_id`

```python
partner_id: int
```

The ID for the [partner](partner.md) linked to this project contact.

### `partner_name`

```python
partner_name: str
```

The name of the [partner](partner.md) linked to this project contact.

### `partner`

```python
partner: Partner
```

The [partner](partner.md) linked to this project contact.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `project_id`

```python
project_id: int | None
```

The ID for the [project](project.md) this contact is linked to, if set.

### `project_name`

```python
project_name: str | None
```

The name of the [project](project.md) this contact is linked to, if set.

### `project`

```python
project: Project | None
```

The [project](project.md) this contact is linked to, if set.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
