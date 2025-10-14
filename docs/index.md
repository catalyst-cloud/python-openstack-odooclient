# OpenStack Odoo Client Library for Python

[![PyPI](https://img.shields.io/pypi/v/openstack-odooclient)](https://pypi.org/project/openstack-odooclient) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openstack-odooclient) [![GitHub](https://img.shields.io/github/license/catalyst-cloud/python-openstack-odooclient)](https://github.com/catalyst-cloud/python-openstack-odooclient/blob/main/LICENSE) ![Test Status](https://img.shields.io/github/actions/workflow/status/catalyst-cloud/python-openstack-odooclient/test.yml?label=tests)

This is an Odoo client library for Python with support for the
[OpenStack Integration add-on](https://github.com/catalyst-cloud/odoo-openstack-integration),
intended to be used by OpenStack projects such as
[Distil](https://github.com/catalyst-cloud/distil).

This library provides a higher level interface than [OdooRPC](https://pythonhosted.org/OdooRPC)
(which is used internally), and is intended to make it possible to develop applications against
a well-defined API, without having to take into account considerations such as backward-incompatible
changes between Odoo versions.

## Installation

The OpenStack Odoo Client library supports Python 3.10 and later.

To install the library package, simply install the
[`openstack-odooclient`](https://pypi.org/project/openstack-odooclient)
package using `pip`.

```bash
python -m pip install openstack-odooclient
```

## Connecting to Odoo

To connect to an Odoo server, create an `openstack_odooclient.Client` object and
pass the connection details to it.

```python
openstack_odooclient.Client(
    *,
    hostname: str,
    database: str,
    username: str,
    password: str,
    protocol: str = "jsonrpc",
    port: int = 8069,
    verify: bool | str | Path = True,
    version: str | None = None,
) -> Client
```

This is the recommended way of creating the Odoo client object,
as it provides some extra parameters for convenience.

```python
from openstack_odooclient import Client as OdooClient

odoo_client = OdooClient(
    hostname="localhost",
    database="odoodb",
    user="test-user",
    password="<password>",
    protocol="jsonrpc",  # HTTP, or "jsonrpc+ssl" for HTTPS.
    port=8069,
    # verify=True,  # Enable/disable SSL verification, or pass the path to a CA certificate.
    # version="14.0",  # Optionally specify the server version. Default is to auto-detect.
)
```

If you have a pre-existing `odoorpc.ODOO` connection object, that can instead
be passed directly into `openstack_odooclient.Client`.

```python
openstack_odooclient.Client(*, odoo: odoorpc.ODOO) -> Client
```

This allows for sharing a single OdooRPC connection object with other code.

```python
from odoorpc import ODOO
from openstack_odooclient import Client as OdooClient

odoo = ODOO(
    host="localhost",
    port=8069,
    protocol="jsonrpc",  # HTTP, or "jsonrpc+ssl" for HTTPS.
    # version="14.0",  # Optionally specify the server version. Default is to auto-detect.
)
odoo.login("odoodb", "test-user", "<password>")

odoo_client = OdooClient(odoo=odoo)
```

## Managers

The Odoo client object exposes a number of record managers, which contain methods
used to query specific record types, or create one or more new records of that type.

For example, performing a simple search query would look something like this:

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
>>> odoo_client.users.search([("id", "=", odoo_client.user_id)], as_id=True)
[1234]
```

For more information on the available managers and their functions, see [Managers](managers/index.md).

## Records

Record manager methods return record objects for the corresponding model
in Odoo.

Record fields can be accessed as attributes on these record objects.
The record classes are fully type hinted, allowing IDEs and validation
tools such as Mypy to verify that your application is using the fields
correctly.

```python
>>> from openstack_odooclient import Client as OdooClient, User
>>> user: User | None = None
>>> odoo_client = OdooClient(
...     hostname="localhost",
...     port=8069,
...     protocol="jsonrpc",
...     database="odoodb",
...     user="test-user",
...     password="<password>",
... )
>>> user = odoo_client.users.get(1234)
>>> user
User(record={'id': 1234, ...}, fields=None)
>>> user.id
1234
```

For more information on record objects, see [Records](managers/index.md#records).
