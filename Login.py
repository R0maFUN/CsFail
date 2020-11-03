from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def login(driver, *args):
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