import pytest
import time
from selenium.webdriver.common.by import By
from config.chrome_driver import get_chrome_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    """Setup and teardown for WebDriver."""
    driver = get_chrome_driver()
    yield driver
    driver.quit()


def test_checkout(driver):

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

    cart_btn = driver.find_element(By.CSS_SELECTOR, "i.fa.fa-shopping-bag")
    cart_btn.click()

    checkout_btn = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-cmd.full.fr.-g-order-checkout-button")
    checkout_btn.click()

    result = driver.find_element(By.ID, "doCheckout")
    final_result = result.get_attribute('textContent')

    assert "Trimite comanda" in final_result, "Checkout process did not reach the billing address step!"