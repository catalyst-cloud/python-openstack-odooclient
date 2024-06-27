# Performance Considerations

The OpenStack Odoo Client library uses [OdooRPC](https://pythonhosted.org/OdooRPC)
to communicate with Odoo. OdooRPC performs synchronous RPC requests, some of which
can take a long time to execute depending on what work is being done.

Optimising performance when interfacing with Odoo mostly revolves around minimising
the number of requests, and reducing the amount of data selected to the minimum
necessary. The OpenStack Odoo Client library offers a few ways of doing this.

## Selecting Fields

By default, all fields on a record are selected when performing queries.

When querying a lot of records this can mean a lot more data is being selected,
serialised and deserialised than necessary, causing requests to take longer
than they need to.

```python
>>> from datetime import datetime
>>> from openstack_odooclient import Client
>>> odoo_client = Client(...)
>>> before_dt = datetime.now()
>>> odoo_client.products.get_sellable_company_products(1234)
>>> print(f"{(datetime.now() - before_dt).total_seconds():.1f} seconds")
2.1 seconds
```

If requests are taking longer than expected, try using the `fields` parameter on the
query method to limit the selected fields to only the fields required for the task.

```python
>>> from datetime import datetime
>>> from openstack_odooclient import Client
>>> odoo_client = Client(...)
>>> before_dt = datetime.now()
>>> odoo_client.products.get_sellable_company_products(1234, fields={"name", "default_code"})
>>> print(f"{(datetime.now() - before_dt).total_seconds():.1f} seconds")
0.4 seconds
```

You can also query only the record IDs using the `as_id` parameter on
the query method. This eliminates the step where the record contents are fetched,
improving performance further, but means that you will need to make another query
to fetch the contents of records when required.

```python
>>> from datetime import datetime
>>> from openstack_odooclient import Client
>>> odoo_client = Client(...)
>>> before_dt = datetime.now()
>>> odoo_client.products.get_sellable_company_products(1234, as_id=True)
>>> print(f"{(datetime.now() - before_dt).total_seconds():.1f} seconds")
0.2 seconds
```

## Clustering Queries

The Odoo Client library provides nested model references on record objects,
which makes it easier to interface with Odoo records in a more Pythonic manner.

However, using them results in the application making a number of smaller
requests to Odoo to retrieve records, which is not very efficient.
Depending on the use case, other ways of querying records are preferable.

```python
>>> from openstack_odooclient import Client
>>> odoo_client = Client(...)
>>> invoice = odoo_client.account_moves.get(1234)
>>> for invoice_line in invoice.invoice_lines:
...     print(
...         (
...             f"{invoice_line.name}"
...             f"- {invoice_line.product.name}"
...             f" - {invoice_line.quantity} {invoice_line.product.default_code}"
...             f" - {invoice.price_subtotal}"
...         ),
...     )
...
test-instance-1 - m1.small - 1.0 hour - 0.012
test-instance - m1.small - 744.0 hour - 8.928
```

In the above example, [`invoice_line.product`](managers/account-move-line.md#product),
which is a [product](managers/product.md) model ref within an
[account move (invoice) line](managers/account-move-line.md), would be
individually queried for each invoice line in the loop, increasing the runtime
of the task.

Some record types, such as products as shown above, are commonly referenced in
relationships in a number of other record types. For these record types,
it is usually more efficient to fetch all of them in a single dedicated query,
save the resulting objects, and reference the objects using the record's IDs.

```python
>>> from openstack_odooclient import Client
>>> odoo_client = Client(...)
>>> products = {
...     p.id: p
...     for p in odoo_client.products.get_sellable_company_products(
...         company=5678,
...     )
... }
>>> invoice = odoo_client.account_moves.get(1234)
>>> for invoice_line in invoice.invoice_lines:
...     product = products[invoice_line.product_id]
...     print(
...         (
...             f"{invoice_line.name}"
...             f"- {product.name}"
...             f" - {invoice_line.quantity} {product.default_code}"
...             f" - {invoice.price_subtotal}"
...         ),
...     )
...
test-instance-1 - m1.small - 1.0 hour - 0.012
test-instance - m1.small - 744.0 hour - 8.928
```

## Creating Records

In many cases multiple records need to be created that have a relationship
with each other.

In the below example an empty [sale order](managers/sale-order.md) is created,
with a [sale order line](managers/sale-order-line.md) then being created and
linked to that sale order. Since a sale order can have multiple sale order
lines, creating sale orders this way can be inefficient.

```python
>>> from datetime import date
>>> from openstack_odooclient import Client
>>> odoo_client = Client(...)
>>> order = odoo_client.sales_orders.create(
...     user=5678,
...     partner=9012,
...     os_invoice_date=date(2024, 6, 30),
...     os_invoice_due_date=date(2024, 7, 20),
...     os_project=3456,
...     order_lines=[],
... )
>>> odoo_client.sale_order_lines.create(
...     name="test-instance",
...     product=7890,
...     product_uom=123456,
...     product_uom_qty=1.0,
...     price_unit=0.05,
...     os_project=3456,
...     os_resource_id="1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a",
...     os_region="RegionOne",
...     os_resource_type="Virtual Machine",
...     os_resource_name="m1.small",
...     order=order,
... )
789012
```

If the contents of the sale order lines are known before the sale order is
created, this can be optimised by nesting the sale order lines within the
[`create`](managers/index.md#create) method call for the sale order itself,
as shown below.

All of the child records will be created and linked to the parent record,
in a single request.

```python
>>> from datetime import date
>>> from openstack_odooclient import Client
>>> odoo_client = Client(...)
>>> odoo_client.sales_orders.create(
...     user=5678,
...     partner=9012,
...     os_invoice_date=date(2024, 6, 30),
...     os_invoice_due_date=date(2024, 7, 20),
...     os_project=3456,
...     order_lines=[
...         {
...             "name": "test-instance",
...             "product": 7890,
...             "product_uom": 123456,
...             "product_uom_qty": 1.0,
...             "price_unit": 0.05,
...             "os_project": 3456,
...             "os_resource_id": "1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a",
...             "os_region": "RegionOne",
...             "os_resource_type": "Virtual Machine",
...             "os_resource_name": "m1.small",
...         },
...     ],
... )
1234
```

This can be done for any record type with a list of references
to another record type (a `One2many` or `Many2many` relation).
