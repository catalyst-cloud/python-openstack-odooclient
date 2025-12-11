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


def test_import():
    """Test that the openstack_odooclient package can be imported.

    Believe it or not, this is an actual test of things.
    The ``openstack_odooclient`` package has circular imports
    in many places, to add type annotations for classes that
    reference each other that must be available at runtime
    so the library can parse the annotations.

    Importing the package as an individual test is a sanity check
    to make sure that mistakes made in the dependency chain
    do not result in the package being unable to be imported.
    """

    import openstack_odooclient  # noqa: F401, PLC0415
