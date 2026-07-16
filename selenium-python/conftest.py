import os
import shutil
import tempfile

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = os.environ.get("RESUME_APP_URL", "http://localhost:8080")
KNOWN_SLUG = "divya-kodukula"


@pytest.fixture(scope="session")
def base_url():
    try:
        requests.get(f"{BASE_URL}/api/health", timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.exit(
            f"Could not reach resume-app at {BASE_URL}. "
            "Start it first (see resume-app/scripts/start.sh) or set RESUME_APP_URL.",
            returncode=1,
        )
    return BASE_URL


@pytest.fixture
def known_slug():
    return KNOWN_SLUG


@pytest.fixture
def download_dir():
    d = tempfile.mkdtemp(prefix="selenium-downloads-")
    yield d
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture
def driver(download_dir):
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True,
        },
    )
    d = webdriver.Chrome(options=opts)
    yield d
    d.quit()
