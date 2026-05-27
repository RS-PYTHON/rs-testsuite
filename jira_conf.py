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

"""Module retrieving JIRA configuration from environment"""

import os
import re
from urllib.parse import urlparse


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(
            f"Environment variable {name} is required and must not be empty",
        )
    return value


def _validate_jira_key(value: str) -> str:
    if not re.fullmatch(r"RSPY-[1-9]\d*", value):
        raise ValueError(
            f"Invalid INPUT_XRAY_KEY '{value}'. Expected format: RSPY-<positive integer>",
        )
    return value


def _validate_url(name: str, value: str) -> str:
    parsed = urlparse(value)
    if not (parsed.scheme and parsed.netloc):
        raise ValueError(f"Invalid URL in environment variable {name}: '{value}'")
    return value


# ---- Load & validate configuration ----


cfg = {}
cfg["user"] = _require_env("XRAY_USER")
cfg["password"] = _require_env("XRAY_PASSWORD")
cfg["jira_key"] = _validate_jira_key(_require_env("INPUT_XRAY_KEY"))
cfg["jira_url"] = _validate_url("XRAY_BASE_URL", _require_env("XRAY_BASE_URL"))
