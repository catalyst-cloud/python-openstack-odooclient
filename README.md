# OpenStack Odoo Client library for Python

This is an Odoo client library for Python with support for the
[OpenStack Integration add-on](https://github.com/catalyst-cloud/odoo-openstack-integration),
intended to be used by OpenStack projects such as
[Distil](https://github.com/catalyst-cloud/distil).

This library provides a higher level interface than [OdooRPC](https://pythonhosted.org/OdooRPC)
(which is used internally), and is intended to make it possible to develop applications against
a common API, without having to take into account considerations such as backward-incompatible
changes between Odoo versions.

## Installation

To install the library package, simply install `openstack-odooclient` using `pip`.

```python
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
    verify: bool | Path | str = True,
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

The Odoo Client object exposes a number of record managers, which contain methods
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

### Available Managers

* `account_moves` - Account Moves (Invoices) (Odoo Model: `account.move`)
* `account_move_lines` - Account Move (Invoice) Lines (Odoo Model: `account.move.line`)
* `companies` - Companies (Odoo Model: `res.company`)
* `credits` - OpenStack Credits (Odoo Model: `openstack.credit`)
* `credit_transactions` - OpenStack Credit Transactions (Odoo Model: `openstack.credit.transaction`)
* `credit_types` - OpenStack Credit Types (Odoo Model: `openstack.credit.type`)
* `currencies` - Currencies (Odoo Model: `res.currency`)
* `customer_groups` - OpenStack Customer Groups (Odoo Model: `openstack.customer_group`)
* `grants` - OpenStack Grants (Odoo Model: `openstack.grant`)
* `grant_types` - OpenStack Grant Types (Odoo Model: `openstack.grant.type`)
* `partners` - Partners (Odoo Model: `res.partner`)
* `partner_categories` - Partner Categories (Odoo Model: `res.partner.category`)
* `pricelists` - Pricelists (Odoo Model: `product.pricelist`)
* `products` - Products (Odoo Model: `product.product`)
* `product_categories` - Product Categories (Odoo Model: `product.category`)
* `projects` - OpenStack Projects (Odoo Model: `openstack.project`)
* `project_contacts` - OpenStack Project Contacts (Odoo Model: `openstack.project_contact`)
* `referral_codes` - OpenStack Referral Codes (Odoo Model: `openstack.referral_code`)
* `resellers` - OpenStack Resellers (Odoo Model: `openstack.reseller`)
* `reseller_tiers` - OpenStack Reseller Tiers (Odoo Model: `openstack.reseller.tier`)
* `sale_orders` - Sale Orders (Odoo Model: `sale.order`)
* `sale_order_lines` - Sale Order Lines (Odoo Model: `sale.order.line`)
* `support_subscriptions` - OpenStack Support Subscriptions (Odoo Model: `openstack.support_subscription`)
* `support_subscription_types` - OpenStack Support Subscription Types (Odoo Model: `openstack.support_subscription.type`)
* `taxes` - Taxes (Odoo Model: `account.tax`)
* `tax_groups` - Tax Groups (Odoo Model: `account.tax.group`)
* `term_discounts` - OpenStack Term Discounts (Odoo Model: `openstack.term_discount`)
* `trials` - OpenStack Trials (Odoo Model: `openstack.trial`)
* `uoms` - Units of Measure (UoM) (Odoo Model: `uom.uom`)
* `uom_category` - Unit of Measure (UoM) Categories (Odoo Model: `uom.category`)
* `users` - Users (Odoo Model: `res.user`)
* `volume_discount_ranges` - OpenStack Volume Discount Ranges (Odoo Model: `openstack.volume_discount_range`)
* `voucher_codes` - OpenStack Voucher Codes (Odoo Model: `openstack.voucher_code`)

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
