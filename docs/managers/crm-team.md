# CRM Teams

This page documents how to use the manager and record objects
for CRM teams.

## Manager

The CRM team manager is available as the `crm_teams`
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
>>> odoo_client.crm_teams.get(1234)
CrmTeam(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The CRM team manager returns `CrmTeam` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import CrmTeam
```

The record class currently implements the following fields and methods.

### `name`

```python
name: str
```

The name of the CRM team.
