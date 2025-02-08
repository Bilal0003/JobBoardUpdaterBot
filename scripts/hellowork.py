from dotenv import load_dotenv
from datetime import datetime
import os, time, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# load email and password from env file
load_dotenv()
# define a function reference for later use
now = datetime.now


# helper function for loging
def log(msg: str):
    return print(now(), msg)


# helper function for adding a delay
def human_delay(min_sec=0.5, max_sec=2.0):
    """Random delay to mimic human interaction."""
    time.sleep(random.uniform(min_sec, max_sec))


# helper function to slow down the send_keys function
def slow_send_keys(el, input: str):
    """Send down keys to input element on key at a time"""
    for char in input:
        el.send_keys(char)
        human_delay(0.1, 0.2)


def NavigateFunction():
    # Configure Chromium options
    chrome_options = Options()

    # Disable automation flags and features
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")

    # Mask automation indicators
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Set a common user-agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")

    # Launch chrome
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    # Override navigator.webdriver property
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    # Navigate to hellowork.fr
    URL = "https://www.hellowork.com/fr-fr/"
    try:
        driver.get(URL)
        log("=" * 100)
        log(f"Reached {URL}")
    except Exception as e:
        log(f"Failed to reach {URL}")
        return

    # Reject Coockies
    try:
        RejectBtn_XPATH = "//button[@id='hw-cc-notice-continue-without-accepting-btn']"
        human_delay(2, 3)
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, RejectBtn_XPATH))
            ),
        )
        log("Rejected coockies")
    except Exception as e:
        log(f"Exception occured clicking reject cookies btn: {str(e)}")
        return

    # Find and click "Mon Compte" button
    try:
        MonBtn_XPATH = "//summary[./span[text()='Mon compte']]"
        human_delay(1.5, 2)  # wait human delay
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, MonBtn_XPATH))
            ),
        )
        log("Selected Mon Compte button")
    except Exception as e:
        log(f"Exception occured trying to select Mon Compte button : {str(e)}")
        return

    # Click "Se Connecter" button
    try:
        SeConnecterBtn_XPATH = "//./span[text()='Se connecter']"
        human_delay(1, 1.5)  # wait human delay
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, SeConnecterBtn_XPATH))
            ),
        )
        log("Clicked Se connecter tab.")
    except Exception as e:
        log(f"Execption occured trying click Se Connecter tab")
        return

    # Enter credentials and login
    try:
        Email_input = driver.find_element(By.NAME, "email2")
        Password_input = driver.find_element(By.NAME, "password2")
        log("Found email and password input elements")
    except Exception as e:
        log(
            f"Exception occured trying to locate email and passwor input elements: {str(e)}"
        )
        return

    MYEMAIL = os.getenv("EMAIL")
    HW_PASSWORD = os.getenv("HW_PASSWORD")

    try:
        human_delay(5, 10)
        slow_send_keys(Email_input, MYEMAIL)
        human_delay(1.7, 2.3)
        slow_send_keys(Password_input, HW_PASSWORD)

        log("Succefully entered email and password")
    except Exception as e:
        log(f"Exception occured trying to enter email and/or password: {str(e)}")
        return

    # Click login button

    # getting captcha error: try different browser, by friendlycaptcha
    try:
        human_delay(1, 1.7)
        LoginBtn_XPATH = "//button[normalize-space(text())='Je me connecte']"
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, LoginBtn_XPATH))
            ),
        )
        print(now(), "Clicked the login button")
    except Exception as e:
        print(now(), f"Excpetion occured trying to click the login button : {str(e)}")
        return

    # Click UserName
    try:
        human_delay(2, 3)
        UserName_Xpath = "//summary[./span[text()='Bilal']]"
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, UserName_Xpath))
            ),
        )
        log("Clicked Username : Bilal")
    except Exception as e:
        log(f"Exception occured trying to click username: {str(e)}")
        return

    # Navigate to profile
    try:
        human_delay(2, 3)
        MonProfil_Xpath = "//span[@data-controller='atc' and @data-cy='headerAccountMyAccountLink' and @data-atc-l-value='x/se-se/pnaqvqng/cebsvy=pt=ugzyf']"
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, MonProfil_Xpath))
            ),
        )
        log("Reached Mon Profil")
    except Exception as e:
        log(f"Exception occured trying to visit profile page: {str(e)}")
        return

    # Simulate edit
    try:
        PosteActuel_XPATH = "//./span[text()='Développeur']"
        human_delay(1.5, 3)
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, PosteActuel_XPATH))
            ),
        )
        log("Clicked Poste actuel")
    except Exception as e:
        log(f"Exception occured trying to click poste actuel: {str(e)}")
        return

    try:
        SaveBtn_XPATH = "//button[@class='profile-form-save' and @data-simple-progress]"
        human_delay(1, 2.5)
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, SaveBtn_XPATH))
            ),
        )
        log("Clicked Save profile")
    except Exception as e:
        log(f"Exception occured trying to click the J'enregistre button: {str(e)}")
        return
    finally:
        log(f"Succesfully updated profile on {URL}")
        driver.quit()


NavigateFunction()
