"""Module exporting JIRA X-Ray tickets as a zip archive of Cucumber features files"""

import os
import shutil
from pathlib import Path
import requests
from jira_utils import firefox_browser, login_to_jira, get_cookies

cfg = {}
cfg["user"] = os.environ["XRAY_USER"]
cfg["password"] = os.environ["XRAY_PASSWORD"]
cfg["jira_key"] = os.environ["XRAY_KEY"]
cfg["jira_url"] = os.environ["XRAY_BASE_URL"]

# Create Firefox browser and download directory
firefox_profile, browser, download_dir = firefox_browser()

download_file = download_dir + "/FeatureBundle.zip"
Path(download_file).unlink(missing_ok=True)

try:
    # Login to Jira/XRay
    login_to_jira(browser, cfg["jira_url"], cfg["user"], cfg["password"])

    # Export JIRA Cucumber feature files
    print(":: Exporting XRay Cucumber feature files")

    r = requests.get(cfg["jira_url"]+"rest/raven/1.0/export/test?fz=true&keys="+cfg["jira_key"],
                     cookies=get_cookies(browser), timeout=30)
    with open(download_dir+"/FeatureBundle.zip", 'wb') as file:
        file.write(r.content)

finally:
    print(":: Exiting")
    browser.quit()

    print(":: Cleaning")
    shutil.rmtree(firefox_profile.path)
