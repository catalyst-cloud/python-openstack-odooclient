# Copyright (C) 2025 Catalyst Cloud Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

FilterCriterion = tuple[str, str, Any] | Sequence[Any] | str
"""An individual criterion used for searching records in Odoo.

Query filters should be defined using the ORM API search domain
format. For more information on the ORM API search domain format:

https://www.odoo.com/documentation/14.0/developer/reference/addons/orm.html#search-domains

Filters are a sequence of criteria, where each criterion
is one of the following types of values:

* A 3-tuple or 3-element sequence in ``(field_name, operator, value)``
  format, where:

  * ``field_name`` (``str``) is the the name of the field to filter by.
  * ``operator`` (`str`) is the comparison operator to use (for more
    information on the available operators, check the ORM API
    search domain documentation).
  * ``value`` (`Any`) is the value to compare records against.

* A logical operator which prefixes the following filter criteria
  to form a **criteria combination**:

  * ``&`` is a logical AND. Records only match if **both** of the
    following **two** criteria match.
  * ``|`` is a logical OR. Records match if **either** of the
    following **two** criteria match.
  * ``!`` is a logical NOT (negation). Records match if the
    following **one** criterion does **NOT** match.

Every criteria combination is implicitly combined using a logical AND
to form the overall filter to use to query records.
"""
