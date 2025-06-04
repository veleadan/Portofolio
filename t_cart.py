import time

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--start-maximized")

driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service, options=options)

driver.get("https://www.gourmetto.ro/")
wait = WebDriverWait(driver, 10)

wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sunt de acord"))).click()

driver.find_element(By.XPATH, '//*[@id="_autocompleteSearchMainHeader"]').send_keys("vinuri")
driver.find_element(By.ID, '_doSearch').click()

wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Adauga in cos"))).click()

time.sleep(5)

result = driver.find_element(By.CSS_SELECTOR, "span.q-cart")
print(result.text)

input('enter..')
