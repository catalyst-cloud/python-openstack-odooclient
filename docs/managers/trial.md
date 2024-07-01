# OpenStack Trials

This page documents how to use the manager and record objects
for trials.

## Details

| Name            | Value                 |
|-----------------|-----------------------|
| Odoo Modules    | OpenStack Integration |
| Odoo Model Name | `openstack.trial`     |
| Manager         | `trials`              |
| Record Type     | `Trial`               |

## Manager

The trial manager is available as the `trials`
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
>>> odoo_client.trials.get(1234)
Trial(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

## Record

The trial manager returns `Trial` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Trial
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `account_suspended_date`

```python
account_suspended_date: date | Literal[False]
```

The date the account was suspended, following the end of the trial.

### `account_terminated_date`

```python
account_terminated_date: date | Literal[False]
```

The date the account was terminated, following the end of the trial.

### `account_upgraded_date`

```python
account_upgraded_date: date | Literal[False]
```

The date the account was upgraded to a full account,
following the end of the trial.

### `end_date`

```python
end_date: date
```

The end date of this trial.

### `partner_id`

```python
partner_id: int
```

The ID for the target [partner](partner.md) for this trial.

### `partner_name`

```python
partner_name: str
```

The name of the target [partner](partner.md) for this trial.

### `partner`

```python
partner: Partner
```

The target [partner](partner.md) for this trial.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `start_date`

```python
start_date: date
```

The start date of this trial.
