import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

GEM_URL = "https://bidplus-global.gem.gov.in/"

KEYWORDS = [
    "fly ash",
    "pond ash",
    "transportation",
    "transport",
    "loading",
    "unloading",
    "backhoe loader",
    "jcb",
    "earthmoving",
    "earth moving",
    "excavation",
    "earthwork",
    "earth work",
    "dumper",
]

LOCATION_KEYWORDS = [
    "nashik",
    "nasik",
]


def contains_keyword(text, keywords):
    text = text.lower()
    return any(
        keyword in text
        for keyword in keywords
    )


def send_telegram_message(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram secrets are missing.")
        return

    url = (
        "https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
        },
        timeout=30,
    )

    response.raise_for_status()
    print("Telegram message sent.")


def get_gem_tenders():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        GEM_URL,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    tenders = []

    for item in soup.find_all(
        ["tr", "div"]
    ):
        text = item.get_text(
            " ",
            strip=True,
        )

        if len(text) < 30:
            continue

        has_keyword = contains_keyword(
            text,
            KEYWORDS,
        )

        has_location = contains_keyword(
            text,
            LOCATION_KEYWORDS,
        )

        if has_keyword and has_location:
            tenders.append(
                text[:800]
            )

    return list(
        dict.fromkeys(tenders)
    )


def main():
    print(
        "Checking GeM tenders..."
    )

    tenders = get_gem_tenders()

    print(
        "Matching tenders:",
        len(tenders),
    )

    if len(tenders) == 0:
        print(
            "No matching tender found."
        )
        return

    message = (
        "NEW GeM TENDER ALERT\n\n"
        "Location: Nashik\n\n"
    )

    for number, tender in enumerate(
        tenders[:5],
        start=1,
    ):
        message += (
            f"{number}. {tender}\n\n"
        )

    message += (
        "https://bidplus.gem.gov.in/all-bids"
    )

    send_telegram_message(
        message
    )


if __name__ == "__main__":
    main()
