from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

# class Round:
#     def __init__(self):
#         self.koef = 0.0
# class Skin:
#
# class Inventory:
#

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


#Main program
waitForStrick(driver)
