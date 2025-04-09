from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def initialize_driver(pg):
    options = Options()
    options.headless = False

    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service, options=options)
    page_url = pg

    driver.get(page_url)
    wait = WebDriverWait(driver, 10)

    cookie_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.action-buttons-container"))).click()
    x_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.fancybox-content button[type="button"][class="fancybox-button fancybox-close-small"] '))).click()
    maga_btn = (wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.x-product-box-warehouse-search")))).click()

    driver.implicitly_wait(10)

    stock_list = []
    stock_status = driver.find_elements(By.CSS_SELECTOR, "div.availability-info")
    for stock in stock_status:
        stock_list.append(stock.get_attribute("textContent"))


    li_addresses = driver.find_elements(By.CSS_SELECTOR, "div.address")
    address_list = []
    for address in li_addresses:
       address_list.append(address.get_attribute("textContent"))


    def trim_and_associate(adr_list, stk):
        results = []

        for i,adr in enumerate(adr_list):
            normalized_txt = adr.strip().splitlines()

            filtered_lines = [line.strip() for line in normalized_txt if line.strip()]

            extracted_city = None
            for line in filtered_lines:
                if "bucharest" in line.lower() or "bucuresti" in line.lower():
                    extracted_city = line.strip()  # Take the full city-region detail
                    break  # Stop after finding the first relevant line

            if extracted_city:  # Check if we found a city match
                # Append a dictionary with address, city, stock, and status
                results.append({
                    "address": " | ".join(filtered_lines),  # Combine multiple filtered lines
                    "stock": stk[i].strip(),
                })

        return results

    data = trim_and_associate(address_list,stock_list)

    return data


