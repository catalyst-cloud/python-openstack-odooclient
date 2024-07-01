# Taxes

This page documents how to use the manager and record objects
for taxes.

## Details

| Name            | Value         |
|-----------------|---------------|
| Odoo Modules    | Accounting    |
| Odoo Model Name | `account.tax` |
| Manager         | `taxes`       |
| Record Type     | `Tax`         |

## Manager

The tax manager is available as the `taxes`
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
>>> odoo_client.taxes.get(1234)
Tax(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The tax manager returns `Tax` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Tax
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `active`

```python
active: bool
```

Whether or not this tax is active (enabled).

### `amount`

```python
amount: float
```

The amount of tax to apply.

### `amount_type`

```python
amount_type: Literal["group", "fixed", "percent", "division"]
```

The method that should be used to tax invoices.

Values:

* ``group`` - Group of Taxes
* ``fixed`` - Fixed
* ``percent`` - Percentage of Price
* ``division`` - Percentage of Price Tax Included

### `analytic`

```python
analytic: bool
```

When set to ``True``, the amount computed by this tax will be assigned
to the same analytic account as the invoice line (if any).


### `company_id`

```python
company_id: int
```

The ID for the [company](company.md) this tax is owned by.

### `company_name`

```python
company_name: str
```

The name of the [company](company.md) this tax is owned by.

### `company`

```python
company: Company
```

The [company](company.md) this tax is owned by.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `country_code`

```python
country_code: str
```

The country code for this tax.

### `description`

```python
description: str
```

The label for this tax on invoices.

### `include_base_amount`

```python
include_base_amount: bool
```

When set to ``True``, taxes included after this one will be calculated
based on the price with this tax included.

### `name`

```python
name: str
```

Name of the tax.

### `price_include`

```python
price_include: bool
```

Whether or not prices included in invoices should include this tax.

### `tax_eligibility`

```python
tax_eligibility: Literal["on_invoice", "on_payment"]
```

When the tax is due for the invoice.

Values:

* ``on_invoice`` - Due as soon as the invoice is validated
* ``on_payment`` - Due as soon as payment of the invoice is received

### `tax_group_id`

```python
tax_group_id: int
```

The ID for the [tax group](tax-group.md) this tax is categorised under.

### `tax_group_name`

```python
tax_group_name: str
```

The name of the [tax group](tax-group.md) this tax is categorised under.

### `tax_group`

```python
tax_group: TaxGroup
```

The [tax group](tax-group.md) this tax is categorised under.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.
