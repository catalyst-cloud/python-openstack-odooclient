# OpenStack Support Subscriptions

This page documents how to use the manager and record objects
for support subscriptions.

## Details

| Name            | Value                            |
|-----------------|----------------------------------|
| Odoo Modules    | OpenStack Integration            |
| Odoo Model Name | `openstack.support_subscription` |
| Manager         | `support_subscriptions`          |
| Record Type     | `SupportSubscription`            |

## Manager

The support subscription manager is available as the `support_subscriptions`
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
>>> odoo_client.support_subscriptions.get(1234)
SupportSubscription(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The support subscription manager returns `SupportSubscription` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import SupportSubscription
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `billing_type`

```python
billing_type: Literal["paid", "complimentary"]
```

The method of billing for the support subscription.

Values:

* ``paid`` - Charge the subscription independently
* ``complimentary`` - Bundled with a contract that includes the charge


### `end_date`

```python
end_date: date
```

The end date of the credit.

### `partner_id`

```python
partner_id: int | None
```

The ID for the [partner](partner.md) linked to this support subscription,
if it is linked to a partner.

Support subscriptions linked to a partner
cover all projects the partner owns.

### `partner_name`

```python
partner_name: str | None
```

The name of the [partner](partner.md) linked to this support subscription,
if it is linked to a partner.

Support subscriptions linked to a partner
cover all projects the partner owns.

### `partner`

```python
partner: Partner | None
```

The [partner](partner.md) linked to this support subscription,
if it is linked to a partner.

Support subscriptions linked to a partner
cover all projects the partner owns.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `project_id`

```python
project_id: int | None
```

The ID of the [project](project.md) this support subscription is for,
if it is linked to a specific project.

### `project_name`

```python
project_name: str | None
```

The name of the [project](project.md) this support subscription is for,
if it is linked to a specific project.

### `project`

```python
project: Project | None
```

The [project](project.md) this support subscription is for,
if it is linked to a specific project.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `start_date`

```python
start_date: date
```

The start date of the credit.

### `support_subscription_type_id`

```python
support_subscription_type_id: int
```

The ID of the [type](support-subscription-type.md) of the support subscription.

### `support_subscription_type_name`

```python
support_subscription_type_name: str
```

The name of the [type](support-subscription-type.md) of the support subscription.

### `support_subscription_type`

```python
support_subscription_type: SupportSubscriptionType
```

The [type](support-subscription-type.md) of the support subscription.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
