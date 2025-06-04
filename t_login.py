import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.headless = False

driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service, options=options)

driver.get("https://www.gourmetto.ro/")
wait = WebDriverWait(driver, 10)

wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sunt de acord"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='wrapper']/header/div[2]/div/div/div[3]/ul/li[2]/a/i"))).click()

driver.find_element(By.ID, "_loginEmail").send_keys("velea.radu.dan@gmail.com")
driver.find_element(By.ID, "_loginPassword").send_keys("Samurai1802")
driver.find_element(By.ID, "doLogin").click()


time.sleep(5)
