"""Module defining JIRA X-Ray utilities"""

import logging
import os
import shutil
import subprocess
from pathlib import Path

import geckodriver_autoinstaller
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def firefox_browser() -> tuple[FirefoxProfile, webdriver.Firefox, str]:
    """Create a Firefox browser"""

    # Create non-hidden directory in $HOME to be accessible by snap package and native processes
    # https://firefox-source-docs.mozilla.org/testing/geckodriver/Usage.html#running-firefox-in-a-container-based-package
    # https://firefox-source-docs.mozilla.org/testing/geckodriver/Profiles.html#default-locations-for-temporary-profiles
    os.environ["TMPDIR"] = os.environ["HOME"] + "/snap/firefox/common/tmp"
    Path(os.environ["TMPDIR"]).mkdir(parents=True, exist_ok=True)

    # Install gecko driver if it's missing
    if shutil.which("geckodriver") is None and not os.path.exists(
        geckodriver_autoinstaller.utils.get_geckodriver_path(),
    ):
        print(":: Gecko driver not foud, installing...")
        geckodriver_autoinstaller.install()
    else:
        print(":: Gecko driver already present, skipping installation.")

    geckodriver_path = (
        shutil.which("geckodriver")
        or geckodriver_autoinstaller.utils.get_geckodriver_path()
    )

    # Create download directory
    download_dir = os.environ["TMPDIR"] + "/downloads"
    Path(download_dir).mkdir(parents=True, exist_ok=True)

    # Create Firefox options
    options = Options()
    options.add_argument("-headless")
    options.enable_downloads = True
    options.log.level = (
        "fatal"  # WARNING enabling logs in debug/trace will reveal secrets
    )
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.manager.closeWhenDone", True)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/octet-stream, application/x-gzip, application/zip",
    )

    # Create Firefox profile with JavaScript enabled
    firefox_profile = FirefoxProfile()
    firefox_profile.set_preference("javascript.enabled", True)
    options.profile = firefox_profile

    # Start browser and navigate to page
    print(f":: Starting Firefox with geckodriver at {geckodriver_path}")
    browser = webdriver.Firefox(
        options,
        Service(
            executable_path=geckodriver_path,
            log_output=subprocess.STDOUT,
        ),
    )  # DEVNULL if needed
    return firefox_profile, browser, download_dir


def login_to_jira(browser: webdriver.Firefox, jira_url: str, login: str, password: str):
    """Login to Jira/Xray using the provided credentials"""
    success = False
    for _ in range(5):
        try:
            print(":: Connecting to JIRA/XRay")
            browser.get(jira_url)

            # Insert cookie to avoid alert message later
            browser.add_cookie({"name": "CtxsClientDetectionDone", "value": "true"})

            # NetScaler Gateway Login Page
            print(":: Waiting for NetScaler Gateway Login Page")
            WebDriverWait(browser, 30).until(
                EC.element_to_be_clickable((By.ID, "login")),
            )
            success = True
            break
        except (TimeoutException, WebDriverException) as e:
            logging.error(e)
    if not success:
        raise OSError("Failed to connect to JIRA/XRay")
    browser.find_element(By.ID, "login").send_keys(login)
    browser.find_element(By.ID, "passwd").send_keys(password)
    browser.find_element(By.ID, "nsg-x1-logon-button").click()

    # Terms of use => OK
    print(":: Waiting for Terms of Use")
    WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, "loginBtn")))
    browser.find_element(By.ID, "loginBtn").click()

    # JIRA login form
    print(":: Waiting for JIRA login form")
    WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.ID, "login-form-username")),
    )
    browser.find_element(By.ID, "login-form-username").send_keys(login)
    browser.find_element(By.ID, "login-form-password").send_keys(password)
    browser.find_element(By.ID, "login").click()

    print(":: Waiting for JIRA login success")
    WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, "create_link")))


def get_cookies(browser: webdriver.Firefox):
    """Return the browser cookies"""
    cookies_dict = {}
    for cookie in browser.get_cookies():
        cookies_dict[cookie["name"]] = cookie["value"]
    return cookies_dict
