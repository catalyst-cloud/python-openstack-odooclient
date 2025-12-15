# OpenStack Voucher Codes

This page documents how to use the manager and record objects
for voucher codes.

## Details

| Name            | Value                    |
|-----------------|--------------------------|
| Odoo Modules    | OpenStack Integration    |
| Odoo Model Name | `openstack.voucher_code` |
| Manager         | `voucher_codes`          |
| Record Type     | `VoucherCode`            |

## Manager

The voucher code manager is available as the `voucher_codes`
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
>>> odoo_client.voucher_codes.get(1234)
VoucherCode(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The voucher code manager returns `VoucherCode` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import VoucherCode
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `claimed`

```python
claimed: bool
```

Whether or not this voucher code has been claimed.

### `code`

```python
code: str
```

The code string for this voucher code.

### `credit_amount`

```python
credit_amount: float | Literal[False]
```

The initial credit balance for the voucher code, if a credit is to be
created by the voucher code.

### `credit_type_id`

```python
credit_type_id: int | None
```

The ID of the [credit type](credit-type.md) to use, if a credit is to be
created by this voucher code.

### `credit_type_name`

```python
credit_type_name: str | None
```

The name of the [credit type](credit-type.md) to use, if a credit is to be
created by this voucher code.

### `credit_type`

```python
credit_type: CreditType | None
```

The [credit type](credit-type.md) to use, if a credit is to be
created by this voucher code.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `credit_duration`

```python
credit_duration: int | Literal[False]
```

The duration of the [credit](credit.md), in days, if a credit is to be
created by the voucher code.

### `customer_group_id`

```python
customer_group_id: int | None
```

The ID of the [customer group](customer-group.md) to add the customer to, if set.

### `customer_group_name`

```python
customer_group_name: str | None
```

The name of the [customer group](customer-group.md) to add the customer to, if set.

### `customer_group`

```python
customer_group: CustomerGroup | None
```

The [customer group](customer-group.md) to add the customer to, if set.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `expiry_date`

```python
expiry_date: date | Literal[False]
```

The date the voucher code expires.

### `grant_duration`

```python
grant_duration: int | Literal[False]
```

The duration of the [grant](grant.md), in days, if a grant is to be
created by the voucher code.

### `grant_type_id`

```python
grant_type_id: int | None
```

The ID of the [grant type](grant-type.md) to use, if a grant is to be
created by this voucher code.

### `grant_type_name`

```python
grant_type_name: str | None
```

The name of the [grant type](grant-type.md) to use, if a grant is to be
created by this voucher code.

### `grant_type`

```python
grant_type: GrantType | None
```

The [grant type](grant-type.md) to use, if a grant is to be
created by this voucher code.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `grant_value`

```python
grant_value: float | Literal[False]
```

The value of the [grant](grant.md), if a grant is to be
created by the voucher code.

### `multi_use`

```python
multi_use: bool
```

Whether or not this is a multi-use voucher code.

A multi-use voucher code can be used an unlimited number of times
until it expires.

### `name`

```python
name: str
```

The automatically generated name of this voucher code.

This uses the code specified in the record as-is.

### `quota_size`

```python
quota_size: str | Literal[False]
```

The default quota size for new projects signed up
using this voucher code.

If unset, use the default quota size.

### `sales_person_id`

```python
sales_person_id: int | None
```

The ID for the salesperson [partner](partner.md) responsible for this
voucher code, if assigned.

### `sales_person_name`

```python
sales_person_name: str | None
```

The name of the salesperson [partner](partner.md) responsible for this
voucher code, if assigned.

### `sales_person`

```python
sales_person: Partner | None
```

The salesperson [partner](partner.md) responsible for this
voucher code, if assigned.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `tag_ids`

```python
tag_ids: list[int]
```

A list of IDs for the tags ([partner categories](partner-category.md)) to assign
to partners for new accounts that signed up using this voucher code.

### `tags`

```python
tags: list[PartnerCategory]
```

The list of tags ([partner categories](partner-category.md)) to assign
to partners for new accounts that signed up using this voucher code.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.
