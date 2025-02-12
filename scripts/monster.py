import undetected_chromedriver as uc
from dotenv import load_dotenv
from datetime import datetime
import os, time, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth


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
    """Send down keys to input element one key at a time"""
    for char in input:
        el.send_keys(char)
        human_delay(0.1, 0.3)


def NavigateFunction():

    # Configure Chromium options
    chrome_options = uc.ChromeOptions()

    # Essential headless arguments
    chrome_options.add_argument("--headless=new")  # Modern headless mode
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Remove automation indicators
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Point to my chrome profil
    MyProfile = "/home/bilal0003/.config/google-chrome"
    chrome_options.add_argument(f"--user-data-dir={MyProfile}")
    chrome_options.add_argument("--profile-directory=Default")
    # Modern user-agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    # chrome_options.add_argument(f"user-agent={user_agent}")

    driver = uc.Chrome(
        options=chrome_options,
        version_main=132,
    )

    # stealth driver (did the job for me, i had problems with headless mode being detected)
    stealth(
        driver,
        user_agent=user_agent,
        languages=["en-US", "en"],  # Provide valid language codes
        platform="Win32",  # A typical platform string for Windows
    )

    # navigate to monster.fr
    URL = "https://www.monster.fr/"
    try:
        driver.get(URL)
        log("=" * 100)
        log(f"Reached {URL}")
    except Exception as e:
        log(f"Exception trying to reach {URL}: \n {str(e)}")
        return

    # reject coockies if not already
    CookieBannerXPATH = "//*[@id='onetrust-consent-sdk']"
    isCookieBannerPresent = EC.visibility_of_element_located(
        (By.XPATH, CookieBannerXPATH)
    )
    if isCookieBannerPresent:
        log("Cookie banner is present")
        try:
            RejectBtn_XPATH = "//*[@id='onetrust-reject-all-handler']"
            RejectBtn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, RejectBtn_XPATH))
            )
            human_delay()
            RejectBtn.click()
            log(f"Rejected coockies")
        except Exception as e:
            log(f"Exception trying to reject cookies: {str(e)}")
            # return

    # connect via gmail
    try:
        GmailXPATH = "//span[contains(text(), 'Se connecter')]"
        GmailBtn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, GmailXPATH))
        )
        human_delay(2, 3.5)
        GmailBtn.click()
        log("Clicked connect via gmail button")
    except Exception as e:
        log(f"Exception trying to click connect via gmail: {str(e)}")
        return

    # Click my mail
    try:
        MyMailXPATH = "//div[contains(text(), 'Poursuivre avec Google')]"
        MyMailBtn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, MyMailXPATH))
        )
        human_delay(3, 4)
        MyMailBtn.click()
        log(f"Clicked My Email")
    except Exception as e:
        log(f"Exceptin trying to click my mail : {str(e)}")
        return

    # Close annoying unpredictable popup
    try:
        PopUpXPATH = "//button[@data-testid='dismiss-iconbutton']"
        PopUp = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, PopUpXPATH))
        )
        human_delay(2, 3)
        PopUp.click()
        log(f"Closed Popup")
    except Exception as e:
        log(f"Exception trying to close popup: {str(e)}")
        return

    # Click mon profil button
    try:
        MonProfileXPATH = "//a[@data-testid='profile-navigation-item-profile']"
        MonProfileBtn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, MonProfileXPATH))
        )
        human_delay(2, 3)
        MonProfileBtn.click()
        log("Clicked Mon profil button")
    except Exception as e:
        log(f"Exception trying to click mon profil button :{str(e)}")
        return

    # Click edit cv icon/btn
    try:
        EditCVXPATH = "//a[@data-testid='resume-document-section-editlink']"
        EditCvBtn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, EditCVXPATH))
        )
        human_delay(2, 3)
        EditCvBtn.click()
        log("Clicked Edit Cv button")
    except Exception as e:
        log(f"Exception trying to click edit cv button: {str(e)}")
        return

    # Click upload field:
    try:
        UploadDivXPATH = (
            "//div[@role='button' and @data-testid='upload-from-device-button']"
        )
        UploadDiv = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, UploadDivXPATH))
        )
        human_delay(2, 3)
        UploadDiv.click()
        log(f"Clicked Upload file button")
    except Exception as e:
        log(f"Exception trying to click upload file: {str(e)}")
        return

    # Send file URI to the input element:
    try:
        fileURI = "/home/bilal0003/Projects/JobBoardUpdaterBot/CV.pdf"
        InputElementXPATH = "//input[@type='file']"
        fileInput = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, InputElementXPATH))
        )
        human_delay(3.5, 6)
        fileInput.send_keys(fileURI)
        log(f"Uploaded CV Succesfully")
    except Exception as e:
        log(f"Exception trying to upload Cv: {str(e)}")
        return

    # Click "Telecharger" button
    try:
        TelechargerXPATH = (
            "//button[@data-testid='onboarding-use-this-document-button']"
        )
        TelchargerBtn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, TelechargerXPATH))
        )
        human_delay(2, 3)
        TelchargerBtn.click()
        log("Clicked Telecharger button")
    except Exception as e:
        log(f"Exception trying to click telecharger button: {str(e)}")
        return

    # Click "Telecharger et remplacer" button
    try:
        TeleEtRempXPATH = "//button[@data-testid='upload-and-parse-button']"
        TeleEtRempBtn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, TeleEtRempXPATH))
        )
        human_delay(2, 3)
        TeleEtRempBtn.click()
        log(f"Clicked Telecharger et remplacer button")
    except Exception as e:
        log(f"Exception trying to click Telecharger et remplacer button: {str(e)}")
        return
    # Wait for upload then quit
    finally:
        time.sleep(15)
        log(f"Succesfully updated profile on: {URL}")
        driver.quit()


NavigateFunction()
