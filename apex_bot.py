import requests
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ============================================
BOT_TOKEN = "8939499145:AAH4x7-Wvo6EYf7Obazusaur65EL6lffMwk"
CHANNEL_ID = "@apexpremium009"
# ============================================

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running!')
    def log_message(self, format, *args):
        pass

threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 10000), Handler).serve_forever(), daemon=True).start()

API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

WIN_STICKER  = "CAACAgUAAxkBAAIBCWd7V5J0mWNHHMzNsW_SncgCsmOAAAILAAP2bqRVFiG0kogMC1s2BA"
LOSS_STICKER = "CAACAgUAAxkBAAIBCmd7V5nbRMOHOSPJijkPKHimH4tpAAIMAAP2bqRVOQFbFDjXTss2BA"

last_period = None
current_prediction = ""

def get_data():
    try:
        r = requests.get(API_URL, timeout=10)
        return r.json()["data"]["list"]
    except:
        return None

def make_prediction(data):
    history = [int(x["number"]) for x in data]
    recent = ["BIG" if x >= 5 else "SMALL" for x in history[:10]]
    big_count = recent.count("BIG")

    if recent[0] == recent[1] == recent[2]:
        return recent[0]
    elif big_count >= 6:
        return "SMALL"
    elif big_count <= 4:
        return "BIG"
    else:
        return "SMALL" if recent[0] == "BIG" else "BIG"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML"})

def send_sticker(sticker_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendSticker"
    requests.post(url, json={"chat_id": CHANNEL_ID, "sticker": sticker_id})

def send_prediction(period, prediction):
    last6 = str(period)[-6:]
    arrow = "📈" if prediction == "BIG" else "📉"
    text = f"""👑..APEX PREMIUM..👑

🔰 𝗪𝗜𝗡 𝗚𝗢 𝟭 𝗠𝗜𝗡𝗨𝗧𝗘💰

{last6} =⟩  {prediction} {arrow}"""
    send_message(text)

def send_result(prediction, actual_number, period):
    actual_size = "BIG" if actual_number >= 5 else "SMALL"
    is_win = prediction == actual_size
    if is_win:
        send_sticker(WIN_STICKER)
    else:
        send_sticker(LOSS_STICKER)

def main():
    global last_period, current_prediction
    print("🚀 APEX PREMIUM BOT STARTED!")

    while True:
        try:
            data = get_data()
            if not data:
                time.sleep(5)
                continue

            latest = data[0]
            current_period = latest["issueNumber"]
            next_period = str(int(current_period) + 1)

            if last_period is None:
                current_prediction = make_prediction(data)
                send_prediction(next_period, current_prediction)
                last_period = current_period
                print(f"✅ Prediction: {current_prediction} for {next_period}")

            elif last_period != current_period:
                actual_number = int(latest["number"])
                send_result(current_prediction, actual_number, current_period)
                time.sleep(2)
                current_prediction = make_prediction(data)
                send_prediction(next_period, current_prediction)
                last_period = current_period
                print(f"✅ Prediction: {current_prediction} for {next_period}")

        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(8)

if __name__ == "__main__":
    main()
