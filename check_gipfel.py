import os
import requests

URL = "https://diegipfelstuermer.org/collections/fussballkindergarten"
SEARCH_TEXT = "Jahrgang 2022"

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

    if SEARCH_TEXT in page:
        print("FOUND Jahrgang 2022!")
        send_telegram(
            f"🎉 Anmeldung offenbar offen: '{SEARCH_TEXT}' gefunden!\n{URL}"
        )
    else:
        print("Not found yet.")

if __name__ == "__main__":
    main()
