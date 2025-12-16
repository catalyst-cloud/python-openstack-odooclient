# Attachments

*Added in version 0.2.1.*

This page documents how to use the manager and record objects
for attachments.

## Details

| Name            | Value           |
|-----------------|-----------------|
| Odoo Modules    | Base, Mail      |
| Odoo Model Name | `ir.attachment` |
| Manager         | `attachments`   |
| Record Type     | `Attachment`    |

## Manager

The attachment manager is available as the `attachments`
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
>>> odoo_client.attachments.get(1234)
Attachment(record={'id': 1234, ...}, fields=None)
```

For more information on how to use managers, refer to [Managers](index.md).

The following manager methods are also available, in addition to the standard methods.

### `upload`

```python
def upload(
    name: str,
    data: bytes,
    *,
    record: RecordBase[Any] | None = None,
    res_id: int | None = None,
    res_model: str | None = None,
    type: str = "binary",
    **fields: Any,
) -> int
```

Upload an attachment and associate it with the given record.

One of `record` or `res_id` must be set to specify the record
to link the attachment to. When `res_id` is used, `res_model`
(and in some cases, `res_field`) must also be specified to
define the model of the record.

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
>>> odoo_client.attachments.upload(
...     "example.txt",
...     b"Hello, world!",
...     res_id=1234,
...     res_model="account.move",
...     res_field="message_main_attachment_id",
... )
5678
```

When `record` is used, this is not necessary.

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
>>> account_move = odoo_client.account_moves.get(1234)
>>> odoo_client.attachments.upload(
...     "example.txt",
...     b"Hello, world!",
...     record=account_move,
... )
5678
```

Any keyword arguments passed to this method are passed to
the attachment record as fields.

#### Parameters

| Name        | Type                     | Description                                                    | Default    |
|-------------|--------------------------|----------------------------------------------------------------|------------|
| `name`      | `str`                    | The name of the attachment                                     | (required) |
| `data`      | `bytes`                  | The contents of the attachment                                 | (required) |
| `record`    | `RecordBase[Any] | None` | The linked record (if referencing by object)                   | `None`     |
| `res_id`    | `int | None`             | The ID of the linked record (if referencing by ID)             | `None`     |
| `res_model` | `str | None`             | The model of the linked record (if referencing by ID)          | `None`     |
| `**fields`  | `Any`                    | Additional fields to set on the attachment (keyword arguments) | (none)     |

#### Returns

| Type  | Description                                    |
|-------|------------------------------------------------|
| `int` | The record ID of the newly uploaded attachment |

### `download`

```python
def download(
    attachment: int | Attachment,
) -> bytes
```

Download a given attachment, and return the contents as bytes.

#### Parameters

| Name         | Type               | Description               | Default    |
|--------------|--------------------|---------------------------|------------|
| `attachment` | `int | Attachment` | Attachment (ID or object) | (required) |

#### Returns

| Type    | Description         |
|---------|---------------------|
| `bytes` | Attachment contents |

### `reupload`

```python
def reupload(
    attachment: int | Attachment,
    data: bytes,
    **fields: Any,
) -> None
```

Reupload a new version of the contents of the given attachment,
and update the attachment in place.

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
>>> odoo_client.attachments.download(1234)
b'Goodbye, world!'
>>> odoo_client.attachments.reupload(
...     1234,
...     b"Hello, world!",
... )
>>> odoo_client.attachments.download(1234)
b'Hello, world!'
```

Other fields can be updated at the same time by passing them
as keyword arguments.

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
>>> odoo_client.attachments.get(1234)
Attachment(record={'id': 1234, 'name': 'hello.txt', ...}, fields=None)
>>> odoo_client.attachments.download(1234)
b'Goodbye, world!'
>>> odoo_client.attachments.reupload(
...     1234,
...     b"Hello, world!",
...     name="example.txt",
... )
>>> odoo_client.attachments.get(1234)
Attachment(record={'id': 1234, 'name': 'example.txt', ...}, fields=None)
>>> odoo_client.attachments.download(1234)
b'Hello, world!'
```

Any keyword arguments passed to this method are passed to
the attachment record as fields.

#### Parameters

| Name         | Type               | Description                                                    | Default    |
|--------------|--------------------|----------------------------------------------------------------|------------|
| `attachment` | `int | Attachment` | Attachment (ID or object)                                      | (required) |
| `data`       | `bytes`            | The contents of the attachment                                 | (required) |
| `**fields`   | `Any`              | Additional fields to set on the attachment (keyword arguments) | (none)     |

### `register_as_main_attachment`

```python
def register_as_main_attachment(
    attachment: int | Attachment,
    force: bool = True,
) -> None
```

Register the given attachment as the main attachment
of the record it is attached to.

The model of the attached record must have the
`message_main_attachment_id` field defined.

#### Parameters

| Name         | Type               | Description               | Default    |
|--------------|--------------------|---------------------------|------------|
| `attachment` | `int | Attachment` | Attachment (ID or object) | (required) |
| `force`      | `bool`             | Overwrite if already set  | `True`     |

## Record

The attachment manager returns `Attachment` record objects.

To import the record class for type hinting purposes:

```python
from openstack_odooclient import Attachment
```

The record class currently implements the following fields and methods.

For more information on attributes and methods common to all record types,
see [Record Attributes and Methods](index.md#attributes-and-methods).

### `checksum`

```python
checksum: str
```

A SHA1 checksum of the attachment contents.

### `company_id`

```python
company_id: int | None
```

The ID for the [company](company.md) that owns this attachment, if set.

### `company_name`

```python
company_name: str | None
```

The name of the [company](company.md) that owns this attachment, if set.

### `company`

```python
company: Company | None
```

The [company](company.md) that owns this attachment, if set.

This fetches the full record from Odoo once,
and caches it for subsequent accesses.

### `datas`

```python
datas: str | Literal[False]
```

The contents of the attachment, encoded in base64.

Only applies when [`type`](#type) is set to `binary`.

**This field is not fetched by default.** To make this field available,
use the `fields` parameter on the [`get`](index.md#get) or
[`list`](index.md#list) methods to select the `datas` field.

### `description`

```python
description: str | Literal[False]
```

A description of the file, if defined.

### `index_content`

```python
index_content: str
```

The index content value computed from the attachment contents.

**This field is not fetched by default.** To make this field available,
use the `fields` parameter on the [`get`](index.md#get) or
[`list`](index.md#list) methods to select the `index_content` field.

### `mimetype`

```python
mimetype: str
```

MIME type of the attached file.

### `name`

```python
name: str
```

The name of the attachment.

Usually matches the filename of the attached file.

### `public`

```python
public: bool
```

Whether or not the attachment is publicly accessible.

### `res_field`

```python
res_field: str | Literal[False]
```

The name of the field used to refer to this attachment
on the linked record's model, if set.

### `res_id`

```python
res_id: int | Literal[False]
```

The ID of the record this attachment is linked to, if set.

### `res_model`

```python
res_model: str | Literal[False]
```

The name of the model of the record this attachment
is linked to, if set.

### `res_name`

```python
res_name: str | Literal[False]
```

The name of the record this attachment is linked to, if set.

### `store_fname`

```python
store_fname: str | Literal[False]
```

The stored filename for this attachment, if set.

### `type`

```python
type: Literal["binary", "url"]
```

The type of the attachment.

When set to `binary`, the contents of the attachment are available
using the `datas` field. When set to `url`, the attachment can be
downloaded from the URL configured in the `url` field.

Values:

* `binary` - Stored internally as binary data
* `url` - Stored externally, accessible using a URL

### `url`

```python
url: str | Literal[False]
```

The URL the contents of the attachment are available from.

Only applies when `type` is set to `url`.

### `download`

```python
def download() -> bytes
```

Download this attachment, and return the contents as bytes.

#### Returns

| Type    | Description         |
|---------|---------------------|
| `bytes` | Attachment contents |

### `reupload`

```python
def reupload(
    data: bytes,
    **fields: Any,
) -> None
```

Reupload a new version of the contents of this attachment,
and update the attachment in place.

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
>>> attachment = odoo_client.attachments.get(1234)
>>> attachment.download()
b'Goodbye, world!'
>>> attachment.reupload(b"Hello, world!")
>>> attachment = attachment.refresh()
>>> attachment.download()
b'Hello, world!'
```

Other fields can be updated at the same time by passing them
as keyword arguments.

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
>>> attachment = odoo_client.attachments.get(1234)
>>> attachment
Attachment(record={'id': 1234, 'name': 'hello.txt', ...}, fields=None)
>>> attachment.download()
b'Goodbye, world!'
>>> attachment.reupload(
...     b"Hello, world!",
...     name="example.txt",
... )
>>> attachment = attachment.refresh()
>>> attachment
Attachment(record={'id': 1234, 'name': 'example.txt', ...}, fields=None)
>>> attachment.download()
b'Hello, world!'
```

Any keyword arguments passed to this method are passed to
the attachment record as fields.

!!! note

    This attachment object not updated in place by this method.

    If you need an updated version of the attachment object,
    use the [`refresh`](index.md#refresh) method to fetch the latest version.

#### Parameters

| Name       | Type    | Description                                                    | Default    |
|------------|---------|----------------------------------------------------------------|------------|
| `data`     | `bytes` | The contents of the attachment                                 | (required) |
| `**fields` | `Any`   | Additional fields to set on the attachment (keyword arguments) | (none)     |

### `register_as_main_attachment`

```python
def register_as_main_attachment(
    force: bool = True,
) -> None
```

Register this attachment as the main attachment
of the record it is attached to.

The model of the attached record must have the
`message_main_attachment_id` field defined.

#### Parameters

| Name    | Type   | Description              | Default |
|---------|--------|--------------------------|---------|
| `force` | `bool` | Overwrite if already set | `True`  |
