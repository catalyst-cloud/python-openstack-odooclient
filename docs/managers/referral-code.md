# OpenStack Referral Codes

This page documents how to use the manager and record objects
for referral codes.

## Details

| Name            | Value                     |
|-----------------|---------------------------|
| Odoo Modules    | OpenStack Integration     |
| Odoo Model Name | `openstack.referral_code` |
| Manager         | `referral_codes`          |
| Record Type     | `ReferralCode`            |

## Manager

The project manager is available as the `referral_codes`
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
>>> odoo_client.referral_codes.get(1234)
ReferralCode(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The referral code manager returns `ReferralCode` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import ReferralCode
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `allowed_uses`

```python
allowed_uses: int
```

The number of allowed uses of this referral code.

Set to `-1` for unlimited uses.

### `before_reward_usage_threshold`

```python
before_reward_usage_threshold: float
```

The amount of usage that must be recorded by the new sign-up
before the reward credit is awarded to the referrer.

### `code`

```python
code: str
```

The unique referral code.

### `name`

```python
name: str
```

Automatically generated name for the referral code.

### `referral_ids`

```python
referral_ids: list[int]
```

A list of IDs for the [partners](partner.md) that signed up
using this referral code.

### `referrals`

```python
referrals: list[Partner]
```

The [partners](partner.md) that signed up using this referral code.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `referral_credit_amount`

```python
referral_credit_amount: float
```

Initial balance for the referral credit.

### `referral_credit_duration`

```python
referral_credit_duration: int
```

Duration of the referral credit, in days.

### `referral_credit_type_id`

```python
referral_credit_type_id: int
```

The ID of the [credit type](credit-type.md) to use for the referral credit.

### `referral_credit_type_name`

```python
referral_credit_type_name: str
```

The name of the [credit type](credit-type.md) to use for the referral credit.

### `referral_credit_type`

```python
referral_credit_type: CreditType
```

The [credit type](credit-type.md) to use for the referral credit.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `reward_credit_amount`

```python
reward_credit_amount: float
```

Initial balance for the reward credit.

### `reward_credit_duration`

```python
reward_credit_duration: int
```

Duration of the reward credit, in days.

### `reward_credit_type_id`

```python
reward_credit_type_id: int
```

The ID of the [credit type](credit-type.md) to use for the reward credit.

### `reward_credit_type_name`

```python
reward_credit_type_name: str
```

The name of the [credit type](credit-type.md) to use for the reward credit.

### `reward_credit_type`

```python
reward_credit_type: CreditType
```

The [credit type](credit-type.md) to use for the reward credit.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
