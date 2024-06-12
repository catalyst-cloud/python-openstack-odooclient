# Managers

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

## Available Managers

* [Account Moves (Invoices)](account-move.md)
* [Account Move (Invoice) Lines](account-move-line.md)
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
* [Users](users.md)
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

#### Parameters

| Name      | Type                    | Description                                       | Default    |
|-----------|-------------------------|---------------------------------------------------|------------|
| `ids`     | `int \| Iterable[int]`  | Record ID, or list of record IDs                  | (required) |
| `fields`  | `Iterable[str] \| None` | Fields to select (or `None` to select all fields) | `None`     |
| `as_dict` | `bool`                  | Return records as dictionaries                    | `False`    |

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

| Name       | Type                    | Description                                       | Default    |
|------------|-------------------------|---------------------------------------------------|------------|
| `id`       | `int`                   | Record ID                                         | (required) |
| `fields`   | `Iterable[str] \| None` | Fields to select (or `None` to select all fields) | `None`     |
| `as_dict`  | `bool`                  | Return record as a dictionary                     | `False`    |
| `optional` | `bool`                  | Return `None` if not found                        | `False`    |

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

#### Parameters

| Name      | Type                    | Description                                       | Default |
|-----------|-------------------------|---------------------------------------------------|---------|
| `filters` | `Sequence[Any] \| None` | Filters to query by (or `None` for no filters)    | `None`  |
| `fields`  | `Iterable[str] \| None` | Fields to select (or `None` to select all fields) | `None`  |
| `order`   | `str \| None`           | Field to order results by, if ordering results    | `None`  |
| `as_id`   | `bool`                  | Return the record IDs only                        | `False` |
| `as_dict` | `bool`                  | Return records as dictionaries                    | `False` |

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

#### Parameters

| Name       | Type                | Description                                        | Default    |
|------------|---------------------|----------------------------------------------------|------------|
| `*records` | `Mapping[str, Any]` | Record field-value mappings (positional arguments) | (required) |

#### Returns

| Type        | Description                          |
|-------------|--------------------------------------|
| `list[int]` | The IDs of the newly created records |

### `unlink`/`delete`

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

#### Parameters

| Name       | Type                                       | Description                                                                  | Default    |
|------------|--------------------------------------------|------------------------------------------------------------------------------|------------|
| `*records` | `Record \| int \| Iterable[Record \| int]` | The records to delete (object, ID, or record/ID list) (positional arguments) | (required) |

## Named Record Managers

Some record types have a name field that is generally expected to be unique.
The managers for these record types have additional methods for querying records by name.

* [Account Moves (Invoices)](account-move.md)
* [Companies](company.md)
* [OpenStack Credit Types](credit-type.md)
* [Currencies](currency.md)
* [OpenStack Customer Groups](customer-group.md)
* [OpenStack Grant Types](grant-type.md)
* [Partner Categories](partner-category.md)
* [Pricelists](pricelist.md)
* [Product Categories](product-category.md)
* [OpenStack Projects](project.md)
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

| Name       | Type                    | Description                                       | Default    |
|------------|-------------------------|---------------------------------------------------|------------|
| `name`     | `str`                   | The record name                                   | (required) |
| `fields`   | `Iterable[str] \| None` | Fields to select (or `None` to select all fields) | `None`     |
| `as_id`    | `bool`                  | Return the record IDs only                        | `False`    |
| `as_dict`  | `bool`                  | Return records as dictionaries                    | `False`    |
| `optional` | `bool`                  | Return `None` if not found                        | `False`    |

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

### Custom Attributes

Most of the model fields commonly used by applications have been defined
in the record classes, but if your installation of Odoo has add-ons
installed that define custom fields that the Odoo client library
does not know about, these can still be used (just without type hinting).

Access these fields as object attributes, the same way as you would any
other field.

```python
>>> user.custom_field_name
'custom-field-value'
```

If the custom field is a reference to another model record,
it will be available on the record object as 2-member list.
The first value is the record ID, and the second value
is the display name of the record.

```python
>>> user.custom_model_ref
[5678, 'custom-record-name']
```

If the custom field is a list of model records,
the record IDs will be made available as type `list[int]`.

```python
>>> user.custom_model_refs
[5678, 9012, ...]
```

### Attributes and Methods

The following attributes and methods are available on all record types.

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
create_uid: int
```

The ID of the partner that created this record.

#### `create_name`

```python
create_name: str
```

The name of the partner that created this record.

#### `create_user`

```python
create_user: Partner
```

The partner that created this record.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

#### `write_date`

```python
write_date: datetime
```

The time the record was last modified.

#### `write_uid`

```python
write_uid: int
```

The ID of the partner that last modified this record.

#### `write_name`

```python
write_name: str
```

The name of the partner that modified this record.

#### `write_user`

```python
write_user: Partner
```

The partner that last modified this record.

This fetches a full Partner object from Odoo once,
and caches it for subsequence access.

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
User(record={'id': 1234, 'name': 'Old Name', ...}, fields=None)
>>> user.unlink()
>>> user.refresh()
...
openstack_odooclient.exceptions.RecordNotFoundError: User record not found with ID: 1234
```
