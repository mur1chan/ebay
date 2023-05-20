import gspread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import numpy as np

driver_path = '/home/arch/truth/chromedriver'
brave_path = '/usr/bin/brave'

option = webdriver.ChromeOptions()
option.binary_location = brave_path
option.add_argument("--lang=en")

driver = webdriver.Chrome(executable_path=driver_path, options=option)
price_limit_lower = int(input("Geben sie die Untergrenze an"))
url = input("Bitte gebe die Ebay URL ein: ")
driver.get(url)
driver.implicitly_wait(10)

verkaufte_artikel = driver.find_element(By.XPATH, "//input[@type='checkbox' and @aria-label='Verkaufte Artikel']")
verkaufte_artikel.click()
print("verkaufte artikel ausgewählt")

standort_deutschland = driver.find_element(By.XPATH, "//input[@type='radio' and @aria-label='Deutschland' and @name='location']")
standort_deutschland.click()
print("deutschland als standort ausgewählt")

driver.implicitly_wait(3)

price_tags = driver.find_elements(By.XPATH, "//div[@class='s-item__detail s-item__detail--primary']/span[@class='s-item__price']/span[@class='POSITIVE']")

list_prices = [price.text for price in price_tags]

# Formatieren Sie die Preise
formatted_prices = [float(price.replace('EUR ', '').replace('.', '').replace(',', '.')) for price in list_prices if float(price.replace('EUR ', '').replace('.', '').replace(',', '.')) >= price_limit_lower]
300
# Berechnen Sie den Durchschnitt der Preise
average_price = np.mean(formatted_prices)

# Berechnen Sie die Standardabweichung der Preise
std_dev = np.std(formatted_prices)

# Ignorieren Sie Preise, die mehr als 2 Standardabweichungen vom Durchschnitt entfernt sind
filtered_prices = [price for price in formatted_prices if abs(price - average_price) <= 2 * std_dev]

# Berechnen Sie den Durchschnitt der gefilterten Preise
average_filtered_price = np.mean(filtered_prices)

print('Durchschnittspreis: ', round(average_filtered_price, 2))

sa = gspread.service_account(filename="login.json")
# Open the Google Spreadsheet
spreadsheet = sa.open("Pokemon Assets")

# Select the first worksheet in the spreadsheet
worksheet = spreadsheet.get_worksheet(0)

# Write the average price to cell E8
worksheet.update('I19', round(average_filtered_price, 2))