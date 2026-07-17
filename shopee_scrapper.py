from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

# List of Shopee URLs
urls = [
    "https://shopee.ph/-BUNDLE-Epson-WF-M5899-Printer-with-Inkrite-Chipless-Refillable-Cartridge-Dye-Ink-and-Act-Key-i.33348590.41350964641?sp_atk=54987bb2-ff0b-4435-934f-e38a7c573b70&xptdk=54987bb2-ff0b-4435-934f-e38a7c573b70",
    # Add more URLs here
]

# Set up ChromeDriver
service = Service("C:/ProgramData/chocolatey/bin/chromedriver.exe")  # Replace with your actual path
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background
driver = webdriver.Chrome(service=service, options=options)

# Store results
results = []

for url in urls:
    driver.get(url)
    time.sleep(3)  # Give time for dynamic content to load
    try:
        # Try multiple selectors for title
        try:
            title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div._44qnta span"))
            ).text
        except:
            try:
                title = driver.find_element(By.CSS_SELECTOR, "div._44qnta").text
            except:
                title = "Not found"

        # Try multiple selectors for price
        try:
            price = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.pmmxKx span"))
            ).text
        except:
            try:
                price = driver.find_element(By.CSS_SELECTOR, "div.pmmxKx").text
            except:
                price = "Not found"

    except Exception as e:
        title = "Error"
        price = "Not found"

    results.append({"URL": url, "Item Name": title, "Price": price})

driver.quit()

# Save to Excel
output_file = "Shopee_Items.xlsx"
if os.path.exists(output_file):
    try:
        os.rename(output_file, output_file)
    except OSError:
        print(f"Please close '{output_file}' before running this script.")
        exit(1)

df = pd.DataFrame(results)
df.to_excel(output_file, index=False)