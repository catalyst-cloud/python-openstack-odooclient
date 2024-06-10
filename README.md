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

This is the recommended way of creating the Odoo client object,
as it provides some extra parameters for convenience.

```python
from openstack_odooclient import Client as OdooClient

odoo_client = OdooClient(
    hostname="localhost",
    port=8069,
    protocol="jsonrpc",  # HTTP, or "jsonrpc+ssl" for HTTPS.
    database="odoodb",
    user="test-user",
    password="<password>",
    # version="14.0",  # Optionally specify the server version. Default is to auto-detect.
    # verify=True,  # Enable/disable SSL verification, or pass the path to a CA certificate.
)
```

If you have a pre-existing `odoorpc.ODOO` connection object, that can instead
be passed directly into `openstack_odooclient.Client`.

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
* `crm_teams` - CRM Teams (Odoo Model: `crm.team`)
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

### Common Methods

#### `list`

```python
list(
    ids: int | Iterable[int],
    fields: Iterable[str] | None = None,
    as_dict: bool = False,
) -> list[Record]
```

```python
list(
    ids: int | Iterable[int],
    fields: Iterable[str] | None = None,
    as_dict: bool = True,
) -> list[dict[str, Any]]
```

Get one or more specific records by ID.

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
>>> odoo_client.users.list(1234)
[User(record={'id': 1234, ...}, fields=None)]
>>> odoo_client.users.list([1234, 5678])
[User(record={'id': 1234, ...}, fields=None), User(record={'id': 5678, ...}, fields=None)]
```

By default all fields available on the record model
will be selected, but this can be filtered using the
`fields` parameter.

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
>>> odoo_client.users.list(1234, fields={"ids"})
[User(record={'id': 1234}, fields=['ids'])]
```

Use the `as_dict` parameter to return records as `dict`
objects, instead of record objects.

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
>>> odoo_client.users.list(1234, as_dict=True)
[{'id': 1234, ...}]
```

If `ids` is given an empty iterator, this method
returns an empty list.

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
>>> odoo_client.users.list([])
[]
```

##### Parameters

| Name      | Type                    | Description                                       | Default    |
|-----------|-------------------------|---------------------------------------------------|------------|
| `ids`     | `int \| Iterable[int]`  | Record ID, or list of record IDs                  | (required) |
| `fields`  | `Iterable[str] \| None` | Fields to select (or `None` to select all fields) | `None`     |
| `as_dict` | `bool`                  | Return records as dictionaries                    | `False`    |

##### Returns

| Type                   | Description                                    |
|------------------------|------------------------------------------------|
| `list[Record]`         | Record objects (when `as_dict` is `False`)     |
| `list[dict[str, Any]]` | Record dictionaries (when `as_dict` is `True`) |

#### `get`

```python
get(
    id: int,
    fields: Iterable[str] | None = None,
    as_dict: bool = False,
    optional: bool = False,
) -> Record
```

```python
get(
    id: int,
    fields: Iterable[str] | None = None,
    as_dict: bool = False,
    optional: bool = True,
) -> Record | None
```

```python
get(
    id: int,
    fields: Iterable[str] | None = None,
    as_dict: bool = True,
    optional: bool = False,
) -> dict[str, Any]
```

```python
get(
    id: int,
    fields: Iterable[str] | None = None,
    as_dict: bool = True,
    optional: bool = True,
) -> dict[str, Any] | None
```

Get a single record by ID.

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
>>> odoo_client.users.get(1234)
User(record={'id': 1234, ...}, fields=None)
```

By default all fields available on the record model
will be selected, but this can be filtered using the
``fields`` parameter.

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
>>> odoo_client.users.get(1234, fields={"ids"})
User(record={'id': 1234}, fields=['ids'])
```

Use the ``as_dict`` parameter to return the record as
a ``dict`` object, instead of a record object.

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
>>> odoo_client.users.get(1234, as_dict=True)
{'id': 1234, ...}
```

##### Parameters

| Name       | Type                    | Description                                       | Default    |
|------------|-------------------------|---------------------------------------------------|------------|
| `id`       | `int`                   | Record ID                                         | (required) |
| `fields`   | `Iterable[str] \| None` | Fields to select (or `None` to select all fields) | `None`     |
| `as_dict`  | `bool`                  | Return record as a dictionary                     | `False`    |
| `optional` | `bool`                  | Return `None` if not found                        | `False`    |

##### Raises

| Type                  | Description                                                        |
|-----------------------|--------------------------------------------------------------------|
| `RecordNotFoundError` | If the given record ID does not exist (when `optional` is `False`) |

##### Returns

| Type             | Description                                                 |
|------------------|-------------------------------------------------------------|
| `Record`         | Record object (when `as_dict` is `False`)                   |
| `dict[str, Any]` | Record dictionary (when `as_dict` is `True`)                |
| `None`           | If the record ID does not exist (when `optional` is `True`) |

#### `search`

```python
search(
    filters: Sequence[Any] | None = None,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = False,
    optional: bool = False,
) -> list[Record]
```

```python
search(
    filters: Sequence[Any] | None = None,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = False,
    optional: bool = True,
) -> list[Record] | None
```

```python
search(
    filters: Sequence[Any] | None = None,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = True,
    as_dict: bool = False,
    optional: bool = False,
) -> list[int]
```

```python
search(
    filters: Sequence[Any] | None = None,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = True,
    as_dict: bool = False,
    optional: bool = True,
) -> list[int] | None
```

```python
search(
    filters: Sequence[Any] | None = None,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = True,
    optional: bool = False,
) -> list[dict[str, Any]]
```

```python
search(
    filters: Sequence[Any] | None = None,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = True,
    optional: bool = True,
) -> list[dict[str, Any]] | None
```

Query the ERP for records, optionally defining
filters to constrain the search and other parameters,
and return the results.

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
>>> odoo_client.users.search([("id", "=", 1234)])
[User(record={'id': 1234, ...}, fields=None)]
```

Query filters should be defined using the same format as OdooRPC,
but some additional features are supported:

* Odoo client field aliases can be specified as the field name,
  in additional to the original field name on the Odoo model
  (e.g. `create_user` instead of `create_uid`).
* Record objects can be directly passed as the value
  on a filter, where a record ID would normally be expected.
* Sets and tuples are supported when specifying a range of values,
  in addition to lists.

To search *all* records, leave ``filters`` unset
(or set it to ``None``).

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
>>> odoo_client.users.search()
[User(record={'id': 1234, ...}, fields=None), ...]
```

By default all fields available on the record model
will be selected, but this can be filtered using the
``fields`` parameter.

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
>>> odoo_client.users.search(fields={"ids"})
[User(record={'id': 1234}, fields=['ids']), ...]
```

Use the `as_id` parameter to return the record as
a list of IDs, instead of record objects.

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
>>> odoo_client.users.search(as_id=True)
[1234, ...]
```

Use the `as_dict` parameter to return the record as
a list of `dict` objects, instead of record objects.

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
>>> odoo_client.users.search(as_dict=True)
[{'id': 1234, ...}, ...]
```

##### Parameters

| Name      | Type                    | Description                                       | Default |
|-----------|-------------------------|---------------------------------------------------|---------|
| `filters` | `Sequence[Any] \| None` | Filters to query by (or `None` for no filters)    | `None`  |
| `fields`  | `Iterable[str] \| None` | Fields to select (or `None` to select all fields) | `None`  |
| `order`   | `str \| None`           | Field to order results by, if ordering results    | `None`  |
| `as_id`   | `bool`                  | Return the record IDs only                        | `False` |
| `as_dict` | `bool`                  | Return records as dictionaries                    | `False` |

##### Returns

| Type                   | Description                                    |
|------------------------|------------------------------------------------|
| `list[Record]`         | Record objects (default)                       |
| `list[int]`            | Record IDs (when `as_id` is `True`)            |
| `list[dict[str, Any]]` | Record dictionaries (when `as_dict` is `True`) |

#### `create`

```python
create(**fields: Any) -> int
```

Create a new record, using the specified keyword arguments
as input fields.

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
>>> odoo_client.sales_order_lines.create(...)
1234
```

To fetch the newly created record object,
pass the returned ID to the [``get``](#get) method.

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
>>> odoo_client.sale_order_lines.get(
...     odoo_client.sales_order_lines.create(...),
... )
SaleOrderLine(record={'id': 1234, ...}, fields=None)
```

##### Parameters

| Name       | Type  | Description                             | Default    |
|------------|-------|-----------------------------------------|------------|
| `**fields` | `Any` | Record field values (keyword arguments) | (required) |

##### Returns

| Type  | Description                        |
|-------|------------------------------------|
| `int` | The ID of the newly created record |

#### `create_multi`

```python
create_multi(*records: Mapping[str, Any]) -> list[int]
```

Create one or more new records in a single request,
passing in the mappings containing the record's input fields
as positional arguments.

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
>>> odoo_client.sales_order_lines.create_multi({...}, {...})
[1234, 1235]
```

To fetch the newly created record objects,
pass the returned IDs to the [``list``](#list) method.

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
>>> odoo_client.sale_order_lines.list(
...     odoo_client.sales_order_lines.create_multi({...}, {...}),
... )
[SaleOrderLine(record={'id': 1234, ...}, fields=None), SaleOrderLine(record={'id': 1235, ...}, fields=None)]
```

##### Parameters

| Name       | Type                | Description                                        | Default    |
|------------|---------------------|----------------------------------------------------|------------|
| `*records` | `Mapping[str, Any]` | Record field-value mappings (positional arguments) | (required) |

##### Returns

| Type        | Description                          |
|-------------|--------------------------------------|
| `list[int]` | The IDs of the newly created records |

#### `unlink`/`delete`

```python
unlink(*records: Record | int | Iterable[Record | int]) -> None
```

```python
delete(*records: Record | int | Iterable[Record | int]) -> None
```

Delete one or more records from Odoo.

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
>>> odoo_client.sales_order_lines.unlink(1234)
```

This method accepts either a record object or ID, or an iterable of
either of those types. Multiple positional arguments are allowed.

All specified records will be deleted in a single request.

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
>>> line1 = odoo_client.sales_order_lines.get(1234)
>>> line2 = odoo_client.sales_order_lines.get(5678)
>>> odoo_client.sales_order_lines.unlink(line1, 9012, [line2, 3456])
```

##### Parameters

| Name       | Type                                       | Description                                                                  | Default    |
|------------|--------------------------------------------|------------------------------------------------------------------------------|------------|
| `*records` | `Record \| int \| Iterable[Record \| int]` | The records to delete (object, ID, or record/ID list) (positional arguments) | (required) |

### Managers for Named Records

Some record types have a name field that is generally expected to be unique.
The managers for these record types have additional methods for querying records by name.

* `account_moves` - Account Moves (Invoices) (Odoo Model: `account.move`)
* `companies` - Companies (Odoo Model: `res.company`)
* `credit_types` - OpenStack Credit Types (Odoo Model: `openstack.credit.type`)
* `crm_teams` - CRM Teams (Odoo Model: `crm.team`)
* `currencies` - Currencies (Odoo Model: `res.currency`)
* `customer_groups` - OpenStack Customer Groups (Odoo Model: `openstack.customer_group`)
* `grant_types` - OpenStack Grant Types (Odoo Model: `openstack.grant.type`)
* `partner_categories` - Partner Categories (Odoo Model: `res.partner.category`)
* `pricelists` - Pricelists (Odoo Model: `product.pricelist`)
* `product_categories` - Product Categories (Odoo Model: `product.category`)
* `reseller_tiers` - OpenStack Reseller Tiers (Odoo Model: `openstack.reseller.tier`)
* `sale_orders` - Sale Orders (Odoo Model: `sale.order`)
* `support_subscription_types` - OpenStack Support Subscription Types (Odoo Model: `openstack.support_subscription.type`)
* `taxes` - Taxes (Odoo Model: `account.tax`)
* `tax_groups` - Tax Groups (Odoo Model: `account.tax.group`)
* `voucher_codes` - OpenStack Voucher Codes (Odoo Model: `openstack.voucher_code`)

#### `get_by_name`

```python
get_by_name(
    name: str,
    fields: Iterable[str] | None = None,
    as_id: bool = False,
    as_dict: bool = False,
    optional: bool = False,
) -> Record
```

```python
get_by_name(
    name: str,
    fields: Iterable[str] | None = None,
    as_id: bool = False,
    as_dict: bool = False,
    optional: bool = True,
) -> Record | None
```

```python
get_by_name(
    name: str,
    fields: Iterable[str] | None = None,
    as_id: bool = True,
    as_dict: bool = False,
    optional: bool = False,
) -> int
```

```python
get_by_name(
    name: str,
    fields: Iterable[str] | None = None,
    as_id: bool = True,
    as_dict: bool = False,
    optional: bool = True,
) -> int | None
```

```python
get_by_name(
    name: str,
    fields: Iterable[str] | None = None,
    as_id: bool = False,
    as_dict: bool = True,
    optional: bool = False,
) -> dict[str, Any]
```

```python
get_by_name(
    name: str,
    fields: Iterable[str] | None = None,
    as_id: bool = False,
    as_dict: bool = True,
    optional: bool = True,
) -> dict[str, Any] | None
```

Query a unique record by name.

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
>>> odoo_client.currencies.get_by_name("NZD")
[Currency(record={'id': 1234, 'name': 'NZD', ...}, fields=None)]
```

A number of parameters are available to configure the return type,
and what happens when a result is not found.

By default all fields available on the record model
will be selected, but this can be filtered using the
`fields` parameter.

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
>>> odoo_client.currencies.get_by_name("NZD", fields={"rounding"})
Currency(record={'id': 1234, 'rounding': 0.001}, fields=['rounding'])
```

Use the `as_id` parameter to return the ID of the record,
instead of the record object.

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
>>> odoo_client.currencies.get_by_name("NZD", as_id=True)
1234
```

Use the `as_dict` parameter to return the record as
a `dict` object, instead of a record object.

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
>>> odoo_client.currencies.get_by_name("NZD", as_dict=True)
{'id': 1234, ...}
```

When `optional` is `True`, `None` is returned if a record
with the given name does not exist, instead of raising an error.

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
>>> odoo_client.currencies.get_by_name("non-existent", optional=True)
None
```

##### Parameters

| Name       | Type                    | Description                                       | Default    |
|------------|-------------------------|---------------------------------------------------|------------|
| `name`     | `str`                   | The record name                                   | (required) |
| `fields`   | `Iterable[str] \| None` | Fields to select (or `None` to select all fields) | `None`     |
| `as_id`    | `bool`                  | Return the record IDs only                        | `False`    |
| `as_dict`  | `bool`                  | Return records as dictionaries                    | `False`    |
| `optional` | `bool`                  | Return `None` if not found                        | `False`    |

##### Raises

| Type                        | Description                                                             |
|-----------------------------|-------------------------------------------------------------------------|
| `RecordNotFoundError`       | If no record with the given name was found (when `optional` is `False`) |
| `MultipleRecordsFoundError` | If multiple records were found with the same name                       |

##### Returns

| Type             | Description                                                                |
|------------------|----------------------------------------------------------------------------|
| `Record`         | Record object (default)                                                    |
| `int`            | Record ID (when `as_id` is `True`)                                         |
| `dict[str, Any]` | Record dictionary (when `as_dict` is `True`)                               |
| `None`           | If a record with the given name does not exist (when `optional` is `True`) |
