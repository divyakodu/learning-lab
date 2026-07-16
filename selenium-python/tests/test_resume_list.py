from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_resume_list_shows_known_resume(driver, base_url, known_slug):
    driver.get(f"{base_url}/index.html")
    link = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="resume-link-{known_slug}"]'))
    )
    assert link.is_displayed()


def test_clicking_resume_link_navigates_to_detail(driver, base_url, known_slug):
    driver.get(f"{base_url}/index.html")
    link = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="resume-link-{known_slug}"]'))
    )
    link.click()
    WebDriverWait(driver, 5).until(EC.url_contains(f"slug={known_slug}"))
    name = driver.find_element(By.CSS_SELECTOR, '[data-testid="resume-name"]')
    assert name.text == "Divya Kodukula"
