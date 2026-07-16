import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _wait_for_download(directory, timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        files = [f for f in os.listdir(directory) if not f.endswith(".crdownload")]
        if files:
            return os.path.join(directory, files[0])
        time.sleep(0.2)
    raise TimeoutError(f"No completed download appeared in {directory} within {timeout}s")


def test_pdf_download_button_produces_a_real_pdf(driver, base_url, known_slug, download_dir):
    # Headless Chrome blocks downloads by default; this CDP command is the
    # (undocumented-in-prefs) way to allow them -- see the stack's README.
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": download_dir}
    )
    driver.get(f"{base_url}/resume.html?slug={known_slug}")
    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="download-pdf"]'))
    )
    button.click()
    path = _wait_for_download(download_dir)
    with open(path, "rb") as f:
        assert f.read(4) == b"%PDF"


def test_docx_download_button_produces_a_real_docx(driver, base_url, known_slug, download_dir):
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": download_dir}
    )
    driver.get(f"{base_url}/resume.html?slug={known_slug}")
    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="download-docx"]'))
    )
    button.click()
    path = _wait_for_download(download_dir)
    with open(path, "rb") as f:
        assert f.read(2) == b"PK"  # docx is a zip container
