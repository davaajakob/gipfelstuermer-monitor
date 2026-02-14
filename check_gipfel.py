import os, json, sys
import requests

URL = "https://diegipfelstuermer.org/collections/fussballkindergarten"
NEEDLE = "Jahrgang 2022"
STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"notified": False}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f)

def send_telegram(msg: str):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": msg},
        timeout=20,
    ).raise_for_status()

def main():
    state = load_state()
    r = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0 (monitor bot)"})
    r.raise_for_status()
    html = r.text

    found = NEEDLE in html
    if found and not state["notified"]:
        send_telegram(f"🎉 Anmeldung offenbar offen: '{NEEDLE}' gefunden!\n{URL}")
        state["notified"] = True
        save_state(state)
        print("Notified.")
        return

    print(f"Found={found}, notified={state['notified']}")

if __name__ == "__main__":
    try:
        main()
    except KeyError as e:
        print(f"Missing env var: {e}", file=sys.stderr)
        sys.exit(2)
