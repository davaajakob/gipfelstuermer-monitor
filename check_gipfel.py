import os
import requests

URL = "https://diegipfelstuermer.org/collections/fussballkindergarten"

KEYWORDS = [
    "Jahrgang 2022",
    "Warteliste Jahrgang 2022",
    "Fußballkindergarten 26/27",
    "Anmeldung Jahrgang 2022",
    "Warteliste 2022"
]

def send_telegram(message):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": message},
        timeout=20
    )

def main():
    print("Bot started...")

    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )

    print("Status code:", response.status_code)

    page = response.text
    print("Page length:", len(page))

    for word in KEYWORDS:
        if word in page:
            print("FOUND:", word)
            send_telegram(
                f"🎉 Mögliche Anmeldung gefunden:\n'{word}'\n{URL}"
            )
            return

    print("Nothing found yet.")

if __name__ == "__main__":
    main()
