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
