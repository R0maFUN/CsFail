from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.keys import Keys

class Skin:
    def __init__(self, htmlObject):
        self.htmlObj = htmlObject
        self.price = htmlObject.find_element_by_class_name("skin__coins").text
        self.price = float(self.price.strip('$'))
        self.isSelected = False

class Inventory:
    def __init__(self, driver):
        # list of skin's html objects
        invHtml = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "skin_theme_inventory"))
        )
        if (len(invHtml) > 0):
            self.skins = [Skin(el) for el in invHtml]
            self.balance = round(sum(el.price for el in self.skins), 2)
        else:
            self.skins = list()
            self.balance = 0
        bal = driver.find_element_by_class_name("profile__coins").text
        self.balance += round(float(bal.strip('$')), 2)

        self.selectedSkins = list()
        self.selectedSkinsPrice = 0
        self.shopHtml = driver.find_element_by_class_name("inventory__footer")
        self.shopHtml = self.shopHtml.find_element_by_tag_name("button")
        self.betButton = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "information__footer"))
        )
        self.driver = driver
        print(self.betButton.text)
    def Update(self):
        #self.UnSelectAll()
        try:
            invHtml = self.driver.find_elements_by_class_name("skin_theme_inventory")
            self.skins = [Skin(el) for el in invHtml]
            self.balance = round( sum(el.price for el in self.skins), 2)
        except:
            self.skins = list()
            self.balance = 0
        bal = self.driver.find_element_by_class_name("profile__coins").text
        self.balance += round(float(bal.strip('$')), 2)
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
        # if did not find needed skin, buy it in the shop
        self.ExchangeSelected(price)
        self.SelectSkin(price)
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
    def ExchangeSelected(self, price):
        self.shopHtml.click()
        inputHtml = self.driver.find_element_by_class_name("filter_price")
        inputHtml = inputHtml.find_element_by_tag_name("input")
        sleep(0.4)
        inputHtml.send_keys(Keys.CONTROL, 'a')
        inputHtml.send_keys(Keys.CONTROL, 'x')
        inputHtml.send_keys(str(price))
        sleep(0.4)
        skinWindowHtml = self.driver.find_element_by_class_name("skins_for_window")
        skinWindowHtml = skinWindowHtml.find_element_by_class_name("skin_window")
        skinWindowHtml.click()
        buyButtonHtml = self.driver.find_element_by_class_name("xbutton_buy")
        buyButtonHtml.click()
        sleep(0.4)
        closeShopHtml = self.driver.find_element_by_class_name("shop__close")
        closeShopHtml.click()
        self.Update()
    def Bet(self):
        self.betButton.click()
        #self.Update()
