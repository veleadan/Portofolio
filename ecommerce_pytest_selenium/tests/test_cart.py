import pytest
import time
from selenium.webdriver.common.by import By
from config.chrome_driver import get_chrome_driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    driver = get_chrome_driver()
    yield driver
    driver.quit()


def test_add_to_cart(driver):

    wait = WebDriverWait(driver, 10)
    driver.get("https://www.gourmetto.ro/")

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sunt de acord"))).click()

    a = driver.find_element(By.ID, '_autocompleteSearchMainHeader')
    a.send_keys("vinuri")

    search_btn = driver.find_element(By.ID, "_doSearch")
    search_btn.click()

    add_btn = driver.find_element(By.LINK_TEXT, "Adauga in cos")
    add_btn.click()

    time.sleep(5)
    result = driver.find_element(By.CSS_SELECTOR, "span.q-cart")
    text_result = result.text

    assert text_result == '1', "Product was not added to the cart!"