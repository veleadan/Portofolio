import pytest
from selenium.webdriver.common.by import By
from config.chrome_driver import get_chrome_driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    driver = get_chrome_driver()
    yield driver
    driver.quit()


def test_login_valid_credentials(driver):
    driver.get("https://www.gourmetto.ro/")
    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sunt de acord"))).click()
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='wrapper']/header/div[2]/div/div/div[3]/ul/li[2]/a/i"))).click()

    #make a valid account on the website above and write your credentials here:
    driver.find_element(By.ID, "_loginEmail").send_keys("your_email@example.com")#enter your account
    driver.find_element(By.ID, "_loginPassword").send_keys("your_password")#enter your password
    driver.find_element(By.ID, "doLogin").click()

    # if this variable has content, then the process is done
    info_account_display = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.account-info")))

    assert info_account_display is not None, "Login failed!"


def test_login_invalid_credentials(driver):

    driver.get("https://www.gourmetto.ro/")
    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sunt de acord"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='wrapper']/header/div[2]/div/div/div[3]/ul/li[2]/a/i"))).click()

    driver.find_element(By.ID, "_loginEmail").send_keys("invalid_user@example.com")
    driver.find_element(By.ID, "_loginPassword").send_keys("invalid_password")
    driver.find_element(By.ID, "doLogin").click()

#     # Assert error message
    error_message = driver.find_element(By.CSS_SELECTOR, ".errorMsg").text
    assert "Adresa de e-mail / parola introduse sunt incorecte. Te rugam sa incerci din nou." in error_message, "Expected error message not displayed!"