# Project Contacts

This page documents how to use the manager and record objects
for project contacts.

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
