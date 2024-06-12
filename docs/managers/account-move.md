# Account Moves (Invoices)

This page documents how to use the manager and record objects
for account moves (invoices).

## Details

| Name            | Value                             |
|-----------------|-----------------------------------|
| Odoo Modules    | Accounting, OpenStack Integration |
| Odoo Model Name | `account.move`                    |
| Manager         | `account_moves`                   |
| Record Type     | `AccountMove`                     |

## Manager

The account move (invoice) manager is available as the `account_moves`
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
>>> odoo_client.account_moves.get(1234)
AccountMove(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The account move (invoice) manager returns `AccountMove` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import AccountMove
```

The record class currently implements the following fields and methods.

### `amount_total`

```python
amount_total: float
```

Total (taxed) amount charged on the account move (invoice).

### `amount_untaxed`

```python
amount_untaxed: float
```

Total (untaxed) amount charged on the account move (invoice).

### `currency_id`

```python
currency_id: int
```

The ID for the currency used in this account move (invoice).

### `currency_name`

```python
currency_name: str
```

The name of the currency used in this account move (invoice).

### `currency`

```python
currency: Currency
```

The currency used in this account move (invoice).

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `invoice_date`

```python
invoice_date: date
```

Date associated with the account move (invoice).

### `invoice_line_ids`

```python
invoice_line_ids: list[int]
```

The list of the IDs for the account move (invoice) lines
that comprise this account move (invoice).

### `invoice_lines`

```python
invoice_lines: list[AccountMoveLine]
```

A list of account move (invoice) lines
that comprise this account move (invoice).

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `is_move_sent`

```python
is_move_sent: bool
```

Whether or not the account move (invoice) has been sent.

### `move_type`

```python
move_type: Literal[
    "entry",
    "out_invoice",
    "out_refund",
    "in_invoice",
    "in_refund",
    "out_receipt",
    "in_receipt",
]
```

The type of account move (invoice).

Values:

* ``entry`` - Journal Entry
* ``out_invoice`` - Customer Invoice
* ``out_refund`` - Customer Credit Note
* ``in_invoice`` - Vendor Bill
* ``in_refund`` - Vendor Credit Note
* ``out_receipt`` - Sales Receipt
* ``in_receipt`` - Purchase Receipt

### `name`

```python
name: str | Literal[False]
```

Name assigned to the account move (invoice), if posted.

### `os_project_id`

```python
os_project_id: int | None
```

The ID of the [OpenStack project](project.md) this account move (invoice)
was generated for, if this is an invoice for OpenStack project usage.

### `os_project_name`

```python
os_project_name: str | None
```

The name of the [OpenStack project](project.md) this account move (invoice)
was generated for, if this is an invoice for OpenStack project usage.

### `os_project`

```python
os_project: Project | None
```

The [OpenStack project](project.md) this account move (invoice)
was generated for, if this is an invoice for OpenStack project usage.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `payment_state`

```python
payment_state: Literal[
    "not_paid",
    "in_payment",
    "paid",
    "partial",
    "reversed",
    "invoicing_legacy",
]
```

The current payment state of the account move (invoice).

Values:

* ``not_paid`` - Not Paid
* ``in_payment`` - In Payment
* ``paid`` - Paid
* ``partial`` - Partially Paid
* ``reversed`` - Reversed
* ``invoicing_legacy`` - Invoicing App Legacy

### state

```python
state: Literal["draft", "posted", "cancel"]
```

The current state of the account move (invoice).

Values:

* ``draft`` - Draft invoice
* ``posted`` - Posted (finalised) invoice
* ``cancel`` - Cancelled invoice
