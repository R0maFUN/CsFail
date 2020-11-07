from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

from Login import login
from inventory import Skin, Inventory
from bet import waitForStrick
from StartBrowser import startDriver


# template for making bets [0] - not crush, [1] - crush
#templates = [
#    [1, 1, 1],
#    [1, 1, 0, 1, 1],
#    [1, 0, 1, 0, 1],
#    [1, 1, 0, 0, 1, 1, 1]
#]

templates = [
    [1, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 1, 0, 0, 1, 1, 1],
]

# Starting the browser
driver = startDriver()
driver.get('http://cs.fail')

# Waiting for final download of the http://cs.fail
try:
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "xhistory__content"))
    )
except:
    print("Can not load the page")
    driver.quit()
    exit()

#Authorization
login(driver)

# Bet's amount that program will make
betInp = float(input("Enter the bet "))

# Waiting for user is ready
while(input("Are you ready?[y/n]") != 'y'):
    continue

# Initializing the inventory
inventory = Inventory(driver)

# Prepare the inventory for betting
inventory.SelectAll()
sleep(2)
inventory.ExchangeSelected(betInp)
sleep(1)

# Analyzing last crushes and making bets
waitForStrick(driver, inventory, templates, bet=float(betInp))
