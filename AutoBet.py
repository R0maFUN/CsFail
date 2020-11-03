from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import sys
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
        invHtml = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "skin_theme_inventory"))
    )
        if (len(invHtml) > 0):
            self.skins = [Skin(el) for el in invHtml]
            self.balance = sum(el.price for el in self.skins)
        else:
            self.skins = list()
            self.balance = 0
        self.selectedSkins = list()
        self.selectedSkinsPrice = 0
        self.shopHtml = driver.find_element_by_class_name("inventory__footer")
        self.shopHtml = self.shopHtml.find_element_by_tag_name("button")
        self.betButton = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.CLASS_NAME, "information__footer"))
    )
        #self.betButton = self.betButton.find_element_by_tag_name("button")
        print(self.betButton.text)
    def Update(self):
        #self.UnSelectAll()
        invHtml = driver.find_elements_by_class_name("skin_theme_inventory")
        if(len(invHtml) > 0):
            self.skins = [Skin(el) for el in invHtml]
            self.balance = sum(el.price for el in self.skins)
        else:
            self.skins = list()
            self.balance = 0
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
                try:
                    skin.htmlObj.click()
                except:
                    pass
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
            if skin.isSelected == True:
                skin.htmlObj.click()
                skin.isSelected = False
                self.selectedSkins.remove(skin)
                self.selectedSkinsPrice -= skin.price
                sleep(0.5)
    def ExchangeSelected(self, price, driver):
        self.shopHtml.click()
        inputHtml = driver.find_element_by_class_name("filter_price")
        inputHtml = inputHtml.find_element_by_tag_name("input")
        sleep(0.4)
        inputHtml.send_keys(Keys.CONTROL, 'a')
        inputHtml.send_keys(Keys.CONTROL, 'x')
        inputHtml.send_keys(str(price))
        sleep(0.5)
        skinWindowHtml = driver.find_element_by_class_name("skins_for_window")
        skinWindowHtml = skinWindowHtml.find_element_by_class_name("skin_window")
        skinWindowHtml.click()
        buyButtonHtml = driver.find_element_by_class_name("xbutton_buy")
        buyButtonHtml.click()
        sleep(0.6)
        closeShopHtml = driver.find_element_by_class_name("shop__close")
        closeShopHtml.click()
        self.Update()
    def Bet(self):
        self.betButton.click()
        #self.Update()

def waitForStrick(driver, invent, crushStrick = 1,bet = 0.25, strategy = 0): # Getting latest round and checking for X crash strick
    lastRound = driver.find_element_by_class_name('xhistory__link')

    lastRoundKoef, lastRoundId = lastRound.text, int(lastRound.get_attribute('href').split('/')[-1])
    crushes = 0
    betted = False
    noCrash = 0
    while(1):
        noCrash += 1
        lastRound = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, {str(lastRoundId+1)})]"))
        ) #wait for next round showed in history
        if (betted):
            invent.Update()
            invent.SelectAll()
            invent.ExchangeSelected(bet, driver)
            betted = False
        lastRoundKoef, lastRoundId = float(lastRound.text.strip('x')), int(lastRound.get_attribute('href').split('/')[-1])
        print(lastRoundKoef, lastRoundId)
        if lastRoundKoef < 1.20:
            crushes+=1
        else:
            crushes = 0
        if crushes == 0 and noCrash >= 12:
            noCrash = 0
            driver.refresh()
            invent = Inventory(driver)
        if(crushes >= crushStrick):
            print("Now i have to bet")
            invent.SelectSkin(bet)
            invent.Bet()
            betted = True


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

chrome_options = Options() # saving and loading cookies/settings/etc and trying to make selenium undetectable

#ua = UserAgent()
#userAgent = ua.random
#print(userAgent)
chrome_options.add_argument("start-maximized")
#chrome_options.add_argument(f'user-agent={userAgent}')
chrome_options.add_argument("user-data-dir=selenium")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

#driver = webdriver.Chrome(resource_path('./chromedriver/chromedriver.exe'), options=chrome_options)
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
betInp = float(input("Enter the bet "))
crushSt = int(input("Enter the crash strick "))

print("Make an authorization")
while(input("Did you log in?[y/n]") != 'y'):
    continue

test = Inventory(driver)
for sk in test.skins:
    print(sk.price)

#test.SelectSkin(0.36)
#sleep(2)
test.SelectAll()
sleep(2)
# test.UnSelectSkin(price=2.49)
# sleep(2)
test.ExchangeSelected(betInp, driver)
sleep(1)
#test.SelectSkin(0.25)
#Main program



waitForStrick(driver, test, bet=float(betInp), crushStrick=crushSt)
