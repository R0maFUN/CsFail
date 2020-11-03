from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import sys
from collections import deque
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
        bal = driver.find_element_by_class_name("profile__coins").text
        self.balance += float(bal.strip('$'))

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
        try:
            invHtml = driver.find_elements_by_class_name("skin_theme_inventory")
            #if(len(invHtml) > 0):
            self.skins = [Skin(el) for el in invHtml]
            self.balance = sum(el.price for el in self.skins)
        except:
            self.skins = list()
            self.balance = 0
        bal = driver.find_element_by_class_name("profile__coins").text
        self.balance += float(bal.strip('$'))
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
    lastRounds = deque(maxlen=5)
    while(1):
        noCrash += 1
        invent.Update()
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
        print("Balance: "+str(invent.balance))
        if lastRoundKoef < 1.20:
            crushes+=1
            lastRounds.appendleft(1)
        else:
            crushes = 0
            lastRounds.appendleft(0)
        print("last 5 rounds: ", lastRounds)

        if crushes == 0 and noCrash >= 12:
            noCrash = 0
            driver.refresh()
            invent = Inventory(driver)
        #if(crushes >= crushStrick):
        if isBet(lastRounds, templates):
            print("Now i have to bet")
            invent.Update()
            invent.SelectSkin(bet)
            sleep(0.3)
            invent.Bet()
            betted = True


# def initButtons(driver):
#     global buttons
#     buttons = dict()
#     buttons['MakeBet'] = WebDriverWait(driver, 40).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "information__footer"))
#     )
#     buttons['OpenShop'] = driver.find_element_by_class_name("inventory__footer").find_element_by_tag_name("button")
#

def isBet(lastRounds, templates):
    for template in templates:
        bet_ = True
        if len(template) > len(lastRounds):
            continue
        i = 0
        for elTemplate in template:
            if elTemplate != lastRounds[i]:
                bet_ = False
                break
            i += 1
        if bet_:
            return True
    return False

def login(*args):
    try:
        loginButton = driver.find_element_by_class_name("profile__auth")
    except:
        print("Already logged in")
        return 0 # already logged in
    loginButton.click()
    try:
        loginInput = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "steamAccountName"))
        )
    except:
        sleep(5)
        signInButton = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "login_btn_signin"))
        )
        signInButton.click()
        print("Logged in without entering the pass")
        return 1

    passInput = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "steamPassword"))
    )
    if len(args) >= 2:
        username = str(args[0])
        password = str(args[1])
    elif len(args) == 1:
        username = str(args[0])
        password = str(input("Enter the password: "))
    else:
        username = str(input("Enter the username: "))
        password = str(input("Enter the password: "))

    loginInput.send_keys(username)
    sleep(0.3)
    passInput.send_keys(password)
    passInput.send_keys('\n')
    sleep(0.3)

    try:
        while(1):
            guardInput = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "twofactorcode_entry"))
            )
            print("Enter the steam guard code")
            sgc = str(input("Steam guard code: "))
            guardInput.send_keys(sgc)
            guardInput.send_keys('\n')
            try:
                err = WebDriverWait(driver, 6).until(
                    EC.presence_of_element_located((By.ID, "login_twofactorauth_message_incorrectcode"))
                )
                print("Incorrect steam guard code")
                continue
            except:
                print("Logged in with steam guard code")
                return 2
    except:
        print(Exception)
        print("logged in without Steam Guard")



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

login()
templates = [
    [1, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 0, 1, 0, 1]
]

#Authorization
betInp = float(input("Enter the bet "))
#crushSt = int(input("Enter the crash strick "))

while(input("Are you ready?[y/n]") != 'y'):
    continue

inventory = Inventory(driver)
for sk in inventory.skins:
    print(sk.price)

inventory.SelectAll()
sleep(2)

inventory.ExchangeSelected(betInp, driver)
sleep(1)

#Main program
waitForStrick(driver, inventory, bet=float(betInp))
