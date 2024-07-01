# Partners

This page documents how to use the manager and record objects
for partners.

## Details

| Name            | Value                                       |
|-----------------|---------------------------------------------|
| Odoo Modules    | Base, Product, Sales, OpenStack Integration |
| Odoo Model Name | `res.partner`                               |
| Manager         | `partners`                                  |
| Record Type     | `Partner`                                   |

## Manager

The partner manager is available as the `partners`
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
>>> odoo_client.partners.get(1234)
Partner(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The partner manager returns `Partner` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Partner
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `active`

```python
active: bool
```

Whether or not this partner is active (enabled).

### `company_id`

```python
company_id: int
```

The ID for the [company](company.md) this partner is owned by.

### `company_name`

```python
company_name: str
```

The name of the [company](company.md) this partner is owned by.

### `company`

```python
company: Company
```

The [company](company.md) this partner is owned by.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `email`

```python
email: str
```

Main e-mail address for the partner.

### `name`

```python
name: str
```

Full name of the partner.

### `os_customer_group_id`

```python
os_customer_group_id: int | None
```

The ID for the [customer group](customer-group.md) this partner is part of,
if it is part of one.

### `os_customer_group_name`

```python
os_customer_group_name: str | None
```

The name of the [customer group](customer-group.md) this partner is part of,
if it is part of one.

### `os_customer_group`

```python
os_customer_group: CustomerGroup
```

The [customer group](customer-group.md) this partner is part of,
if it is part of one.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `os_project_ids`

```python
os_project_ids: list[int]
```

A list of IDs for the [OpenStack projects](project.md) that
belong to this partner.

### `os_projects`

```python
os_projects: list[project.Project]
```

The [OpenStack projects](project.md) that belong to this partner.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `os_project_contact_ids`

```python
os_project_contact_ids: list[int]
```

A list of IDs for the [project contacts](project-contact.md) that are associated
with this partner.

### `os_project_contacts`

```python
os_project_contacts: list[ProjectContact]
```

The [project contacts](project-contact.md) that are associated with this partner.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `os_referral_id`

```python
os_referral_id: int | None
```

The ID for the [referral code](referral-code.md) the partner used on sign-up,
if one was used.

### `os_referral_name`

```python
os_referral_name: str | None
```

The name of the [referral code](referral-code.md) the partner used on sign-up,
if one was used.

### `os_referral`

```python
os_referral: ReferralCode
```

The [referral code](referral-code.md) the partner used on sign-up, if one was used.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `os_referral_code_ids`

```python
os_referral_code_ids: list[int]
```

A list of IDs for the [referral codes](referral-code.md) the partner has used.

### `os_referral_codes`

```python
os_referral_codes: list[ReferralCode]
```

The [referral codes](referral-code.md) the partner has used.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `os_reseller_id`

```python
os_reseller_id: int | None
```

The ID for the [reseller](reseller.md) for this partner, if this partner
is billed through a reseller.

### `os_reseller_name`

```python
os_reseller_name: str | None
```

The name of the [reseller](reseller.md) for this partner, if this partner
is billed through a reseller.

### `os_reseller`

```python
os_reseller: Reseller | None
```

The [reseller](reseller.md) for this partner, if this partner
is billed through a reseller.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `os_trial_id`

```python
os_trial_id: int | None
```

The ID for the sign-up [trial](trial.md) for this partner,
if signed up under a trial.

### `os_trial_name`

```python
os_trial_name: str | None
```

The name of the sign-up [trial](trial.md) for this partner,
if signed up under a trial.

### `os_trial`

```python
os_trial: Trial | None
```

The sign-up [trial](trial.md) for this partner,
if signed up under a trial.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `parent_id`

```python
parent_id: int | None
```

The ID for the parent partner of this partner,
if it has a parent.

### `parent_name`

```python
parent_name: str | None
```

The name of the parent partner of this partner,
if it has a parent.

### `parent`

```python
parent: Partner | None
```

The parent partner of this partner,
if it has a parent.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `property_product_pricelist_id`

```python
property_product_pricelist_id: int | None
```

The ID for the [pricelist](pricelist.md) this partner uses, if explicitly set.

If not set, the pricelist set for the customer group
is used (and if that is not set, the global default
pricelist is used).

### `property_product_pricelist_name`

```python
property_product_pricelist_name: str | None
```

The name of the [pricelist](pricelist.md) this partner uses, if explicitly set.

If not set, the pricelist set for the customer group
is used (and if that is not set, the global default
pricelist is used).

### `property_product_pricelist`

```python
property_product_pricelist: Pricelist | None
```

The [pricelist](pricelist.md) this partner uses, if explicitly set.

If not set, the pricelist set for the customer group
is used (and if that is not set, the global default
pricelist is used).

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `stripe_customer_id`

```python
stripe_customer_id: str | Literal[False]
```

Stripe customer ID for this partner, if one has been assigned.

### `user_id`

```python
user_id: int | None
```

The ID of the internal [user](user.md) associated with this partner,
if one is assigned.

### `user_name`

```python
user_name: str | None
```

The name of the internal [user](user.md) associated with this partner,
if one is assigned.

### `user`

```python
user: User | None
```

The internal [user](user.md) associated with this partner,
if one is assigned.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
