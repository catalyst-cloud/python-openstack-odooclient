# Currencies

This page documents how to use the manager and record objects
for currencies.

## Details

| Name            | Value            |
|-----------------|------------------|
| Odoo Modules    | Base, Accounting |
| Odoo Model Name | `res.currency`   |
| Manager         | `currencies`     |
| Record Type     | `Currency`       |

## Manager

The currency manager is available as the `currencies`
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
>>> odoo_client.currencies.get(1234)
Currency(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The currency manager returns `Currency` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Currency
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `active`

```python
active: bool
```

Whether or not this currency is active (enabled).

### `currency_unit_label`

```python
currency_unit_label: str | Literal[False]
```

The unit label for this currency, if set.

### `currency_subunit_label`

```python
currency_subunit_label: str | Literal[False]
```

The sub-unit label for this currency, if set.

### `date`

```python
date: date
```

The age of the set currency rate.

### `decimal_places`

```python
decimal_places: int
```

Decimal places taken into account for operations on amounts
in this currency.

It is determined by the rounding factor (``rounding`` field).

### `name`

```python
name: str
```

The ISO-4217 currency code for the currency.

### `position`

```python
position: Literal["before", "after"]
```

The position of the currency unit relative to the amount.

Values:

* ``before`` - Place the unit before the amount
* ``after`` - Place the unit after the amount

### `rate`

```python
rate: float
```

The rate of the currency to the currency of rate 1.

### `rounding`

```python
rounding: float
```

The rounding factor configured for this currency.

### `symbol`

```python
symbol: str
```

The currency sign to be used when printing amounts.
