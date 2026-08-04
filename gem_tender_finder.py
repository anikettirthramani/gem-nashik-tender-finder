import requests
from bs4 import BeautifulSoup

# Keywords related to your business
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

# Nashik location words
LOCATION_KEYWORDS = [
    "nashik",
    "nasik",
]

# Temporary public GeM search page
GEM_URL = "https://bidplus.gem.gov.in/all-bids"


def contains_keyword(text, keywords):
    text = text.lower()
    return any(keyword in text for keyword in keywords)


def get_gem_tenders():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; Mobile) "
            "AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )
    }

    response = requests.get(
        GEM_URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    tenders = []

    # Read visible bid cards/rows
    rows = soup.find_all(
        ["tr", "div"]
    )

    for row in rows:
        text = row.get_text(
            " ",
            strip=True
        )

        if len(text) < 30:
            continue

        if contains_keyword(
            text,
            KEYWORDS
        ) and contains_keyword(
            text,
            LOCATION_KEYWORDS
        ):
            tenders.append(
                text[:1000]
            )

    # Remove duplicates
    unique_tenders = list(
        dict.fromkeys(tenders)
    )

    return unique_tenders


def main():
    print(
        "Checking GeM tenders for Nashik..."
    )

    try:
        tenders = get_gem_tenders()

        print(
            f"Matching tenders found: "
            f"{len(tenders)}"
        )

        for number, tender in enumerate(
            tenders,
            start=1
        ):
            print(
                f"\n--- Tender {number} ---"
            )
            print(tender)

    except Exception as error:
        print(
            f"Error: {error}"
        )


if __name__ == "__main__":
    main()
