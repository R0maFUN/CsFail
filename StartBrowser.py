from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import sys

def startDriver():
    # saving and loading cookies/settings/etc and trying to make selenium undetectable
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-data-dir=selenium")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # driver = webdriver.Chrome(resource_path('./chromedriver/chromedriver.exe'), options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    return driver

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)