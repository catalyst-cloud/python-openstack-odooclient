# Managers

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

## Available Managers

* [Account Moves (Invoices)](account-move.md)
* [Account Move (Invoice) Lines](account-move-line.md)
* [Attachments](attachment.md)
* [Companies](company.md)
* [OpenStack Credits](credit.md)
* [OpenStack Credit Transactions](credit-transaction.md)
* [OpenStack Credit Types](credit-type.md)
* [Currencies](currency.md)
* [OpenStack Customer Groups](customer-group.md)
* [OpenStack Grants](grant.md)
* [OpenStack Grant Types](grant-type.md)
* [Partners](partner.md)
* [Partner Categories](partner-category.md)
* [Pricelists](pricelist.md)
* [Products](product.md)
* [Product Categories](product-category.md)
* [OpenStack Projects](project.md)
* [OpenStack Project Contacts](project-contact.md)
* [OpenStack Referral Codes](referral-code.md)
* [OpenStack Resellers](reseller.md)
* [OpenStack Reseller Tiers](reseller-tier.md)
* [Sale Orders](sale-order.md)
* [Sale Order Lines](sale-order-line.md)
* [OpenStack Support Subscriptions](support-subscription.md)
* [OpenStack Support Subscription Types](support-subscription-type.md)
* [Taxes](tax.md)
* [Tax Groups](tax-group.md)
* [OpenStack Term Discounts](term-discount.md)
* [OpenStack Trials](trial.md)
* [Units of Measure (UoM)](uom.md)
* [Unit of Measure (UoM) Categories](uom-category.md)
* [Users](user.md)
* [OpenStack Volume Discount Ranges](volume-discount-range.md)
* [OpenStack Voucher Codes](voucher-code.md)

## Methods

All record managers implement the following methods for querying and
managing records.

### `list`

```python
list(
    ids: int | Iterable[int],
    fields: Iterable[str] | None = None,
    as_dict: bool = False,
    optional: bool = False,
) -> list[Record]
```

```python
list(
    ids: int | Iterable[int],
    fields: Iterable[str] | None = None,
    as_dict: bool = True,
    optional: bool = False,
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

By default, the method checks that all provided IDs
were found and returned (and will raise an error if any are missing),
at the cost of a small performance hit.

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
>>> odoo_client.users.list(999999)
...
openstack_odooclient.exceptions.RecordNotFoundError: User records with IDs not found: 999999
```

To instead return the list of records that were found
without raising an error, set `optional` to `True`.

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
>>> odoo_client.users.list(999999, optional=True)
[]
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

#### Parameters

| Name       | Type                   | Description                                         | Default    |
|------------|------------------------|-----------------------------------------------------|------------|
| `ids`      | `int | Iterable[int]`  | Record ID, or list of record IDs                    | (required) |
| `fields`   | `Iterable[str] | None` | Fields to select (or `None` to select all fields)   | `None`     |
| `as_dict`  | `bool`                 | Return records as dictionaries                      | `False`    |
| `optional` | `bool`                 | Do not raise an error if not all records were found | `False`    |

#### Raises

| Type                  | Description                                                                |
|-----------------------|----------------------------------------------------------------------------|
| `RecordNotFoundError` | If any of the given record IDs were not found (when `optional` is `False`) |

#### Returns

| Type                   | Description                                    |
|------------------------|------------------------------------------------|
| `list[Record]`         | Record objects (when `as_dict` is `False`)     |
| `list[dict[str, Any]]` | Record dictionaries (when `as_dict` is `True`) |

### `get`

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

#### Parameters

| Name       | Type                   | Description                                       | Default    |
|------------|------------------------|---------------------------------------------------|------------|
| `id`       | `int`                  | Record ID                                         | (required) |
| `fields`   | `Iterable[str] | None` | Fields to select (or `None` to select all fields) | `None`     |
| `as_dict`  | `bool`                 | Return record as a dictionary                     | `False`    |
| `optional` | `bool`                 | Return `None` if not found                        | `False`    |

#### Raises

| Type                  | Description                                                        |
|-----------------------|--------------------------------------------------------------------|
| `RecordNotFoundError` | If the given record ID does not exist (when `optional` is `False`) |

#### Returns

| Type             | Description                                                 |
|------------------|-------------------------------------------------------------|
| `Record`         | Record object (when `as_dict` is `False`)                   |
| `dict[str, Any]` | Record dictionary (when `as_dict` is `True`)                |
| `None`           | If the record ID does not exist (when `optional` is `True`) |

### `search`

```python
search(
    filters: Sequence[tuple[str, str, Any] | Sequence[Any] | str] | None = None,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = False,
) -> list[Record]
```

```python
search(
    filters: Sequence[tuple[str, str, Any] | Sequence[Any] | str] | None = None,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = True,
    as_dict: bool = False,
) -> list[int]
```

```python
search(
    filters: Sequence[tuple[str, str, Any] | Sequence[Any] | str] | None = None,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = True,
) -> list[dict[str, Any]]
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

Query filters should be defined using the
[ORM API search domain](https://www.odoo.com/documentation/14.0/developer/reference/addons/orm.html#search-domains)
format.

Filters are a sequence of criteria, where each criterion
is one of the following types of values:

* A 3-tuple or 3-element sequence in `(field_name, operator, value)`
  format, where:

    * `field_name` (`str`) is the the name of the field to filter by.
    * `operator` (`str`) is the comparison operator to use (for more
      information on the available operators, check the
      [ORM API search domain](https://www.odoo.com/documentation/14.0/developer/reference/addons/orm.html#search-domains)
      documentation).
    * `value` (`Any`) is the value to compare records against.

* A logical operator which prefixes the following filter criteria
  to form a **criteria combination**:

    * `&` is a logical AND. Records only match if **both** of the
      following **two** criteria match.
    * `|` is a logical OR. Records match if **either** of the
      following **two** criteria match.
    * `!` is a logical NOT (negation). Records match if the
      following **one** criterion does **NOT** match.

Every criteria combination is implicitly combined using a logical AND
to form the overall filter to use to query records.

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
>>> odoo_client.users.search(
...     [
...         # Both user AND connected partner are active
...         ("active", "=", True),
...         ("active_partner", "=", True),
...         # Name is either Lorem Ipsum or Alice Bob
...         "|",
...         ("name", "=", "Lorem Ipsum"),
...         ("name", "=", "Alice Bob"),
...     ],
... )
[User(record={'id': 1234, 'name': 'Lorem Ipsum', ...}, fields=None), User(record={'id': 5678, 'name': 'Alice Bob', ...}, fields=None)]
```

For the field value, this method accepts the same types as defined
on the record objects.

In addition to the native Odoo field names, field aliases
and model ref field names can be specified as the field name
in the search filter. Record objects can also be directly
passed as the value on a filter, not just record IDs.

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
>>> user = odoo_client.users.get(1234)
>>> odoo_client.users.search([("create_user", "=", user)])
[User(record={'id': 5678, ...}, fields=None), ...]
```

When specifying a range of possible values, lists, tuples
and sets are supported.

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
>>> user = odoo_client.users.get(1234)
>>> odoo_client.users.search([("create_user", "in", {user})])
[User(record={'id': 5678, ...}, fields=None), ...]
```

Search criteria using nested field references can be defined
by using the dot-notation (`.`) to specify what field on what
record reference to check.
Field names and values for nested field references are
validated and encoded just like criteria for standard
field references.

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
>>> odoo_client.users.search(
...     [
...         # Check that the "name" field inside "create_user" matches
...         ("create_user.name", "=", "Lorem Ipsum"),
...     ],
... )
[User(record={'id': 5678, ...}, fields=None), ...]
```

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

#### Parameters

| Name      | Type                                                          | Description                                       | Default |
|-----------|---------------------------------------------------------------|---------------------------------------------------|---------|
| `filters` | `Sequence[tuple[str, str, Any] | Sequence[Any] | str] | None` | Filters to query by (or `None` for no filters)    | `None`  |
| `fields`  | `Iterable[str] | None`                                        | Fields to select (or `None` to select all fields) | `None`  |
| `order`   | `str | None`                                                  | Field to order results by, if ordering results    | `None`  |
| `as_id`   | `bool`                                                        | Return the record IDs only                        | `False` |
| `as_dict` | `bool`                                                        | Return records as dictionaries                    | `False` |

#### Returns

| Type                   | Description                                    |
|------------------------|------------------------------------------------|
| `list[Record]`         | Record objects (default)                       |
| `list[int]`            | Record IDs (when `as_id` is `True`)            |
| `list[dict[str, Any]]` | Record dictionaries (when `as_dict` is `True`) |

### `create`

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
>>> odoo_client.sales_orders.create(...)
1234
```

This method allows a lot of flexibility in how input fields
should be defined.

The fields passed to this method should use the same field names
and value types that are defined on the record classes.
The Odoo Client library will convert the values to the formats
that the Odoo API expects.

For example, when defining references to another record,
you can either pass the record ID, or the record object.
The field name can also either be for the ID or the object.

Field aliases are also resolved to their target field names.

```python
>>> from datetime import date
>>> from openstack_odooclient import Client as OdooClient
>>> odoo_client = OdooClient(
...     hostname="localhost",
...     port=8069,
...     protocol="jsonrpc",
...     database="odoodb",
...     user="test-user",
...     password="<password>",
... )
>>> user = odoo_client.users.get(5678)
>>> odoo_client.sales_orders.create(
...     user=user,  # User object
...     partner_id=9012,  # Partner ID
...     os_invoice_date=date(2024, 6, 30),
...     os_invoice_due_date=date(2024, 7, 20),
...     os_project=3456,  # Field name is for the object, value is the ID
...     order_lines=[7890],  # Field alias used
... )
1234
```

When creating a record with a list of references to another record
(a `One2many` or `Many2many` relation), it is possible to **nest**
record mappings where an ID or object would normally go.
New records will be created for those mappings, and linked
to the parent record. Nested record mappings are recursively validated
and processed in the same way as the parent record.

```python
>>> from datetime import date
>>> from openstack_odooclient import Client as OdooClient
>>> odoo_client = OdooClient(
...     hostname="localhost",
...     port=8069,
...     protocol="jsonrpc",
...     database="odoodb",
...     user="test-user",
...     password="<password>",
... )
>>> user = odoo_client.users.get(5678)
>>> odoo_client.sales_orders.create(
...     user=user,  # User object
...     partner_id=9012,  # Partner ID
...     os_invoice_date=date(2024, 6, 30),
...     os_invoice_due_date=date(2024, 7, 20),
...     os_project=3456,  # Field name for object, value is ID
...     order_lines=[  # Create the sale order lines
...         {
...             "name": "test-instance",
...             "product": odoo_client.products.get(7890),  # Product object
...             "product_uom": 123456,  # Field name for object, value is ID
...             "product_uom_qty": 1.0,
...             "price_unit": 0.05,
...             "os_project_id": 3456,  # Project ID
...             "os_resource_id": "1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a",
...             "os_region": "RegionOne",
...             "os_resource_type": "Virtual Machine",
...             "os_resource_name": "m1.small",
...         },
...     ],
... )
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

#### Parameters

| Name       | Type  | Description                             | Default    |
|------------|-------|-----------------------------------------|------------|
| `**fields` | `Any` | Record field values (keyword arguments) | (required) |

#### Returns

| Type  | Description                        |
|-------|------------------------------------|
| `int` | The ID of the newly created record |

### `create_multi`

```python
create_multi(*records: Mapping[str, Any]) -> list[int]
```

Create one or more new records in a single request,
passing in the mappings containing the record's input fields
as positional arguments.

The record mappings should be in the same format as with
the [``create``](#create) method.

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
>>> odoo_client.sales_orders.create_multi({...}, {...})
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
>>> odoo_client.sale_orders.list(
...     odoo_client.sales_orders.create_multi({...}, {...}),
... )
[SaleOrder(record={'id': 1234, ...}, fields=None), SaleOrder(record={'id': 1235, ...}, fields=None)]
```

#### Parameters

| Name       | Type                | Description                                        | Default    |
|------------|---------------------|----------------------------------------------------|------------|
| `*records` | `Mapping[str, Any]` | Record field-value mappings (positional arguments) | (required) |

#### Returns

| Type        | Description                          |
|-------------|--------------------------------------|
| `list[int]` | The IDs of the newly created records |

### `update`

```python
def update(record: int | Record, **fields: Any) -> None
```

Update one or more fields on this record in place.

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
User(record={'id': 1234, 'name': 'Old Name', ...}, fields=None)
>>> odoo_client.users.update(1234, name="New Name")
>>> odoo_client.users.get(1234)
User(record={'id': 1234, 'name': 'New Name', ...}, fields=None)
```

Field names are passed as keyword arguments.
This method has the same flexibility with regards to what
field names are used as when [creating records](#create);
for example, when updating a model ref, either its ID
(e.g. ``user_id``) or object (e.g. ``user``) field names
can be used.

*Added in version 0.2.1.*

#### Parameters

| Name       | Type           | Description                             | Default    |
|------------|----------------|-----------------------------------------|------------|
| `record`   | `int | Record` | The record to update (object or ID)     | (required) |
| `**fields` | `Any`          | Record field values (keyword arguments) | (required) |

### `unlink`/`delete`

```python
unlink(*records: int | Record | Iterable[int | Record]) -> None
```

```python
delete(*records: int | Record | Iterable[int | Record]) -> None
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

#### Parameters

| Name       | Type                                    | Description                                                                  | Default    |
|------------|-----------------------------------------|------------------------------------------------------------------------------|------------|
| `*records` | `int | Record | Iterable[int | Record]` | The records to delete (object, ID, or record/ID list) (positional arguments) | (required) |

## Named Record Managers

Some record types have a `name` field that is generally expected to be unique.
The managers for these record types have additional methods for querying records by name.

* [Account Moves (Invoices)](account-move.md)
* [Companies](company.md)
* [OpenStack Credit Types](credit-type.md)
* [Currencies](currency.md)
* [OpenStack Customer Groups](customer-group.md)
* [OpenStack Grant Types](grant-type.md)
* [Pricelists](pricelist.md)
* [OpenStack Reseller Tiers](reseller-tier.md)
* [Sale Orders](sale-order.md)
* [OpenStack Support Subscription Types](support-subscription-type.md)
* [Taxes](tax.md)
* [Tax Groups](tax-group.md)

### `get_by_name`

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

#### Parameters

| Name       | Type                   | Description                                       | Default    |
|------------|------------------------|---------------------------------------------------|------------|
| `name`     | `str`                  | The record name                                   | (required) |
| `fields`   | `Iterable[str] | None` | Fields to select (or `None` to select all fields) | `None`     |
| `as_id`    | `bool`                 | Return the record IDs only                        | `False`    |
| `as_dict`  | `bool`                 | Return records as dictionaries                    | `False`    |
| `optional` | `bool`                 | Return `None` if not found                        | `False`    |

#### Raises

| Type                        | Description                                                             |
|-----------------------------|-------------------------------------------------------------------------|
| `RecordNotFoundError`       | If no record with the given name was found (when `optional` is `False`) |
| `MultipleRecordsFoundError` | If multiple records were found with the same name                       |

#### Returns

| Type             | Description                                                                |
|------------------|----------------------------------------------------------------------------|
| `Record`         | Record object (default)                                                    |
| `int`            | Record ID (when `as_id` is `True`)                                         |
| `dict[str, Any]` | Record dictionary (when `as_dict` is `True`)                               |
| `None`           | If a record with the given name does not exist (when `optional` is `True`) |

## Coded Record Managers

Some record types have a `code` field that is guaranteed to be unique.
The managers for these record types have additional methods for querying records by code.

* [OpenStack Referral Codes](referral-code.md)
* [OpenStack Voucher Codes](voucher-code.md)

### `get_by_code`

```python
get_by_code(
    code: str,
    fields: Iterable[str] | None = None,
    as_id: bool = False,
    as_dict: bool = False,
    optional: bool = False,
) -> Record
```

```python
get_by_code(
    code: str,
    fields: Iterable[str] | None = None,
    as_id: bool = False,
    as_dict: bool = False,
    optional: bool = True,
) -> Record | None
```

```python
get_by_code(
    code: str,
    fields: Iterable[str] | None = None,
    as_id: bool = True,
    as_dict: bool = False,
    optional: bool = False,
) -> int
```

```python
get_by_code(
    code: str,
    fields: Iterable[str] | None = None,
    as_id: bool = True,
    as_dict: bool = False,
    optional: bool = True,
) -> int | None
```

```python
get_by_code(
    code: str,
    fields: Iterable[str] | None = None,
    as_id: bool = False,
    as_dict: bool = True,
    optional: bool = False,
) -> dict[str, Any]
```

```python
get_by_code(
    code: str,
    fields: Iterable[str] | None = None,
    as_id: bool = False,
    as_dict: bool = True,
    optional: bool = True,
) -> dict[str, Any] | None
```

Query a unique record by code.

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
>>> odoo_client.voucher_codes.get_by_code("OSCODE123")
VoucherCode(record={'id': 1234, 'code': 'OSCODE123', ...}, fields=None)
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
>>> odoo_client.voucher_codes.get_by_code("OSCODE123", fields={"code", "multi_use"})
VoucherCode(record={'id': 1234, 'code': 'OSCODE123', 'multi_use': True, ...}, fields=['code', 'multi_use'])
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
>>> odoo_client.voucher_codes.get_by_code("OSCODE123", as_id=True)
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
>>> odoo_client.voucher_codes.get_by_code("OSCODE123", as_dict=True)
{'id': 1234, ...}
```

When `optional` is `True`, `None` is returned if a record
with the given code does not exist, instead of raising an error.

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
>>> odoo_client.voucher_codes.get_by_code("non-existent", optional=True)
None
```

#### Parameters

| Name       | Type                   | Description                                       | Default    |
|------------|------------------------|---------------------------------------------------|------------|
| `code`     | `str`                  | The record code                                   | (required) |
| `fields`   | `Iterable[str] | None` | Fields to select (or `None` to select all fields) | `None`     |
| `as_id`    | `bool`                 | Return the record IDs only                        | `False`    |
| `as_dict`  | `bool`                 | Return records as dictionaries                    | `False`    |
| `optional` | `bool`                 | Return `None` if not found                        | `False`    |

#### Raises

| Type                        | Description                                                             |
|-----------------------------|-------------------------------------------------------------------------|
| `RecordNotFoundError`       | If no record with the given code was found (when `optional` is `False`) |
| `MultipleRecordsFoundError` | If multiple records were found with the same code                       |

#### Returns

| Type             | Description                                                                |
|------------------|----------------------------------------------------------------------------|
| `Record`         | Record object (default)                                                    |
| `int`            | Record ID (when `as_id` is `True`)                                         |
| `dict[str, Any]` | Record dictionary (when `as_dict` is `True`)                               |
| `None`           | If a record with the given code does not exist (when `optional` is `True`) |

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

### Attributes and Methods

The following attributes and methods are available on all record types.

To find the available attributes and methods on specific record classes,
check the manager page for the record type.

#### `id`

```python
id: int
```

The record's ID in Odoo.

#### `create_date`

```python
create_date: datetime
```

The time the record was created.

#### `create_uid`

```python
create_uid: int | None
```

The ID of the [user](user.md) that created this record.

#### `create_name`

```python
create_name: str | None
```

The name of the [user](user.md) that created this record.

#### `create_user`

```python
create_user: User | None
```

The [user](user.md) that created this record.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

#### `write_date`

```python
write_date: datetime
```

The time the record was last modified.

#### `write_uid`

```python
write_uid: int | None
```

The ID of the [user](user.md) that last modified this record.

#### `write_name`

```python
write_name: str | None
```

The name of the [user](user.md) that modified this record.

#### `write_user`

```python
write_user: User | None
```

The [user](user.md) that last modified this record.

This fetches the full record from Odoo once,
and caches it for subsequence accesses.

#### `as_dict`

```python
as_dict(raw: bool = False) -> dict[str, Any]
```

Convert this record object to a dictionary.

The fields and values in the dictionary are the same
as if the record was queried using `as_dict=True`.
This changes field names to the record object equivalents,
if they are different, to take into account fields being
named differently across Odoo versions.

```python
>>> user
User(record={'id': 1234, ...}, fields=None)
>>> user.as_dict()
{'id': 1234, ...}
```

Set `raw=True` to instead get the raw record dictionary
fields and values as returned by OdooRPC.

```python
>>> user
User(record={'id': 1234, ...}, fields=None)
>>> user.as_dict(raw=True)
{'id': 1234, ...}
```

##### Parameters

| Name  | Type   | Description                        | Default |
|-------|--------|------------------------------------|---------|
| `raw` | `bool` | Return raw dictionary from OdooRPC | `False` |

##### Returns

| Type             | Description       |
|------------------|-------------------|
| `dict[str, Any]` | Record dictionary |

#### `update`

```python
def update(**fields: Any) -> None
```

Update one or more fields on this record in place.

```python
>>> user
User(record={'id': 1234, 'name': 'Old Name', ...}, fields=None)
>>> user.update(name="New Name")
>>> user.refresh()
User(record={'id': 1234, 'name': 'New Name', ...}, fields=None)
```

Field names are passed as keyword arguments.
This method has the same flexibility with regards to what
field names are used as when [creating records](#create);
for example, when updating a model ref, either its ID
(e.g. ``user_id``) or object (e.g. ``user``) field names
can be used.

!!! note

    This record object is not updated in place by this method.

    If you need an updated version of the record object,
    use the [`refresh`](#refresh) method to fetch the latest version.

*Added in version 0.2.1.*

##### Parameters

| Name       | Type  | Description                             | Default    |
|------------|-------|-----------------------------------------|------------|
| `**fields` | `Any` | Record field values (keyword arguments) | (required) |

#### `refresh`

```python
refresh() -> Self
```

Fetch the latest version of this record from Odoo.

This does not update the record object in place,
a new object is returned with the up-to-date field values.

```python
>>> user
User(record={'id': 1234, 'name': 'Old Name', ...}, fields=None)
>>> user.refresh()
User(record={'id': 1234, 'name': 'New Name', ...}, fields=None)
```

##### Returns

| Type   | Description                         |
|--------|-------------------------------------|
| `Self` | Latest version of the record object |

#### `unlink`/`delete`

```python
unlink() -> None
```

```python
delete() -> None
```

Delete this record from Odoo.

```python
>>> user
User(record={'id': 1234, ...}, fields=None)
>>> user.unlink()
>>> user.refresh()
Traceback (most recent call last):
...
openstack_odooclient.exceptions.RecordNotFoundError: User record not found with ID: 1234
```

## Records with Attachments

Some records can have [attachments](attachment.md) uploaded and associated with them.

* [Account Moves (Invoices)](account-move.md)

When fetching an attachment record from Odoo, the contents of the attachment
(available using the `datas` field) are not fetched by default. This is to
ensure that downloading only takes place when requested, preventing
unexpected large downloads.

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
>>> account_move = odoo_client.account_moves.get(1234)
>>> attachment = odoo_client.attachments.get(
...     account_move.message_main_attachment_id,
... )
>>> attachment
Attachment(record={'id': 5678, ...}, fields=None)
>>> attachment.datas  # AttributeError
```

Common attachment operations for binary attachments
(attachments with a `type` of `binary`) are documented below.

In addition to regular binary attachments, Odoo
also supports URL-referenced attachments and a number
of other useful fields; for more information see the
manager page for [attachments](attachment.md).

### Downloading

Attachments can be downloaded by simply calling the `download` method
on an attachment object.

The contents of the attachment will be returned as a `bytes` object.

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
>>> account_move = odoo_client.account_moves.get(1234)
>>> attachment = odoo_client.attachments.get(
...     account_move.message_main_attachment_id,
... )
>>> attachment.download()
b'Hello, world!'
```

### Uploading

New attachments can be uploaded and associated with a record
using the `upload` method.

For more information, see the documentation for the
[`upload`](attachment.md#upload) method.

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
>>> contents = b"Hello, world!"
>>> account_move = odoo_client.account_moves.get(1234)
>>> odoo_client.attachments.upload(
...     "example.txt",
...     contents,
...     record=account_move,
... )
5678
```

### Evaluating checksums

Attachments have a `checksum` field, which is a SHA-1 hash of the attachment
stored by Odoo that can be used to efficiently verify the integrity of the
uploaded attachment without redownloading the contents.

```python
>>> import hashlib
>>> from openstack_odooclient import Client as OdooClient
>>> odoo_client = OdooClient(
...     hostname="localhost",
...     port=8069,
...     protocol="jsonrpc",
...     database="odoodb",
...     user="test-user",
...     password="<password>",
... )
>>> contents = b"Hello, world!"
>>> account_move = odoo_client.account_moves.get(1234)
>>> attachment_id = odoo_client.attachments.upload(
...     "example.txt",
...     contents,
...     record=account_move,
... )
>>> attachment.checksum == hashlib.sha1(contents).hexdigest()
True
```

### In-place updates

If you'd like to update an attachment in-place without creating
a new record (and then having to delete the old one), this can
be done using the `reupload` method on the attachment object.

For more information, see the documentation for the
[`reupload`](attachment.md#reupload_1) method.

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
>>> account_move = odoo_client.account_moves.get(1234)
>>> attachment = odoo_client.attachments.get(
...     account_move.message_main_attachment_id,
... )
>>> attachment.download()
b'Hello, world!'
>>> attachment.reupload(b"Goodbye, world!")
>>> attachment = attachment.refresh()
>>> attachment.download()
b'Goodbye, world!'
```

### Attributes and Methods

Record types that can have attachments associated with them
have the following fields added.

#### `message_main_attachment_id`

```python
message_main_attachment_id: int | None
```

The ID of the main [attachment](attachment.md) on the record, if there is one.

#### `message_main_attachment_name`

```python
message_main_attachment_name: str | None
```

The name of the main [attachment](attachment.md) on the record, if there is one.

#### `message_main_attachment`

```python
message_main_attachment: Attachment | None
```
The main [attachment](attachment.md) on the record, if there is one.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

## Custom Managers and Record Types

The OpenStack Odoo Client library supports defining new record types and adding
managers for them to the Odoo client object, allowing for adding support for custom Odoo add-ons.

For more information, see [Custom Managers and Record Types](custom.md).
