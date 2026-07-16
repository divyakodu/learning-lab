import os
import shutil
import tempfile

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

BASE_URL = os.environ.get("RESUME_APP_URL", "http://localhost:8080")


def before_all(context):
    context.base_url = BASE_URL
    try:
        requests.get(f"{BASE_URL}/api/health", timeout=5)
    except requests.exceptions.ConnectionError:
        raise SystemExit(
            f"Could not reach resume-app at {BASE_URL}. "
            "Start it first (see resume-app/scripts/start.sh) or set RESUME_APP_URL."
        )


def before_scenario(context, scenario):
    context.download_dir = tempfile.mkdtemp(prefix="bdd-behave-downloads-")
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_experimental_option(
        "prefs",
        {"download.default_directory": context.download_dir, "download.prompt_for_download": False},
    )
    # See learning-lab/selenium-python/conftest.py: Selenium Manager has no
    # linux/aarch64 build, so fall back to apt's chromium + chromium-driver
    # there (e.g. this project's Jenkins container).
    chromium_bin = shutil.which("chromium") or shutil.which("chromium-browser")
    chromedriver_bin = shutil.which("chromedriver")
    if chromium_bin and chromedriver_bin:
        opts.binary_location = chromium_bin
        context.driver = webdriver.Chrome(service=Service(executable_path=chromedriver_bin), options=opts)
    else:
        context.driver = webdriver.Chrome(options=opts)
    context.driver.execute_cdp_cmd(
        "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": context.download_dir}
    )


def after_scenario(context, scenario):
    context.driver.quit()
    shutil.rmtree(context.download_dir, ignore_errors=True)
