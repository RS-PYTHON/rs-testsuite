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

"""Module exporting JIRA X-Ray tickets as a zip archive of Cucumber features files"""

import shutil
from pathlib import Path

import requests

from jira_conf import cfg
from jira_utils import firefox_browser, get_cookies, login_to_jira

# Create Firefox browser and download directory
firefox_profile, browser, download_dir = firefox_browser()

download_file = download_dir + "/FeatureBundle.zip"
Path(download_file).unlink(missing_ok=True)

try:
    # Login to Jira/XRay
    login_to_jira(browser, cfg["jira_url"], cfg["user"], cfg["password"])

    # Export JIRA Cucumber feature files
    url = cfg["jira_url"] + "rest/raven/1.0/export/test?fz=true&keys=" + cfg["jira_key"]
    print(":: Exporting XRay Cucumber feature files from " + url)
    r = requests.get(url, cookies=get_cookies(browser), timeout=30)
    r.raise_for_status()
    with open(download_dir + "/FeatureBundle.zip", "wb") as file:
        file.write(r.content)

finally:
    print(":: Exiting")
    browser.quit()

    print(":: Cleaning")
    shutil.rmtree(firefox_profile.path)
