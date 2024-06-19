# Sale Order Lines

This page documents how to use the manager and record objects
for sale order lines.

## Details

| Name            | Value                        |
|-----------------|------------------------------|
| Odoo Modules    | Sales, OpenStack Integration |
| Odoo Model Name | `sale.order.line`            |
| Manager         | `sale_order_lines`           |
| Record Type     | `SaleOrderLine`              |

## Manager

The sale order line manager is available as the `sale_order_lines`
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
>>> odoo_client.sale_order_lines.get(1234)
SaleOrderLine(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The sale order line manager returns `SaleOrderLine` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import SaleOrderLine
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `company_id`

```python
company_id: int
```

The ID for the [company](company.md) this sale order line
was generated for.

### `company_name`

```python
company_name: str
```

The name of the [company](company.md) this sale order line
was generated for.

### `company`

```python
company: Company
```

The [company](company.md) this sale order line
was generated for.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `currency_id`

```python
currency_id: int
```

The ID for the [currency](currency.md) used in this sale order line.

### `currency_name`

```python
currency_name: str
```

The name of the [currency](currency.md) used in this sale order line.

### `currency`

```python
currency: Currency
```

The [currency](currency.md) used in this sale order line.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `discount`

```python
discount: float
```

Discount percentage on the sale order line (0-100).

### `display_name`

```python
display_name: str
```

Display name for the sale order line in the sale order.

### `invoice_line_ids`

```python
invoice_line_ids: list[int]
```

A list of IDs for the [account move (invoice) lines](account-move-line.md) created
from this sale order line.

### `invoice_lines`

```python
invoice_lines: list[AccountMoveLine]
```

The [account move (invoice) lines](account-move-line.md) created
from this sale order line.

This fetches the full records from Odoo once,
and caches them for subsequent accesses.

### `invoice_status`

```python
invoice_status: Literal["no", "to invoice", "invoiced", "upselling"]
```

The current invoicing status of this sale order line.

Values:

* ``no`` - Nothing to invoice
* ``to invoice`` - Has quantity that needs to be invoiced
* ``invoiced`` - Fully invoiced
* ``upselling`` - Upselling opportunity

### `is_downpayment`

```python
is_downpayment: bool
```

Whether or not this sale order line is a downpayment.

### `is_expense`

```python
is_expense: bool
```

Whether or not this sale order line is an expense.

### `name`

```python
name: str
```

Name assigned to the the sale order line.

This is not the same as the product name.
In the OpenStack Integration add-on, this is normally used to store
the resource's name.

### `order_id`

```python
order_id: int
```

The ID for the [sale order](sale-order.md) this line is linked to.

### `order_name`

```python
order_name: str
```

The name of the [sale order](sale-order.md) this line is linked to.

### `order`

```python
order: SaleOrder
```

The [sale order](sale-order.md) this line is linked to.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `order_partner_id`

```python
order_partner_id: int
```

The ID for the recipient [partner](partner.md) for the sale order.

### `order_partner_name`

```python
order_partner_name: str
```

The name of the recipient [partner](partner.md) for the sale order.

### `order_partner`

```python
order_partner: Partner
```

The recipient [partner](partner.md) for the sale order.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `os_project_id`

```python
os_project_id: int | None
```

The ID for the the [OpenStack project](project.md) this sale order line was
was generated for.

### `os_project_name`

```python
os_project_name: str | None
```

The name of the the [OpenStack project](project.md) this sale order line was
was generated for.

### `os_project`

```python
os_project: Project | None
```

The [OpenStack project](project.md) this sale order line was
was generated for.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `os_region`

```python
os_region: str | Literal[False]
```

The OpenStack region the sale order line was created from.

### `os_resource_id`

```python
os_resource_id: str | Literal[False]
```

The OpenStack resource ID for the resource that generated
this sale order line.

### `os_resource_name`

```python
os_resource_name: str | Literal[False]
```

The name of the OpenStack resource tier or flavour,
as used by services such as Distil for rating purposes.

For example, if this is the sale order line for a compute instance,
this would be set to the instance's flavour name.

### `os_resource_type`

```python
os_resource_type: str | Literal[False]
```

A human-readable description of the type of resource captured
by this sale order line.


### `price_reduce`

```python
price_reduce: float
```

Base unit price, less discount (see the ``discount`` field).

### `price_reduce_taxexcl`

```python
price_reduce_taxexcl: float
```

Actual unit price, excluding tax.

### `price_reduce_taxinc`

```python
price_reduce_taxinc: float
```

Actual unit price, including tax.

### `price_subtotal`

```python
price_subtotal: float
```

Subtotal price for the sale order line, excluding tax.

### `price_tax`

```python
price_tax: float
```

Tax charged on the sale order line.

### `price_total`

```python
price_total: float
```

Total price for the sale order line, including tax.

### `price_unit`

```python
price_unit: float
```

Base unit price, excluding tax, before any discounts.

### `product_id`

```python
product_id: int
```

The ID of the [product](product.md) charged on this sale order line.

### `product_name`

```python
product_name: str
```

The name of the [product](product.md) charged on this sale order line.

### `product`

```python
product: Product
```

The [product](product.md) charged on this sale order line.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `product`

```python
product_uom_id: int
```

The ID for the [Unit of Measure](uom.md) for the product being charged in
this sale order line.

### `product_uom_name`

```python
product_uom_name: str
```

The name of the [Unit of Measure](uom.md) for the product being charged in
this sale order line.

### `product_uom`

```python
product_uom: Uom
```

The [Unit of Measure](uom.md) for the product being charged in
this sale order line.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `product_uom_qty`

```python
product_uom_qty: float
```

The product quantity on the sale order line.

### `product_uom_readonly`

```python
product_uom_readonly: bool
```

Whether or not the product quantity can still be updated
on this sale order line.

### `product_updatable`

```python
product_updatable: bool
```

Whether or not the product can be edited on this sale order line.

### `qty_invoiced`

```python
qty_invoiced: float
```

The product quantity that has already been invoiced.

### `qty_to_invoice`

```python
qty_to_invoice: float
```

The product quantity that still needs to be invoiced.

### `salesman_id`

```python
salesman_id: int
```

The ID for the salesperson [partner](partner.md) assigned
to this sale order line.

### `salesman_name`

```python
salesman_name: str
```

The name of the salesperson [partner](partner.md) assigned
to this sale order line.

### `salesman`

```python
salesman: Partner
```

The salesperson [partner](partner.md) assigned
to this sale order line.

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
* ``cancel`` - Cancelled sale order, can be deleted

### `tax_id`

```python
tax_id: int
```

The ID for the [tax](tax.md) used on this sale order line.

### `tax_name`

```python
tax_name: str
```

The name of the [tax](tax.md) used on this sale order line.

### `tax`

```python
tax: Tax
```

The [tax](tax.md) used on this sale order line.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `untaxed_amount_invoiced`

```python
untaxed_amount_invoiced: float
```

The balance, excluding tax, on the sale order line that
has already been invoiced.

### `untaxed_amount_to_invoice`

```python
untaxed_amount_to_invoice: float
```

The balance, excluding tax, on the sale order line that
still needs to be invoiced.
