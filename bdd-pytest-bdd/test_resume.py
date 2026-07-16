import os
import time

from pytest_bdd import parsers, scenarios, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

scenarios("features/resume.feature")


def _wait_visible(driver, selector, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
    )


def _wait_clickable(driver, selector, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )


def _wait_for_download(directory, timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        files = [f for f in os.listdir(directory) if not f.endswith(".crdownload")]
        if files:
            return os.path.join(directory, files[0])
        time.sleep(0.2)
    raise TimeoutError(f"No completed download appeared in {directory} within {timeout}s")


@when("I open the resume list")
def open_resume_list(driver, base_url):
    driver.get(f"{base_url}/index.html")


@then(parsers.parse('I should see a link for "{slug}"'))
def see_link_for(driver, slug):
    link = _wait_visible(driver, f'[data-testid="resume-link-{slug}"]')
    assert link.is_displayed()


@when(parsers.parse('I open the resume detail page for "{slug}"'))
def open_resume_detail(driver, base_url, slug):
    driver.get(f"{base_url}/resume.html?slug={slug}")


@then(parsers.parse('I should see the name "{name}"'))
def see_name(driver, name):
    el = _wait_visible(driver, '[data-testid="resume-name"]')
    assert el.text == name


@then("I should see a not-found message")
def see_not_found(driver):
    el = _wait_visible(driver, '[data-testid="resume-name"]')
    assert el.text == "Resume not found"


@when(parsers.parse('I download the PDF for "{slug}"'))
def download_pdf(driver, base_url, slug):
    driver.get(f"{base_url}/resume.html?slug={slug}")
    _wait_clickable(driver, '[data-testid="download-pdf"]').click()


@then("the downloaded file should be a valid PDF")
def assert_valid_pdf(download_dir):
    path = _wait_for_download(download_dir)
    with open(path, "rb") as f:
        assert f.read(4) == b"%PDF"


@when(parsers.parse('I download the DOCX for "{slug}"'))
def download_docx(driver, base_url, slug):
    driver.get(f"{base_url}/resume.html?slug={slug}")
    _wait_clickable(driver, '[data-testid="download-docx"]').click()


@then("the downloaded file should be a valid DOCX")
def assert_valid_docx(download_dir):
    path = _wait_for_download(download_dir)
    with open(path, "rb") as f:
        assert f.read(2) == b"PK"
