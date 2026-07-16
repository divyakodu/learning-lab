from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_detail_page_shows_name_headline_summary(driver, base_url, known_slug):
    driver.get(f"{base_url}/resume.html?slug={known_slug}")
    name = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="resume-name"]'))
    )
    assert name.text == "Divya Kodukula"
    headline = driver.find_element(By.CSS_SELECTOR, '[data-testid="resume-headline"]')
    assert headline.text != ""
    summary_items = driver.find_elements(By.CSS_SELECTOR, '[data-testid="resume-summary"] li')
    assert len(summary_items) > 0


def test_back_link_returns_to_list(driver, base_url, known_slug):
    driver.get(f"{base_url}/resume.html?slug={known_slug}")
    back = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="back-link"]'))
    )
    back.click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="resume-list"]'))
    )


def test_unknown_slug_shows_not_found(driver, base_url):
    driver.get(f"{base_url}/resume.html?slug=does-not-exist")
    name = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="resume-name"]'))
    )
    assert name.text == "Resume not found"
