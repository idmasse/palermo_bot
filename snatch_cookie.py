import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from config import *
from utils.selenium_setup import *

driver = get_driver()

# selenium shortcuts
driver_short_wait = WebDriverWait(driver, 10)
driver_long_wait = WebDriverWait(driver, 30)

def short_wait(by, value, short_wait=driver_short_wait):
    return short_wait.until(EC.element_to_be_clickable((by, value)))

def long_wait(by, value, long_wait=driver_long_wait):
    return long_wait.until(EC.element_to_be_clickable((by, value)))

shopify_login_url = "https://admin.shopify.com/"
driver.get(shopify_login_url)

shopify_login_email_field = long_wait(By.ID, "account_email")
shopify_login_email_field.send_keys(os.getenv("SHOPIFY_LOGIN_EMAIL"))
email_next_btn = short_wait(By.NAME, 'commit')
email_next_btn.click()

shopify_login_password_field = long_wait(By.ID, "account_password")
shopify_login_password_field.send_keys(os.getenv('SHOPIFY_LOGIN_PASS'))
password_next_btn = short_wait(By.NAME, 'commit')
password_next_btn.click()

try:
    remind_me_link_el = short_wait(By.CLASS_NAME, 'remind-me-later-link')
    remind_me_link_el.click()
except:
    pass

shopify_app_store_url = os.getenv('SHOPIFY_APP_STORE_URL')
driver.get(shopify_app_store_url)
time.sleep(5)

dear_lover_app_url = os.getenv('DEAR_LOVER_APP_URL')
driver.get(dear_lover_app_url)
time.sleep(5)

cookies = driver.get_cookies()

account_token = None

# extract cookie from browser request
for cookie in cookies:
    if cookie['name'] == 'account_token':
        account_token = cookie['value']
        logger.info(f"new account token scraped: {account_token}")
        break

# save cookie to file
if account_token:
    with open(TOKEN_FILE, 'w') as f:
        f.write(account_token)
        logger.info(f"new account token saved to file: {account_token}")

driver.quit()
