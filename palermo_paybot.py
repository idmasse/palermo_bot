import traceback
import time
import os
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from email_utils import send_email
from dotenv import load_dotenv

load_dotenv()

def paybot(order_numbers):
    try:
        driver = webdriver.Chrome()

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

        app_url = os.getenv('APP_URL')
        driver.get(app_url)

        step_next_btn = long_wait(By.CLASS_NAME, 'step-next')
        step_next_btn.click()
        time.sleep(0.5)
        step_next_btn.click()
        time.sleep(0.5)
        step_next_btn.click()
        time.sleep(0.5)
        step_next_btn.click()
        time.sleep(0.5)
        step_next_btn.click()
        
        orders_button = short_wait(By.XPATH, '//*[@id="app"]/div[1]/div[1]/a[6]/span')
        orders_button.click()

        unpaid_orders_button = short_wait(By.XPATH, '//*[@id="app"]/div[2]/div/div[1]/span[2]')
        unpaid_orders_button.click()

        if len(order_numbers) >= 11:
            select_dropdown = short_wait(By.CLASS_NAME,'J-paginationjs-size-select')
            select = Select(select_dropdown)
            select.select_by_value('50')

        checkbox = short_wait(By.CLASS_NAME, "checkBox")
        if not checkbox.is_selected():
            checkbox.click()

        batchpay = short_wait(By.CLASS_NAME, "pay")
        batchpay.click()

        paypal_button = long_wait(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/dl/ul/li[1]')
        paypal_button.click()

        pay_button = short_wait(By.CLASS_NAME, 'pay-btn')
        pay_button.click()

        pp_email_field = short_wait(By.ID, 'email')
        pp_email_field.send_keys(os.getenv('PP_EMAIL'))
        login_next_btn = short_wait(By.ID, 'btnNext')
        login_next_btn.click()

        pp_pw_field = long_wait(By.ID, 'password')
        pp_pw_field.send_keys(os.getenv('PP_PW'))
        login_btn = short_wait(By.ID, 'btnLogin')
        login_btn.click()

        send_payment_btn = long_wait(By.ID, 'payment-submit-btn')
        send_payment_btn.click()

        payment_confirmation = long_wait(By.XPATH, '/html/body/div[3]/div[2]/div/p[2]')
        payment_confirmation_text = payment_confirmation.text
        print(f'{payment_confirmation_text}')

        driver.quit()

        print(f'Palermo paybot ran successfully and processed orders: {order_numbers}')
        send_email("Palermo Paybot Ran Sucessfully", f"Palermo paybot ran successfully and processed orders: {order_numbers}")
    except Exception as e:
        error_message = traceback.format_exc()
        print(f"paybot failed", f"ERROR MESSAGE: {e}\n {error_message}")
        send_email(f"palermo payBot failed", f"ERROR MESSAGE: {e}\n {error_message}")
