# Sale Orders

This page documents how to use the manager and record objects
for sale orders.

## Details

| Name            | Value                        |
|-----------------|------------------------------|
| Odoo Modules    | Sales, OpenStack Integration |
| Odoo Model Name | `sale.order`                 |
| Manager         | `sale_orders`                |
| Record Type     | `SaleOrder`                  |

## Manager

The sale order manager is available as the `sale_orders`
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
>>> odoo_client.sale_orders.get(1234)
SaleOrder(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

The following manager methods are also available, in addition to the standard methods.

### `action_cancel`

```python
action_cancel(
    sale_order: int | SaleOrder,
) -> None
```

Cancel the given sale order.

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
>>> odoo_client.sale_orders.action_cancel(
...     sale_order=1234,  # ID or object
... )
```

*Added in version 0.2.1.*

#### Parameters

| Name         | Type              | Description              | Default    |
|--------------|-------------------|--------------------------|------------|
| `sale_order` | `int | SaleOrder` | The sale order to cancel | (required) |

### `action_confirm`

```python
action_confirm(
    sale_order: int | SaleOrder,
) -> None
```

Confirm the given sale order.

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
>>> odoo_client.sale_orders.action_confirm(
...     sale_order=1234,  # ID or object
... )
```

#### Parameters

| Name         | Type              | Description               | Default    |
|--------------|-------------------|---------------------------|------------|
| `sale_order` | `int | SaleOrder` | The sale order to confirm | (required) |

### `create_invoices`

```python
create_invoices(
    sale_order: int | SaleOrder,
) -> None
```

Create invoices from the given sale order.

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
>>> odoo_client.sale_orders.create_invoices(
...     sale_order=1234,  # ID or object
... )
```

#### Parameters

| Name         | Type              | Description                            | Default    |
|--------------|-------------------|----------------------------------------|------------|
| `sale_order` | `int | SaleOrder` | The sale order to create invoices from | (required) |

## Record

The sale order manager returns `SaleOrder` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import SaleOrder
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `amount_untaxed`

```python
amount_untaxed: float
```

The untaxed total cost of the sale order.

### `amount_tax`

```python
amount_tax: float
```

The amount in taxes on this sale order.

### `amount_total`

```python
amount_total: float
```

The taxed total cost of the sale order.

### `client_order_ref`

```python
client_order_ref: str | Literal[False]
```

The customer reference for this sale order, if defined.

### `currency_id`

```python
currency_id: int
```

The ID for the [currency](currency.md) used in this sale order.

### `currency_name`

```python
currency_name: str
```

The name of the [currency](currency.md) used in this sale order.

### `currency`

```python
currency: Currency
```

The [currency](currency.md) used in this sale order.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `date_order`

```python
date_order: datetime
```

The time the sale order was created.

### `display_name`

```python
display_name: str
```

The display name of the sale order.

### `invoice_count`

```python
invoice_count: int
```

The number of [invoices (account moves)](account-move.md) generated from the sale order.

*Added in version 0.2.1.*

### `invoice_ids`

```python
invoice_ids: list[int]
```

A list of IDs for [invoices (account moves)](account-move.md) generated from the sale order.

*Added in version 0.2.1.*

### `invoices`

```python
invoices: list[AccountMove]
```

The [invoices (account moves)](account-move.md) generated from the sale order.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

*Added in version 0.2.1.*

### `invoice_status`

```python
invoice_status: Literal["no", "to invoice", "invoiced", "upselling"]
```

The current invoicing status of this sale order.

Values:

* ``no`` - Nothing to invoice
* ``to invoice`` - Has line items that need to be invoiced
* ``invoiced`` - Fully invoiced
* ``upselling`` - Upselling opportunity

### `name`

```python
name: str
```

The name assigned to the sale order.

### `note`

```python
note: str
```

A note attached to the sale order.

Generally used for terms and conditions.

### `order_line_ids`

```python
order_line_ids: list[int]
```

A list of IDs for the [lines](sale-order-line.md) added to the sale order.

### `order_line`

```python
order_line: list[SaleOrderLine]
```

The [lines](sale-order-line.md) added to the sale order.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `order_lines`

```python
order_lines: list[SaleOrderLine]
```

An alias for [``order_line``](#order_line).

### `os_invoice_date`

```python
os_invoice_date: date
```

The invoicing date for the invoice that is created
from the sale order.

### `os_invoice_due_date`

```python
os_invoice_due_date: date
```

The due date for the invoice that is created
from the sale order.

### `os_project_id`

```python
os_project_id: int | None
```

The ID for the the [OpenStack project](project.md) this sale order was
was generated for.

### `os_project_name`

```python
os_project_name: str | None
```

The name of the the [OpenStack project](project.md) this sale order was
was generated for.

### `os_project`

```python
os_project: Project | None
```

The [OpenStack project](project.md) this sale order was
was generated for.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `partner_id`

```python
partner_id: int
```

The ID for the recipient [partner](partner.md) for the sale order.

### `partner_name`

```python
partner_name: str
```

The name of the recipient partner for the sale order.

### `partner`

```python
partner: Partner
```

The recipient [partner](partner.md) for the sale order.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `state`

```python
state: Literal["draft", "sale", "done", "cancel"]
```

State of the sale order.

Values:

* ``draft`` - Draft sale order (quotation), can still be modified
* ``sale`` - Finalised sale order, cannot be modified
* ``done`` - Finalised and settled sale order, cannot be modified
* ``cancel`` - Cancelled sale order, can be deleted in most cases

### `action_cancel`

```python
action_cancel() -> None
```

Cancel this sale order.

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
>>> sale_order = odoo_client.sale_orders.get(1234)
>>> sale_order.action_cancel()
```

*Added in version 0.2.1.*

### `action_confirm`

```python
action_confirm() -> None
```

Confirm this sale order.

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
>>> sale_order = odoo_client.sale_orders.get(1234)
>>> sale_order.action_confirm()
```

### `create_invoices`

```python
create_invoices() -> None
```

Create invoices from this sale order.

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
>>> sale_order = odoo_client.sale_orders.get(1234)
>>> sale_order.create_invoices()
```
