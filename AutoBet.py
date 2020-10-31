from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# class Round:
#     def __init__(self):
#         self.koef = 0.0
# class Skin:
#
# class Inventory:
#

def nameforfun(driver, crushStrick = 1): # Getting latest round and checking for X crash strick
    lastRound = driver.find_element_by_class_name('xhistory__link')
    lastRoundKoef, lastRoundId = lastRound.text, int(lastRound.get_attribute('href').split('/')[-1])

    crushes = 0
    while(1):
        lastRound = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, {str(lastRoundId+1)})]"))
        ) #wait for next round showed in history
        lastRoundKoef, lastRoundId = float(lastRound.text.strip('x')), int(lastRound.get_attribute('href').split('/')[-1])
        print(lastRoundKoef, lastRoundId)
        if lastRoundKoef < 1.20:
            crushes+=1
        else:
            crushes = 0
        if(crushes == crushStrick):
            print("Now i have to bet")



driver = webdriver.Chrome()
driver.get('http://cs.fail')

try:
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "xhistory__content"))
    )
except:
    driver.quit()

nameforfun(driver)
