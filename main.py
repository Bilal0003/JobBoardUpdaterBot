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
now = datetime.now


def NavigateFunction():
    # Configure Chromium options
    chrome_options = Options()

    # Essential settings for cloud environments
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Launch chrome
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to apec.fr
    URL = "https://www.apec.fr"
    try:
        driver.get(URL)
        print(now(), f"Succssefully reached {URL}")
    except Exception as e:
        print(now(), f"Failed to navigate to {URL} : {str(e)}")
        return

    # Find 'mon espace' button and click it
    try:
        HiddenBox_Selector = "div.onetrust-pc-dark-filter ot-fade-in"
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element((By.CSS_SELECTOR, HiddenBox_Selector))
        )
    except Exception as e:
        print(now(), f"Exception occured trying to Wait for hidden box: {str(e)}")
        return

    try:
        MonEspace_Selector = "a.nav-link-espace"
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, MonEspace_Selector))
            ),
        )
        print(now(), "Clicked Mon Espace")
    except Exception as e:
        print(now(), f"Exception occured trying to click mon espace: {str(e)}")
        return

    # Enter the email and password
    try:
        email_input = driver.find_element(By.NAME, "emailid")
        password_input = driver.find_element(By.NAME, "password")
        print(now(), "Found email and password input elements")
    except Exception as e:
        print(
            now(),
            f"Excpetion occured trying to find email and password inputs: {str(e)}",
        )
        return

    MY_EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    try:
        email_input.send_keys(MY_EMAIL)
        password_input.send_keys(PASSWORD)
        print(now(), "Succesfully entered email and password")
    except Exception as e:
        print(now(), f"Exception occured trying to enter password and email: {str(e)}")
        return

    # Click the login button
    try:
        LoginBtn_Selector = "button.popin-btn-primary"
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, LoginBtn_Selector))
            ),
        )
        print(now(), "Clicked the login button")
    except Exception as e:
        print(now(), f"Excpetion occured trying to click the login button : {str(e)}")
        return

    # Navigate to CV Section
    try:
        CvSection_Selector = "a[href='#/mes-cv-lm']"
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, CvSection_Selector))
            ),
        )
        print(now(), "Clicked on the Cv Section")
    except Exception as e:
        print(now(), f"Exception occured trying to click the cv section: {str(e)}")
        return

    # Simulate edit on cv
    try:
        Cv_XPATH = "(//*[@class='cta'])[2]"
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, Cv_XPATH))
            ),
        )
        print(now(), "Clicked the edit cv Button")
    except Exception as e:
        print(now(), f"Exception occured trying to click the edit cv button : {e}")
        return

    # Click save button
    try:
        SaveBtn_XPATH = "//button[contains(text(), 'Valider')]"
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, SaveBtn_XPATH))
            ),
        )
        print(now(), "Clicked on the save button")
    except Exception as e:
        print(now(), f"Exception occured trying to click the save button: {e}")
        return
    finally:
        print(now(), f"Succesfully updated profile on {URL}")
        driver.quit()


NavigateFunction()
