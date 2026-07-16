import os

import pytest
import requests

BASE_URL = os.environ.get("RESUME_APP_URL", "http://localhost:8080")


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


@pytest.fixture(scope="session")
def known_slug():
    return "divya-kodukula"
