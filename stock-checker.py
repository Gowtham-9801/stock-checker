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
        "text": message,
        "disable_web_page_preview": True
    }
    requests.post(url, data=data, timeout=10)


def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(PRODUCT_URL, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    # --------------------------------------------------
    # 1️⃣ PRIMARY CHECK — Add to Cart button (BEST SIGNAL)
    # --------------------------------------------------
    add_to_cart_btn = soup.select_one(
        "button.single_add_to_cart_button, a.add_to_cart_button"
    )

    if add_to_cart_btn:
        classes = add_to_cart_btn.get("class", [])
        text = add_to_cart_btn.get_text(strip=True).lower()

        print("Add to cart button found")
        print("Button text:", text)
        print("Button classes:", classes)

        # Disabled button → OUT OF STOCK
        if "disabled" in classes or "out-of-stock" in classes:
            print("Button disabled → Out of stock")
            return False

        # Button exists and is clickable → IN STOCK
        print("Button enabled → IN STOCK")
        return True

    # --------------------------------------------------
    # 2️⃣ SECONDARY CHECK — Availability text (fallback)
    # --------------------------------------------------
    page_text = soup.get_text(" ", strip=True).lower()

    negative_keywords = [
        "out of stock",
        "sold out",
        "currently unavailable",
        "unavailable"
    ]

    positive_keywords = [
        "add to cart",
        "order now",
        "buy now",
        "available",
        "hurry up",
        "in stock",
        "limited stock"
    ]

    for word in negative_keywords:
        if word in page_text:
            print("Negative stock wording found → Out of stock")
            return False

    for word in positive_keywords:
        if word in page_text:
            print("Positive stock wording found → IN STOCK")
            return True

    # --------------------------------------------------
    # 3️⃣ FINAL SAFETY NET — Assume OUT OF STOCK
    # --------------------------------------------------
    print("Stock status unclear → treating as OUT OF STOCK")
    return False


if check_stock():
    send_telegram_message(
        "🚨 STOCK ALERT!\n\n"
        "The No Face Calendar appears to be AVAILABLE!\n\n"
        f"{PRODUCT_URL}"
    )
else:
    print("Still out of stock")
