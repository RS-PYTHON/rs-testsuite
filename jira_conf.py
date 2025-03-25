"""Module retrieving JIRA configuration from environment"""

import os

cfg = {}
cfg["user"] = os.environ["XRAY_USER"]
cfg["password"] = os.environ["XRAY_PASSWORD"]
cfg["jira_key"] = os.environ["INPUT_XRAY_KEY"]
cfg["jira_url"] = os.environ["XRAY_BASE_URL"]
