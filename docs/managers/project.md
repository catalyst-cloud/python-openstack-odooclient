# OpenStack Projects

This page documents how to use the manager and record objects
for projects.

## Details

| Name            | Value                 |
|-----------------|-----------------------|
| Odoo Modules    | OpenStack Integration |
| Odoo Model Name | `openstack.project`   |
| Manager         | `projects`            |
| Record Type     | `Project`             |

## Manager

The project manager is available as the `projects`
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
>>> odoo_client.projects.get(1234)
Project(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

The following manager methods are also available, in addition to the standard methods.

### `get_by_os_id`

```python
get_by_os_id(
    os_id: str,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = False,
    optional: bool = False,
) -> Project
```

```python
get_by_os_id(
    os_id: str,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = False,
    optional: bool = True,
) -> Project | None
```

```python
get_by_os_id(
    os_id: str,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = True,
    as_dict: bool = False,
    optional: bool = False,
) -> int
```

```python
get_by_os_id(
    os_id: str,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = True,
    as_dict: bool = False,
    optional: bool = True,
) -> int | None
```

```python
get_by_os_id(
    os_id: str,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = True,
    optional: bool = False,
) -> dict[str, Any]
```

```python
get_by_os_id(
    os_id: str,
    fields: Iterable[str] | None = None,
    order: str | None = None,
    as_id: bool = False,
    as_dict: bool = True,
    optional: bool = True,
) -> dict[str, Any] | None
```

Query a unique record by OpenStack project ID.

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
>>> odoo_client.projects.get_by_os_id("1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a")
Project(record={'id': 1234, 'name': 'test-project', 'os_id': '1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a', ...}, fields=None)
```

A number of parameters are available to configure the return type,
and what happens when a result is not found.

By default all fields available on the record model
will be selected, but this can be filtered using the
``fields`` parameter.

Use the ``as_id`` parameter to return the ID of the record,
instead of the record object.

Use the ``as_dict`` parameter to return the record as
a ``dict`` object, instead of a record object.

When ``optional`` is ``True``, ``None`` is returned if a record
with the given name does not exist, instead of raising an error.

#### Parameters

| Name       | Type                   | Description                                       | Default    |
|------------|------------------------|---------------------------------------------------|------------|
| `os_id`    | `str`                  | The OpenStack project ID to search for            | (required) |
| `fields`   | `Iterable[str] | None` | Fields to select, defaults to `None` (select all) | `None`     |
| `as_id`    | `bool`                 | Return a record ID                                | `False`    |
| `as_dict`  | `bool`                 | Return the record as a dictionary                 | `False`    |
| `optional` | `bool`                 | Return `None` if not found                        | `False`    |

#### Raises

| Type                        | Description                                                       |
|-----------------------------|-------------------------------------------------------------------|
| `MultipleRecordsFoundError` | Multiple records with the same name were found                    |
| `RecordNotFoundError`       | Record with the given name not found (when `optional` is `False`) |

#### Returns

| Type             | Description                                                                |
|------------------|----------------------------------------------------------------------------|
| `Project`        | Project object (default)                                                   |
| `int`            | Project ID (when `as_id` is `True`)                                        |
| `dict[str, Any]` | Project dictionary (when `as_dict` is `True`)                              |
| `None`           | If a project with the given name was not found (when `optional` is `True`) |

## Record

The project manager returns `Project` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Project
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `display_name`

```python
display_name: str
```

The automatically generated display name for the project.

### `enabled`

```python
enabled: bool
```

Whether or not the project is enabled in Odoo.

### `group_invoices`

```python
group_invoices: bool
```

Whether or not to group invoices together for this project.

### `name`

```python
name: str
```

OpenStack project name.

### `os_id`

```python
os_id: str
```

OpenStack project ID.

### `override_po_number`

```python
override_po_number: bool
```

Whether or not to override the PO number with the value
set on this Project.


### `owner_id`

```python
owner_id: int
```

The ID for the [partner](partner.md) that owns this project.

### `owner_name`

```python
owner_name: str
```

The name of the [partner](partner.md) that owns this project.

### `owner`

```python
owner: Partner
```

The [partner](partner.md) that owns this project.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `parent_id`

```python
parent_id: int | None
```

The ID for the parent project, if this project
is the child of another project.

### `parent_name`

```python
parent_name: str | None
```

The name of the parent project, if this project
is the child of another project.

### `parent`

```python
parent: Project | None
```

The parent project, if this project
is the child of another project.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `payment_method`

```python
payment_method: Literal["invoice", "credit_card"]
```

Payment method configured on the project.

Values:

* ``invoice`` - Project is paid by invoice
* ``credit_card`` - Project is paid by credit card

### `po_number`

```python
po_number: str | Literal[False]
```

The PO number set for this specific Project (if set).

### `project_contact_ids`

```python
project_contact_ids: list[int]
```

A list of IDs for the [contacts](project-contact.md) for this project.

### `project_contacts`

```python
project_contacts: list[ProjectContact]
```

The [contacts](project-contact.md) for this project.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `project_credit_ids`

```python
project_credit_ids: list[int]
```

A list of IDs for the [credits](credit.md) that apply to this project.

### `project_credits`

```python
project_credits: list[Credit]
```

The [credits](credit.md) that apply to this project.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `project_grant_ids`

```python
project_grant_ids: list[int]
```

A list of IDs for the [grants](grant.md) that apply to this project.

### `project_grants`

```python
project_grants: list[Grant]
```

The [grants](grant.md) that apply to this project.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `stripe_card_id`

```python
stripe_card_id: str | Literal[False]
```

The card ID used for credit card payments on this project
using Stripe, if the payment method is set to `credit_card`.

If a credit card has not been assigned to this project,
this field will be set to `False`.

### `support_subscription_id`

```python
support_subscription_id: int | None
```

The ID for the [support subscription](support-subscription.md) for this project,
if the project has one.

### `support_subscription_name`

```python
support_subscription_name: str | None
```

The name of the [support subscription](support-subscription.md) for this project,
if the project has one.

### `support_subscription`

```python
support_subscription: SupportSubscription | None
```

The [support subscription](support-subscription.md) for this project,
if the project has one.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `term_discount_ids`

```python
term_discount_ids: list[int]
```

A list of IDs for the [term discounts](term-discount.md) that apply to this project.

### `term_discounts`

```python
term_discounts: list[TermDiscount]
```

The [term discounts](term-discount.md) that apply to this project.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.
