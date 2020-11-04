from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from collections import deque
from inventory import Inventory
from datetime import datetime
from termcolor import colored

def waitForStrick(driver, invent, templates, crushStrick = 1,bet = 0.25, strategy = 0): # Getting latest round and checking for X crash strick
    doublesBetweenTriples = [0]
    soloBetweenDoubles = [0]
    triplesBetweenQuadros = [0]
    lastRound = driver.find_element_by_class_name('xhistory__link')
    lastRoundKoef, lastRoundId = lastRound.text, int(lastRound.get_attribute('href').split('/')[-1])
    crushes = 0
    betted = False
    noCrash = 0
    lastRounds = deque(maxlen=7)

    while(1):
        noCrash += 1
        # updating the inventory
        #invent.Update()
        # wait for next round showed in history
        lastRound = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, {str(lastRoundId+1)})]"))
        )
        invent.Update()
        # if we made bet in the previous round, update the inventory and buy new skin with set price
        if (betted):
            invent.Update()
            invent.SelectAll()
            invent.ExchangeSelected(bet)
            betted = False
        # bring to the desired form
        lastRoundKoef, lastRoundId = float(lastRound.text.strip('x')), int(lastRound.get_attribute('href').split('/')[-1])
        print(colored(lastRoundKoef, 'blue'), colored(lastRoundId, 'blue'))
        print("Balance: "+str(invent.balance))
        if lastRoundKoef < 1.20:
            crushes+=1
            lastRounds.appendleft(1)
        else:
            if crushes == 1:
                soloBetweenDoubles[-1] += 1
            elif crushes == 2:
                soloBetweenDoubles.append(0)
                doublesBetweenTriples[-1] += 1
            elif crushes == 3:
                doublesBetweenTriples.append(0)
                triplesBetweenQuadros[-1] += 1
            elif crushes == 4:
                triplesBetweenQuadros.append(0)
            crushes = 0
            lastRounds.appendleft(0)
        print("last 5 rounds: ", lastRounds)
        print("Solo Between Doubles: ", soloBetweenDoubles)
        print("Doubles Between Triples: ", doublesBetweenTriples)
        print("Triples Between Quadros: ", triplesBetweenQuadros)
        if crushes == 0 and noCrash >= 12:
            noCrash = 0
            driver.refresh()
            invent = Inventory(driver)
        #if(crushes >= crushStrick):
        if isBet(lastRounds, templates):
            print(colored("Now i have to bet ", 'red'), colored(datetime.now().time(),'red') )
            invent.Update()
            invent.SelectSkin(bet)
            sleep(0.3)
            invent.Bet()
            betted = True

# compare last rounds with the templates, returns True if program should make a bet
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
