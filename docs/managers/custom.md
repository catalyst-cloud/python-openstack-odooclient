# Custom Managers and Record Types

The OpenStack Odoo Client library supports defining new record types and
adding managers for them to the Odoo client object, allowing for adding
support for custom Odoo add-ons.

!!! note

    When defining custom record types and managers, it is **highly recommended**
    to enable postponed evaluation of annotations by adding the following future import
    to the top of your Python source files:

    ```python
    from __future__ import annotations
    ```

    If this is not enabled, circular imports are not supported, and you may encounter
    issues with undefined type hint objects.

## Records

Odoo records are represented by **record classes** in the Odoo Client library.

Record classes are implementations (subclasses) of the `RecordBase` class,
which the [record manager](#managers) uses to create immutable objects for the record model.
The name of the record manager (as defined in the Python source file) should
be passed as the generic type argument for `RecordBase`, as a string.

Record fields are defined as type hints on the record class.
These type hints are parsed by the Odoo Client library,
and field values from the API are automatically coerced to the
correct types when referenced by applications.

```python
from __future__ import annotations

from openstack_odooclient import RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: str
    """Description of the field."""
```

!!! note

    Make sure not to forget passing the name of the record manager class
    as the generic type argument for `RecordBase`.

    If this is not done there are no issues from a functional perspective,
    but type hinting for the `_manager` attribute will not work correctly
    when creating custom [record methods](#record-methods).

### Field Types

The following basic field types from Odoo are supported.

#### `bool`

Corresponds to the `Boolean` field type in Odoo.

```python
from __future__ import annotations

from openstack_odooclient import RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: bool
    """Description of the field."""
```

#### `int`

Corresponds to the `Integer` field type in Odoo.

```python
from __future__ import annotations

from openstack_odooclient import RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: int
    """Description of the field."""
```

#### `str`

Corresponds to the `Char` or `Text` field types in Odoo.

```python
from __future__ import annotations

from openstack_odooclient import RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: str
    """Description of the field."""
```

#### `float`

Corresponds to the `Float` field type in Odoo.

```python
from __future__ import annotations

from openstack_odooclient import RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: int
    """Description of the field."""
```

#### `date`

Corresponds to the `Date` field type in Odoo.

```python
from __future__ import annotations

from datetime import date

from openstack_odooclient import RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: date
    """Description of the field."""
```

#### `datetime`

Corresponds to the `DateTime` field type in Odoo.

```python
from __future__ import annotations

from datetime import datetime

from openstack_odooclient import RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: datetime
    """Description of the field."""
```

#### `Literal`

Corresponds to the `Selection` field type in Odoo.

Define all possible values for the field.

```python
from __future__ import annotations

from typing import Literal

from openstack_odooclient import RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: Literal["value1", "value2", "value3"]
    """Description of the field.

    Values:

    * ``value1`` - Value 1
    * ``value2`` - Value 2
    * ``value3`` - Value 3
    """
```

### Optional Fields

Any supported field type can be made optional. Two types of optional fields
are supported, depending on what Odoo returns when a field is not set.

#### `False`

The most common case is that `False` is returned, in which case
the type hint should be defined as shown below.

```python
from __future__ import annotations

from typing import Literal

from openstack_odooclient import RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: str | Literal[False]
    """Description of the field."""
```

#### `None`

If the default value is `None` when a field is not set,
the type hint should be defined as shown below instead.

```python
from __future__ import annotations

from openstack_odooclient import RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: str | None
    """Description of the field."""
```

### Field Aliases

Aliases to other fields can be defined by adding the `FieldAlias`
annotation to the field type hint. Aliases can be made for all supported
field types, including [model refs](#model-refs).

Field aliases are resolved internally to fetch the value for the target field.
They can also be used instead of the target field name when
[defining record search filters](index.md#search) and [creating new records](index.md#create).

While not required, it is **highly** recommended that the target field
also have a type hint defined for it on the model class.
The type of the alias **must** match the type of the target field.

```python
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import FieldAlias, RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: str
    """Description of the field."""

    field_alias: Annotated[str, FieldAlias("custom_field")]
    """Alias for ``custom_field``."""
```

### Model Refs

Records in Odoo can reference other records to establish relationships
between them, allowing for easier querying and management of multiple record types.

The Odoo Client library supports a higher level interface for managing these
relationships using the `ModelRef` type hint annotation.

The `ModelRef` annotation takes two arguments: the name of the model ref
field in Odoo, and the record class that implements the model in the Odoo Client library.

There are two types of model refs that can be expressed on record classes:
**singular records**, and **record lists**.

#### Singular Record (Many2one)

Singular record model refs correspond to the `Many2one` relationship type in Odoo.
With this relationship type, the model class references a single record.

Suppose that we want to add a model ref for a `user_id` field to our record class,
which references the `res.users` model
(which is implemented as the [`User`](user.md#record) record class).

There are three ways to reference fields of this type on the record class.
All of these should all be defined on your record class.

The first is to expose the record's ID directly as an integer.

```python
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import ModelRef, RecordBase, User

class CustomRecord(RecordBase["CustomRecordManager"]):
    user_id: Annotated[int, ModelRef("user_id", User)]
    """ID for the user that owns this record."""
```

The second is to expose the target record's display name as a string.

```python
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import ModelRef, RecordBase, User

class CustomRecord(RecordBase["CustomRecordManager"]):
    user_name: Annotated[str, ModelRef("user_id", User)]
    """Name of the user that owns this record."""
```

The third and final one is to define the target record itself as a record object.

```python
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import ModelRef, RecordBase, User

class CustomRecord(RecordBase["CustomRecordManager"]):
    user: Annotated[User, ModelRef("user_id", User)]
    """The user that owns this record.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """
```

The target record ID and display name are always available on the containing record object,
with no query required to retrieve their values.

For performance reasons, the target record as an object is not fetched automatically.
Instead, it is fetched from Odoo on demand when referenced for the first time (lazy loading).
The resulting record object is then cached to ensure the same object is returned every time.

The final result should be the following fields defined on your record class.

```python
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import ModelRef, RecordBase, User

class CustomRecord(RecordBase["CustomRecordManager"]):
    user_id: Annotated[int, ModelRef("user_id", User)]
    """ID for the user that owns this record."""

    user_name: Annotated[str, ModelRef("user_id", User)]
    """Name of the user that owns this record."""

    user: Annotated[User, ModelRef("user_id", User)]
    """The user that owns this record.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """
```

Similar to field aliases, any of these model ref fields can be used
instead of the target field name when [defining record search filters](index.md#search)
and [creating new records](index.md#create).
The record ID or the record object can be passed directly to those methods
(the record display name is not guaranteed to be unique, and thus, not accepted).

Record references can be made optional by unioning with `None`.
If the record reference is not set, `None` will be returned.

```python
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import ModelRef, RecordBase, User

class CustomRecord(RecordBase["CustomRecordManager"]):
    user_id: Annotated[int | None, ModelRef("user_id", User)]
    """ID for the user that owns this record."""

    user_name: Annotated[str | None, ModelRef("user_id", User)]
    """Name of the user that owns this record."""

    user: Annotated[User | None, ModelRef("user_id", User)]
    """The user that owns this record.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """
```

Recursive model refs are also supported using the `Self` type hint.
In the below example, `Self` resolves to `CustomRecord`.

```python
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import ModelRef, RecordBase
from typing_extensions import Self

class CustomRecord(RecordBase["CustomRecordManager"]):
    record_id: Annotated[int | None, ModelRef("user_id", Self)]
    """ID for the record related to this one, if set.."""

    record_name: Annotated[str | None, ModelRef("user_id", Self)]
    """Name of the record related to this one, if set."""

    record: Annotated[Self | None, ModelRef("user_id", Self)]
    """The record related to this one, if set.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """
```

#### Record Lists (One2many/Many2many)

Record list model refs correspond to the `One2many` and `Many2Many` relationship types in Odoo.
With these relationship types, the model class references multiple records in a list structure.

Suppose that we want to add a model ref for a `product_id` list field to our record class,
which references the `product.product` model
(which is implemented as the [`Product`](product.md#record) record class).

There are two ways to reference fields of this type on the record class.
All of these should all be defined on your record class.

The first is to expose the record IDs directly as a list of integers.

```python
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import ModelRef, RecordBase, Product

class CustomRecord(RecordBase["CustomRecordManager"]):
    product_ids: Annotated[list[int], ModelRef("product_id", Product)]
    """The list of IDs for the products to use."""
```

The second and final one is to expose the records as a list of record objects.

```python
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import ModelRef, RecordBase, Product

class CustomRecord(RecordBase["CustomRecordManager"]):
    products: Annotated[list[Product], ModelRef("product_id", Product)]
    """The list of products to use.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """
```

The target record IDs are always available on the containing record object,
with no query required to retrieve their values.

For performance reasons, the target record objects are not fetched automatically.
Instead, they fetched from Odoo on demand when referenced for the first time (lazy loading).
The resulting record objects are then cached to ensure the same objects are returned every time.

The final result should be the following fields defined on your record class.

```python
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import ModelRef, RecordBase, Product

class CustomRecord(RecordBase["CustomRecordManager"]):
    product_ids: Annotated[list[int], ModelRef("product_id", Product)]
    """The list of IDs for the products to use."""

    products: Annotated[list[Product], ModelRef("product_id", Product)]
    """The list of products to use.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """
```

Similar to field aliases, any of these model ref fields can be used
instead of the target field name when [defining record search filters](index.md#search)
and [creating new records](index.md#create).
The passed values (or lists of values) may consist of either record IDs, record objects,
or any combination of the two.

Recursive list model refs are also supported using the `Self` type hint.
In the below example, `Self` resolves to `CustomRecord`.

```python
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import ModelRef, RecordBase
from typing_extensions import Self

class CustomRecord(RecordBase["CustomRecordManager"]):
    child_ids: Annotated[list[int], ModelRef("child_id", Self)]
    """The list of IDs for the child records."""

    children: Annotated[list[Self], ModelRef("child_id", Self)]
    """The list of child records.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """
```

#### Circular Model Refs

Due to the way type hints are dereferenced by Python, two record classes
that reference each other are difficult (but not impossible) to support.

Generally the following must be done for circular model refs to work:

* Postponed evaluation of annotations is enabled using `from __future__ import annotations`
* Imports of the referenced model classes must be defined *after* the model classes
  are defined in each source file

Below is an example of two record classes that correctly reference each other.

```python title="parent.py"
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import ModelRef, RecordBase, RecordManagerBase

class Parent(RecordBase["ParentManager"]):
    child_ids: Annotated[list[int], ModelRef("child_id", Child)]
    """The list of IDs for the children records."""

    children: Annotated[list[Parent], ModelRef("child_id", Child)]
    """The list of children records.

    This fetches the full records from Odoo once,
    and caches them for subsequent accesses.
    """

class ParentManager(RecordManagerBase[Parent]):
    env_name = "custom.parent"
    record_class = Parent

from .child import Child  # noqa: E402
```

```python title="child.py"
from __future__ import annotations

from typing import Annotated

from openstack_odooclient import ModelRef, RecordBase, RecordManagerBase

class Child(RecordBase["ChildManager"]):
    parent_id: Annotated[int | None, ModelRef("parent_id", Parent)]
    """ID for the parent record, if it has one."""

    parent_name: Annotated[str | None, ModelRef("parent_id", Parent)]
    """Name of the parent record, if it has one."""

    parent: Annotated[Parent | None, ModelRef("parent_id", Parent)]
    """The parent record, if it has one.

    This fetches the full record from Odoo once,
    and caches it for subsequent accesses.
    """

class Child(RecordManagerBase[Child]):
    env_name = "custom.child"
    record_class = child

from .parent import Parent  # noqa: E402
```

### Odoo Version Compatibility

Major releases of Odoo may change the database models to introduce
new functionality.

The way models usually change in a backwards-incompatible way is
that fields are renamed so that they are referenced using another name,
without providing an alias for the old one.

In the OpenStack Odoo Client library, this is handled by defining
the `_field_mapping` attribute on the record class.

```python
_field_mapping: dict[str | None, dict[str, str]]
```

The `_field_mapping` attribute is a nested dictionary structure used
to define local-to-remote field name mappings.

```python
from __future__ import annotations

from openstack_odooclient import RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: str
    """Description of the field."""

    custom_field_2: int
    """Description of the second field."""

    custom_field_3: float
    """Description of the third field."""

    _field_mapping = {
        # The Odoo version for which to generate the mapping.
        "13.0": {
            # Key is local field name. Value is the field name in Odoo 13.
            "custom_field": "old_custom_field",
        }
        # Use None to provide a mapping to use for all Odoo versions.
        None: {
            "custom_field_2": "old_custom_field_2",
        },
        # custom_field_3 is not defined here.
        # The field name will be used as-is on all Odoo versions.
    }
```

Mappings can be added for specific Odoo versions, or by using `None`,
mappings that apply to all Odoo versions can be defined.

When the Odoo Client library interfaces with Odoo, it will automatically find
and use the correct field name to present based on the server version
and the record class's field mapping.

### Record Methods

Methods can be defined on record types to provide additional functionality.

```python
from __future__ import annotations

from openstack_odooclient import RecordBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: str
    """Description of the field."""

    def custom_field_is_defined(self) -> bool:
        return bool(self.custom_field)
```

In addition to all of the Odoo fields defined on the record class,
the following internal attributes are also available for use in object methods:

* `_client` ([`Client`](../index.md#connecting-to-odoo)) - The Odoo client object the record was created from
* `_manager` (`RecordManager`) - The manager object the record was created from (correctly type hinted so methods can be called)
* `_records` (`MappingProxyType[str, Any]`) - The raw record fields from OdooRPC
* `_fields` (`tuple[str, ...] | None`) - The fields that were selected during the query (or `None` for all fields)
* `_odoo` (`odoorpc.ODOO`) - The OdooRPC connection object
* `_env` (`odoorpc.env.Environment`) - The OdooRPC environment object for the model

!!! note

    It is recommended to follow these guidelines when defining custom
    record methods:

    * Record objects are intended to be immutable. Custom methods should not
      change the internal state, or the fields, of the record object.
    * If you are releasing your custom record types in a publicly available
      library, **do not** rely on custom manager methods through the `_manager`
      attribute. If a depending package subclasses your custom record types,
      **the manager for that record subclass will not have your custom manager
      methods defined on it.**

## Managers

**Manager classes** are used to provide query methods and other functionality
necessary for managing record objects in the Odoo Client library.

Once you have defined your record class, a manager class must be created
for implementing the query methods for the record class.

### Creating a Manager Class

Manager classes are subclasses of the generic `RecordManagerBase` class,
specifying the record class as the generic type argument,
and defining the following class attributes:

* `env_name` (`str`) - The name of the Odoo environment (database model) for the record class
* `record_class` (`Type[Record]`) - The record class to use to create record objects (**must** be the same class as the one specified in the generic subclass definition)

The following optional class attributes are also available:

* `default_fields` (`tuple[str, ...] | None`) - A set of fields to select by default in queries
  if a field list is not supplied (default is `None` to select all fields)

Below is a simple example of a custom record type and its manager class.

```python
from __future__ import annotations

from openstack_odooclient import RecordBase, RecordManagerBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: str
    """Description of the field."""

class CustomRecordManager(RecordManagerBase[CustomRecord]):
    env_name = "custom.record"
    record_class = CustomRecord
```

### Using a Manager Class

There are two ways of using manager classes. The first is to simply
create a manager object, passing the [`Client`](../index.md#connecting-to-odoo)
object as the sole argument.

This will allow manager methods to be used by calling them on the manager object.

```python
from __future__ import annotations

from openstack_odooclient import Client, RecordBase, RecordManagerBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: str
    """Description of the field."""

class CustomRecordManager(RecordManagerBase[CustomRecord]):
    env_name = "custom.record"
    record_class = CustomRecord

odoo_client = Client(...)
custom_records = CustomRecordManager(odoo_client)
```

This will work perfectly fine, but the disadvantage of using this method is
that the client and manager objects are managed as two separate variables.

To create a single object from which you can manage **all** of your custom
types and managers, subclass the `Client` class, and add a type hint for your
custom manager class.

```python
from __future__ import annotations

from openstack_odooclient import RecordBase, RecordManagerBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: str
    """Description of the field."""

class CustomRecordManager(RecordManagerBase[CustomRecord]):
    env_name = "custom.record"
    record_class = CustomRecord

class CustomClient(Client):
    custom_records: CustomRecordManager
```

This adds the record manager to the client class, allowing you to
reference it on client objects created from it.

```python
>>> odoo_client = CustomClient(...)
>>> odoo_client.custom_records.get(1234)
CustomRecord(record={'id' 1234, 'custom_record': 'Hello, world!'}, fields=None)
```

### Manager Methods

Methods can be defined on manager classes to provide additional functionality.

```python
from __future__ import annotations

from openstack_odooclient import RecordBase, RecordManagerBase

class CustomRecord(RecordBase["CustomRecordManager"]):
    custom_field: str
    """Description of the field."""

class CustomRecordManager(RecordManagerBase[CustomRecord]):
    env_name = "custom.record"
    record_class = CustomRecord

    def search_by_custom_field(self, custom_field: str) -> list[Record]:
        return self.search([("custom_field", "ilike", custom_field)])

    def perform_action(self, custom_record: int | CustomRecord) -> None:
        self._env.perform_action(
            (
                custom_record.id
                if isinstance(custom_record, CustomRecord)
                else custom_record
            ),
        )
```

The following internal attributes are also available for use in methods:

* `env_name` (`str`) - The name of the Odoo environment (database model) for the record class
* `record_class` (`Type[Record]`) - The record class object
* `default_fields` (`tuple[str, ...] | None`) - The default list of fields to fetch on queries (or `None` to fetch all)
* `_client` ([`Client`](../index.md#connecting-to-odoo)) - The Odoo client object the record manager uses
* `_odoo` (`odoorpc.ODOO`) - The OdooRPC connection object
* `_env` (`odoorpc.env.Environment`) - The OdooRPC environment object for the model

## Mixins

Python supports [multiple inheritance](https://docs.python.org/3/tutorial/classes.html#multiple-inheritance)
when creating new classes. A common use case for multiple inheritance is to extend
functionality of a class through the use of *mixin classes*, which are minimal
classes that only consist of supplementary attributes and methods, that get added
to other classes through subclassing.

The OpenStack Odoo Client library for Python supports the use of mixin classes
to add functionality to custom record and manager classes in a modular way.
Multiple mixins can be added to record and manager classes to allow mixing and
matching additional functionality as required.

### Using Mixins

To extend the functionality of your custom record and manager classes,
append the mixins for the record class and/or record manager class
**AFTER** the inheritance for `RecordBase` and `RecordManagerBase`.
You also need to specify the **same** type arguments to the mixins as
is already being done for `RecordBase` and `RecordManagerBase`.

```python
from __future__ import annotations

from openstack_odooclient import (
    NamedRecordManagerMixin,
    NamedRecordMixin,
    RecordBase,
    RecordManagerBase,
)

class CustomRecord(
    RecordBase["CustomRecordManager"],
    NamedRecordMixin["CustomRecordManager"],
):
    custom_field: str
    """Description of the field."""

class CustomRecordManager(
    RecordManagerBase[CustomRecord],
    NamedRecordManagerMixin[CustomRecord],
):
    env_name = "custom.record"
    record_class = CustomRecord
```

That's all that needs to be done. The additional attributes and/or methods
should now be available on your record and manager objects.

The following mixins are provided with the Odoo Client library.

#### Named Records

If your record model has a unique `name` field on it (of `str` type),
you can use the `NamedRecordMixin` and `NamedRecordManagerMixin` mixins
to define the `name` field on the record class, and add the
`get_by_name` method to your custom record manager class.

```python
from __future__ import annotations

from openstack_odooclient import (
    NamedRecordManagerMixin,
    NamedRecordMixin,
    RecordBase,
    RecordManagerBase,
)

class CustomRecord(
    RecordBase["CustomRecordManager"],
    NamedRecordMixin["CustomRecordManager"],
):
    custom_field: str
    """Description of the field."""

    # Added by NamedRecordMixin:
    #
    # name: str
    # """The unique name of the record."""

class CustomRecordManager(
    RecordManagerBase[CustomRecord],
    NamedRecordManagerMixin[CustomRecord],
):
    env_name = "custom.record"
    record_class = CustomRecord

    # Added by NamedRecordManagerMixin:
    #
    # def get_by_name(...):
    #     ...
```

For more information on using record managers with unique `name` fields,
see [Named Record Managers](index.md#named-record-managers).

#### Coded Records

If your record model has a unique `code` field on it (of `str` type),
you can use the `CodedRecordMixin` and `CodedRecordManagerMixin` mixins
to define the `code` field on the record class, and add the
`get_by_code` method to your custom record manager class.

```python
from __future__ import annotations

from openstack_odooclient import (
    CodedRecordManagerMixin,
    CodedRecordMixin,
    RecordBase,
    RecordManagerBase,
)

class CustomRecord(
    RecordBase["CustomRecordManager"],
    CodedRecordMixin["CustomRecordManager"],
):
    custom_field: str
    """Description of the field."""

    # Added by CodedRecordMixin:
    #
    # code: str
    # """The unique name for this record."""

class CustomRecordManager(
    RecordManagerBase[CustomRecord],
    CodedRecordManagerMixin[CustomRecord],
):
    env_name = "custom.record"
    record_class = CustomRecord

    # Added by CodedRecordManagerMixin:
    #
    # def get_by_code(...):
    #     ...
```

For more information on using record managers with unique `code` fields,
see [Coded Record Managers](index.md#coded-record-managers).

#### Records with Attachments

If your record can have [attachments](attachment.md) associated with it,
you can use the `RecordWithAttachmentMixin` mixin to define the associated
fields used to reference the attachment record.

```python
from __future__ import annotations

from openstack_odooclient import (
    RecordBase,
    RecordManagerBase,
    RecordWithAttachmentMixin,
)

class CustomRecord(
    RecordBase["CustomRecordManager"],
    RecordWithAttachmentMixin["CustomRecordManager"],
):
    custom_field: str
    """Description of the field."""

    # Added by RecordWithAttachmentMixin:
    #
    # message_main_attachment_id: Annotated[
    #     int | None,
    #     ModelRef("message_main_attachment_id", Attachment),
    # ]
    # """The ID of the main attachment on the record, if there is one."""
    #
    # message_main_attachment_name: Annotated[
    #     str | None,
    #     ModelRef("message_main_attachment_name", Attachment),
    # ]
    # """The name of the main attachment on the record, if there is one."""
    #
    # message_main_attachment: Annotated[
    #     Attachment | None,
    #     ModelRef("message_main_attachment", Attachment),
    # ]
    # """The main attachment on the record, if there is one.
    #
    # This fetches the full record from Odoo once,
    # and caches it for subsequent accesses.
    # """

class CustomRecordManager(RecordManagerBase[CustomRecord]):
    env_name = "custom.record"
    record_class = CustomRecord
```

For more information on using attachments,
see [Records with Attachments](index.md#records-with-attachments).

### Creating Mixins

It is possible to create your own custom mixins to incorporate into
custom record and manager classes.

There are two mixin types: **record mixins** and **record manager mixins**.

#### Record Mixins

Record mixins are used to add custom fields and methods to record classes.

Here is the full implementation of `NamedRecordMixin` as an example
of a mixin for a record class, that simply adds the `name` field:

```python
from __future__ import annotations

from typing import Generic

from openstack_odooclient import RM, RecordProtocol

class NamedRecordMixin(RecordProtocol[RM], Generic[RM]):
    name: str
    """The unique name of the record."""
```

A record mixin consists of a class that subclasses `RecordProtocol[RM]`
(where `RM` is the type variable for a record manager class) to get the type
hints for a record class' common fields and methods. `Generic[RM]` is also
subclassed to make the mixin itself a generic class, to allow `RM` to be
passed when creating a record class with the mixin.

Once you have the class, simply define any fields and methods you'd like
to add.

You can then use the mixin as shown in [Using Mixins](#using-mixins).

When defining custom methods, in addition to accessing fields/methods
defined within the mixin, fields/methods from the `RecordBase` class
are also available:

```python
from __future__ import annotations

from typing import Generic

from openstack_odooclient import RM, RecordProtocol

class NamedRecordMixin(RecordProtocol[RM], Generic[RM]):
    name: str
    """The unique name of the record."""

    def custom_method(self) -> None:
        self.name  # str
        self._env.custom_method(self.id)
```

#### Record Manager Mixins

Record manager mixins are expected to be mainly used to add custom methods
to a record manager class.

```python
from __future__ import annotations

from typing import Generic

from openstack_odooclient import R, RecordManagerProtocol

class NamedRecordManagerMixin(RecordManagerProtocol[R], Generic[R]):
    def custom_method(self, record: int | R) -> None:
        self._env.custom_method(  # self._env available from RecordManagerBase
            record if isinstance(record, int) else record.id,
        )
```

A record manager mixin consists of a class that subclasses
`RecordManagerProtocol[R]` (where `R` is the type variable for a record class)
to get the type hints for a record manager class' common attributes and
methods. `Generic[R]` is also subclassed to make the mixin itself a generic
class, to allow `R` to be passed when creating a record manager class
with the mixin.

## Extending Existing Record Types

The Odoo Client library provides *limited* support for extending the built-in record types.

It is possible to subclass built-in record types, and create custom record managers
that manage this record class.

```python
from __future__ import annotations

from openstack_odooclient import Client, RecordManagerBase, User, UserManager

class CustomUser(User):
    custom_field: str
    """Description of the field."""

class CustomUserManager(RecordManagerBase[CustomUser]):
    env_name = UserManager.env_name
    record_class = CustomUser

class CustomClient(Client):
    custom_users: CustomUserManager
```

Due to the Odoo Client library using type hints to determine what record classes to use,
and the type hints being physically defined in code to allow type analysis tools such as Mypy
and Pyright to properly evaluate the source, *existing* references on *existing* record classes
cannot be automatically updated to use the custom versions.

However, it is possible to **cast** a record object of the base type into the custom type
using the record class's `from_record_obj` class method.

```python
>>> odoo_client = CustomClient(...)
>>> user = odoo_client.users.get(1234)
>>> user
User(record={'id': 1234, 'custom_field': 'Hello, world!', ...}, fields=None)
>>> custom_user = CustomUser.from_record_obj(user)
>>> custom_user
CustomUser(record={'id': 1234, 'custom_field': 'Hello, world!', ...}, fields=None)
>>> custom_user.custom_field
'Hello, world!'
```

This should cover the majority of use cases where custom add-ons add new functionality
to existing models.
