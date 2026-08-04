import os
import requests
from bs4 import BeautifulSoup

# Telegram settings from GitHub Secrets

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Your business-related keywords

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

# Nashik location keywords

LOCATION_KEYWORDS = [
"nashik",
"nasik",
]

GEM_URL = "https://bidplus.gem.gov.in/all-bids"

def contains_keyword(text, keywords):
text = text.lower()
return any(keyword in text for keyword in keywords)

def send_telegram_message(message):
if not BOT_TOKEN or not CHAT_ID:
print("Telegram secrets are missing.")
return

```
url = (
    f"https://api.telegram.org/"
    f"bot{BOT_TOKEN}/sendMessage"
)

data = {
    "chat_id": CHAT_ID,
    "text": message,
    "disable_web_page_preview": True,
}

response = requests.post(
    url,
    data=data,
    timeout=30,
)

response.raise_for_status()
print("Telegram message sent successfully.")
```

def get_gem_tenders():
headers = {
"User-Agent": (
"Mozilla/5.0 "
"(X11; Linux x86_64) "
"AppleWebKit/537.36 "
"Chrome/130 Safari/537.36"
)
}

```
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

for row in soup.find_all(["tr", "div"]):
    text = row.get_text(
        " ",
        strip=True,
    )

    if len(text) < 30:
        continue

    keyword_match = contains_keyword(
        text,
        KEYWORDS,
    )

    location_match = contains_keyword(
        text,
        LOCATION_KEYWORDS,
    )

    if keyword_match and location_match:
        tenders.append(
            text[:900]
        )

return list(
    dict.fromkeys(tenders)
)
```

def main():
print(
"Checking GeM tenders for Nashik..."
)

```
try:
    tenders = get_gem_tenders()

    print(
        "Matching tenders found:",
        len(tenders),
    )

    if not tenders:
        print(
            "No matching tender found."
        )
        return

    message = (
        "NEW GeM TENDER ALERT\n\n"
        "Location: Nashik\n"
        f"Matching tenders: "
        f"{len(tenders)}\n\n"
    )

    for number, tender in enumerate(
        tenders[:5],
        start=1,
    ):
        message += (
            f"{number}. {tender}\n\n"
        )

    message += (
        "GeM Bid Search:\n"
        "https://bidplus.gem.gov.in/"
        "all-bids"
    )

    send_telegram_message(
        message
    )

except Exception as error:
    print(
        "Error:",
        error,
    )

    try:
        send_telegram_message(
            "GeM Tender Finder Error:\n"
            f"{error}"
        )
    except Exception:
        pass

    raise
```

if **name** == "**main**":
main()
