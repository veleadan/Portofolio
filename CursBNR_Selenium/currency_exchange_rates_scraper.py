import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver with visible configuration
options = Options()
options.headless = False

driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service, options=options)

def trim_text(text, key_word):
    # Find the position of the key word
    start_index = text.find(key_word)

    # Extract everything from the keyword onward
    result_text = text[start_index:] if start_index != -1 else text
    return result_text  # Handle case if keyword not found

def parse_currency_data(text):

    data_text = trim_text(text,'EUR')
    #Trim text till this key word
    # Regular expression to match currency codes and their associated data
    pattern = r"(?P<currency>[A-Z]{3})\s+(?P<name>[^\d]+)\s+(?P<rates>(?:[+-]?\d*\.\d+\s+)+)"

    # Extract matches based on the pattern
    matches = re.finditer(pattern, data_text, re.MULTILINE)

    # Prepare a data container (dictionary)
    currency_data = []
    for match in matches:
        currency = match.group("currency") # The code (e.g., "EUR")
        name = match.group("name").strip()# Full name (e.g., "Euro")
        rates_list = match.group("rates").split()  # Extract rates/changes as a list

        n = replace_romanian_characters(name)
        currency_data.append([currency, n] + rates_list)

    return currency_data

def save_to_csv(data, filename,dates):

    date_pattern = r"\b(\d{1,2})\s([A-Za-zăîșțâĂÎȘȚÂ]+)\.\s(\d{4})\b"
    # Find all dates in the text
    calendar = re.findall(date_pattern, dates)
    result = [(f"{day}.{month}.{year}") for day, month, year in calendar]
    # # Specify headers based on the structure of the data
    headers = ["Cod valuta", "Nume valuta", result[0], "Change 1", result[1], "Change 2", result[2], "Change 3"]

    # # Write to a CSV file
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers[:len(data[0])])  # Adjust headers dynamically
        writer.writerows(data)

def replace_romanian_characters(text):
    # Define a dictionary mapping Romanian characters to replacements
    replacements = {
        "ă": "a",
        "ș": "s",
        "ț": "t",
        "ţ": "t",
        "î": "i",
        "â": "a",
        "Ț": "T",
        "Ș": "S",
        "Ă": "A",
        "Î": "I",
        "Â": "A",
    }

    # Replace the Romanian characters in the text
    for romanian_char, replacement_char in replacements.items():
        text = text.replace(romanian_char, replacement_char)

    return text

### Main ###

url = "https://www.cursbnr.ro/"

try:
    # Open the page
    driver.get(url)
    table_xpath = "//table[@id='table-currencies']"

    # Wait for the table to load
    wait = WebDriverWait(driver, 10)
    currency_table = driver.find_elements(By.TAG_NAME, "td")
    date_var = driver.find_elements(By.TAG_NAME, 'th')

    info = ''
    dates_info = ''

    for elem in currency_table:
        info += elem.get_attribute('textContent')+'\n'
    for date in date_var:
        dates_info += date.get_attribute('textContent')+'\n'

    output = parse_currency_data(info)
    save_to_csv(output, "output.csv",dates=dates_info)


finally:
    # Close the browser
    driver.quit()