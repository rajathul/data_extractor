from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up the driver (ensure appropriate browser driver is installed)
driver = webdriver.Chrome()

# Navigate to the historical prices page
driver.get("https://www.barchart.com/futures/quotes/IMG25/historical-prices?orderBy=contractExpirationDate&orderDir=asc&page=4")

# Wait for the page to load (adjust time as needed)
time.sleep(5)

# Click the "Price History" link (adapt the XPath/CSS selector as needed)
price_history_link = driver.find_element(By.LINK_TEXT, "Price History")
price_history_link.click()

time.sleep(2)

# Navigate to the "Daily Prices" tab and locate the CSV download button
csv_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Download CSV')]")
csv_button.click()

# Close the browser (after download completes)
driver.quit()