"""Module exporting JIRA X-Ray tickets as a zip archive of Cucumber features files"""

import os
import shutil
import subprocess
from pathlib import Path
import requests
import geckodriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

cfg = {}
cfg["user"] = os.environ["XRAY_USER"]
cfg["password"] = os.environ["XRAY_PASSWORD"]
cfg["jira_keys"] = os.environ["XRAY_KEYS"]
cfg["jira_url"] = os.environ["XRAY_BASE_URL"]

# Create non-hidden directory in $HOME to be accessible both by snap package and native processes
# https://firefox-source-docs.mozilla.org/testing/geckodriver/Usage.html#running-firefox-in-a-container-based-package
# https://firefox-source-docs.mozilla.org/testing/geckodriver/Profiles.html#default-locations-for-temporary-profiles
os.environ["TMPDIR"] = os.environ["HOME"] + "/snap/firefox/common/tmp"
Path(os.environ["TMPDIR"]).mkdir(parents=True, exist_ok=True)

# Install gecko driver if it's missing
print(":: Installing Gecko driver")
driver_path = geckodriver_autoinstaller.install()

# Create download directory
download_dir = os.environ["TMPDIR"] + "/downloads"
Path(download_dir).mkdir(parents=True, exist_ok=True)
download_file = download_dir + "/FeatureBundle.zip"
Path(download_file).unlink(missing_ok=True)

# Create Firefox options
options = Options()
options.add_argument("-headless")
options.enable_downloads = True
options.log.level = "fatal"  # WARNING enabling logs in debug/trace will reveal secrets
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.manager.closeWhenDone", True)
options.set_preference("browser.download.dir", download_dir)
options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                       "application/octet-stream, application/x-gzip, application/zip")

# Create Firefox profile with JavaScript enabled
firefox_profile = FirefoxProfile()
firefox_profile.set_preference("javascript.enabled", True)
options.profile = firefox_profile

# Start browser and navigate to page
print(":: Starting Firefox")
browser = webdriver.Firefox(options,
                            Service(executable_path=GeckoDriverManager().install(),
                                    log_output=subprocess.STDOUT))
try:
    print(":: Connecting to JIRA/XRay")
    browser.get(cfg["jira_url"])

    # Insert cookie to avoid alert message later
    browser.add_cookie({"name": "CtxsClientDetectionDone", "value": "true"})

    # NetScaler Gateway Login Page
    print(":: Waiting for NetScaler Gateway Login Page")
    WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.ID, "login")))
    browser.find_element(By.ID, "login").send_keys(cfg["user"])
    browser.find_element(By.ID, "passwd").send_keys(cfg["password"])
    browser.find_element(By.ID, "nsg-x1-logon-button").click()

    # Terms of use => OK
    print(":: Waiting for Terms of Use")
    WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, "loginBtn")))
    browser.find_element(By.ID, "loginBtn").click()

    # JIRA login form
    print(":: Waiting for JIRA login form")
    WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, "login-form-username")))
    browser.find_element(By.ID, "login-form-username").send_keys(cfg["user"])
    browser.find_element(By.ID, "login-form-password").send_keys(cfg["password"])
    browser.find_element(By.ID, "login").click()

    print(":: Waiting for JIRA login success")
    WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, "create_link")))

    # Export JIRA Cucumber feature files
    print(":: Exporting XRay Cucumber feature files")

    all_cookies = browser.get_cookies()
    cookies_dict = {}
    for cookie in all_cookies:
        cookies_dict[cookie['name']] = cookie['value']

    r = requests.get(cfg["jira_url"]+"/rest/raven/1.0/export/test?fz=true&keys="+cfg["jira_keys"],
                     cookies=cookies_dict, timeout=30)
    with open(download_dir+"/FeatureBundle.zip", 'wb') as file:
        file.write(r.content)

finally:
    print(":: Exiting")
    browser.quit()

    print(":: Cleaning")
    shutil.rmtree(firefox_profile.path)
