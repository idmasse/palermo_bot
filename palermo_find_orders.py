import requests
from paybot import paybot
from utils.email_utils import send_email
import os 
from config import *

with open(TOKEN_FILE, 'r') as f:
    account_token = f.read().strip()

find_orders_url = os.getenv('FIND_ORDERS_URL')
headers = {
    "Cookie": f"account_token={account_token}"
}

def find_orders():
    try:
        response = requests.get(find_orders_url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            order_numbers = [order["shopify_itemno"] for order in data["data"]["list"] if order["financial_status"] != "refunded"]
            
            if order_numbers:
                logger.info(f"found new orders: {order_numbers} executing palermo paybot with order numbers")
                paybot(order_numbers)
            else:
                print("palermo bot didnt find any order numbers to process.")
                return
        else:
            logger.error(f"palermo order bot failed to fetch order data. status code: {response.status_code}")
    except Exception as e:
        logger.error(f"palermo bot failed: {e}")
        send_email(f"Palermo bot failed while finding orders", f"palermo order bot failed to find orders with status code: {response.status_code} and error \n{e}")

if __name__ == '__main__':
    find_orders()

