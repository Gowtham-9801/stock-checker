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
    response = requests.get(PRODUCT_URL, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    page_text = soup.get_text().lower()

    # Words that DEFINITELY mean unavailable
    out_of_stock_keywords = [
        "out of stock",
        "sold out",
        "unavailable"
    ]

    for word in out_of_stock_keywords:
        if word in page_text:
            print("Still out of stock")
            return False

    # If none of the negative words are found,
    # assume availability or status change
    print("Stock status changed")
    return True

if check_stock():
    send_telegram_message(
        "🚨 Stock Alert!\n\n"
        "The No Face Calendar appears to be AVAILABLE.\n\n"
        f"{PRODUCT_URL}"
    )
