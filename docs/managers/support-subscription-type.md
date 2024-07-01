# OpenStack Support Subscription Types

This page documents how to use the manager and record objects
for support subscription types.

## Details

| Name            | Value                                 |
|-----------------|---------------------------------------|
| Odoo Modules    | OpenStack Integration                 |
| Odoo Model Name | `openstack.support_subscription.type` |
| Manager         | `support_subscription_types`          |
| Record Type     | `SupportSubscriptionType`             |

## Manager

The support subscription type manager is available as the `support_subscription_types`
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
>>> odoo_client.support_subscription_types.get(1234)
SupportSubscriptionType(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The support subscription type manager returns `SupportSubscriptionType` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import SupportSubscriptionType
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `billing_type`

```python
billing_type: Literal["paid", "complimentary"]
```

The type of support subscription.

Values:

* ``paid`` - Charge the subscription independently
* ``complimentary`` - Bundled with a contract that includes the charge

### `name`

```python
name: str
```
The name of the support subscription type.

### `product_id`

```python
product_id: int
```

The ID for the [product](product.md) to use to invoice
the support subscription.

### `product_name`

```python
product_name: str
```

The name of the [product](product.md) to use to invoice
the support subscription.


### `product`

```python
product: Product
```

The [product](product.md) to use to invoice
the support subscription.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `usage_percent`

```python
usage_percent: float
```

Percentage of usage compared to price (0-100).

### `support_subscription_ids`

```python
support_subscription_ids: list[int]
```

A list of IDs for the [support subscriptions](support-subscription.md) of this type.

### `support_subscription`

```python
support_subscription: list[SupportSubscription]
```

The list of [support subscriptions](support-subscription.md) of this type.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `support_subscriptions`

```python
support_subscriptions: list[SupportSubscription]
```

An alias for [``support_subscription``](#support_subscription).
