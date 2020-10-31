from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
#from fake_useragent import UserAgent

# class Round:
#     def __init__(self):
#         self.koef = 0.0
class Skin:
    def __init__(self, htmlObject):
        self.htmlObj = htmlObject
        self.price = htmlObject.find_element_by_class_name("skin__coins").text
        self.price = float(self.price.strip('$'))
        self.isSelected = False

class Inventory:
    def __init__(self, driver):
        invHtml = driver.find_elements_by_class_name("skin_theme_inventory")
        self.skins = [Skin(el) for el in invHtml]
        self.balance = sum(el.price for el in self.skins)
        self.selectedSkins = list()
        self.selectedSkinsPrice = 0
    def SelectSkin(self, price):
        for skin in self.skins:
            if skin.price == price and skin.isSelected == False:
                skin.htmlObj.click()
                skin.isSelected = True
                self.selectedSkins.append(skin)
                self.selectedSkinsPrice += skin.price
                return
    def UnSelectSkin(self, price):
        for skin in self.skins:
            if skin.price == price and skin.isSelected == True:
                skin.htmlObj.click()
                skin.isSelected = False
                self.selectedSkins.remove(skin)
                self.selectedSkinsPrice -= skin.price
                return
    def SelectAll(self):
        for skin in self.skins:
            if skin.isSelected == False:
                skin.htmlObj.click()
                skin.isSelected = True
                self.selectedSkins.append(skin)
                self.selectedSkinsPrice += skin.price
                sleep(0.5)
    def UnSelectAll(self):
        for skin in self.skins:
            if skin.isSelected == False:
                skin.htmlObj.click()
                skin.isSelected = True
                self.selectedSkins.append(skin)
                self.selectedSkinsPrice += skin.price
                sleep(0.5)

def waitForStrick(driver, crushStrick = 1): # Getting latest round and checking for X crash strick
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



chrome_options = Options() # saving and loading cookies/settings/etc and trying to make selenium undetectable

#ua = UserAgent()
#userAgent = ua.random
#print(userAgent)
chrome_options.add_argument("start-maximized")
#chrome_options.add_argument(f'user-agent={userAgent}')
chrome_options.add_argument("user-data-dir=selenium")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

#driver = webdriver.Chrome()
driver.get('http://cs.fail')

try:
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "xhistory__content"))
    )
except:
    driver.quit()

#Authorization
print("Make an authorization")
while(input("Did you log in?[y/n]") != 'y'):
    continue

test = Inventory(driver)
for sk in test.skins:
    print(sk.price)

test.SelectSkin(price=0.25)
sleep(2)
test.SelectAll()
sleep(2)
test.UnSelectSkin(price=2.49)
sleep(2)
#Main program
waitForStrick(driver)
