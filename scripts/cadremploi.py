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
    # Critical: Remove webdriver detection traces

    # navigate to cadremploi.fr
    URL = "https://www.cadremploi.fr/"
    try:
        driver.get(URL)
        log("=" * 100)
        log(f"Reached {URL}")
    except Exception as e:
        log(f"Exception trying to reach {URL}: \n {str(e)}")
        return

    # Wait for cookies iframe to load
    try:
        iframe_xpath = "//iframe[contains(@style, 'z-index: 2147483647') and contains(@style, 'position: fixed')]"
        iframe = WebDriverWait(driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, iframe_xpath))
        )
        """ driver.switch_to.frame(iframe) """  # Switch to the iframe
        log("Switched to iframe")
    except Exception as e:
        log(f"Exception trying to wait for iframe: {str(e)}")
        return

    # reject cookies
    try:
        RejectBtn_Selector = "body > div > div > div > div > div > div > div.sc-17rhrsc-0.dkMZMt > button > span"
        human_delay(2, 3)
        RejectBtn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, RejectBtn_Selector))
        )
        RejectBtn.click()
        log("Rejected cookies")
        # Switch back to the main page (optional, if needed for later steps)
        driver.switch_to.default_content()
        log("Switched back to main page")
    except Exception as e:
        log(f"Exception trying to reject cookies: {str(e)}")
        # Always switch back to default content even if it fails
        driver.switch_to.default_content()
        return

    # click connection button:
    try:
        ConnectionBtn_XPATH = "/html/body/div[3]/header/div[1]/div[2]/div/button"
        human_delay()
        ConnectionBtn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, ConnectionBtn_XPATH))
        )
        ConnectionBtn.click()
        """ driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, ConnectionBtn_XPATH))
            ),
        ) """
        log("Clicked the connection button")
    except Exception as e:
        log(f"Excpetion trying to click connection button: {str(e)}")
        return

    # Select email and password elements
    try:
        Email_input = driver.find_element(By.NAME, "email")
        Password_input = driver.find_element(By.NAME, "password")
        log("Found email and password input elements")
    except Exception as e:
        log(f"Exception trying to find email and password elements: {str(e)}")
        return

    MYEMAIL = os.getenv("EMAIL")
    CE_PASSWORD = os.getenv("CE_PASSWORD")

    try:
        human_delay(2, 3)
        slow_send_keys(Email_input, MYEMAIL)
        human_delay(2, 3)
        slow_send_keys(Password_input, CE_PASSWORD)

        log("Succefly entered email and password")
    except Exception as e:
        log(f"Exception trying to enter email and password : {str(e)}")
        return

    # Click Je me connecte button
    try:
        human_delay(2, 3)
        Jmc_btn_XPATH = "//*[@id='modaleLogin']/fieldset/button"
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, Jmc_btn_XPATH))
            ),
        )
        log("Clicked je me connecte button")

    except Exception as e:
        log(f"Exception trying to click je me connecte button: {str(e)}")
        return

    # Click Username: Bilal
    try:
        Username_XPATH = "/html/body/div[2]/header/div[1]/div[3]/div/div/button"
        Username = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, Username_XPATH))
        )
        human_delay()
        Username.click()
        log("Clicked Username: Bilal")
    except Exception as e:
        log(f"Exception trying to click username Bilal: {str(e)}")
        return

    # Click Mon Cv
    try:
        MonCV_Selector = "#header > div.header-content > div.right > div > div > div > div.espace-perso > a:nth-child(2)"
        MonCV = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, MonCV_Selector))
        )
        human_delay()
        MonCV.click()
        log("Clicked Mon CV")
    except Exception as e:
        log(f"Exception trying to click mon cv: {str(e)}")
        return

    # Click "Visible" trigger
    try:
        Visible_XPATH = "//*[@id='js-modifier-visibilite-cv--label']"
        VisibleElement = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, Visible_XPATH))
        )
        human_delay()
        VisibleElement.click()
        log("Clicked Visible button")
    except Exception as e:
        log(f"Exception trying to click visible: {str(e)}")
        return

    # Reclick "Visible" trigger
    try:
        Visible_XPATH = "//*[@id='js-modifier-visibilite-cv--label']"
        VisibleElement = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, Visible_XPATH))
        )
        human_delay()
        VisibleElement.click()
        log("ReClicked Visible button")
    except Exception as e:
        log(f"Exception trying to ReClick visible: {str(e)}")
        return
    finally:
        log(f"Succefully updated profile on {URL}")
        driver.quit()


NavigateFunction()
