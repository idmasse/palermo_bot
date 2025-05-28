import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from config import *

def get_driver():
    logger.info("Initializing Chrome driver...")

    chrome_options = Options()
    # chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('window-size=1920,1080')
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = uc.Chrome(options=chrome_options)

    # try to hide automation
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    logger.info("Chrome driver initialized successfully.")
    return driver


