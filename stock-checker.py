import requests
from bs4 import BeautifulSoup
import os

PRODUCT_URL = "https://wallfleurthings.com/product/noface-calendar"

TELEGRAM_BOT_TOKEN = os.environ["BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["CHAT_ID"]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def check_stock():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(PRODUCT_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    stock_element = soup.find("p", class_="stock")
    if not stock_element:
        print("Stock element not found")
        return False

    classes = stock_element.get("class", [])
    print("Stock classes:", classes)

    return "in-stock" in classes

if check_stock():
    send_telegram_message(
        "🎉 The No Face Calendar is BACK IN STOCK!\n\n" + PRODUCT_URL
    )
else:
    print("Still out of stock")
