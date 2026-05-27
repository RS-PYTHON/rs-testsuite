# Copyright 2023-2026 Airbus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json


def check_json_path_is_not_null(data: dict, item1: str, item2: str):
    """Checks that path item1.item2 is found in json data"""
    assert (
        data[item1][item2] is not None
    ), f"Path {item1}.{item2} can not be found on json {data}."


def is_valid_json(chain: str) -> bool:
    """Checks that json is valid"""
    result = json.loads(chain, strict=False)
    return isinstance(result, (dict, list))
