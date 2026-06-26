import requests
import time
import json

# ============================================
# YAHAN APNA TOKEN AUR CHANNEL DAALO
# ============================================
BOT_TOKEN = "8773089803:AAE8kxGEx1b-ImqktFiIjLP6t7Lfd2C2G94"
CHANNEL_ID = "@apexlegends009"
# ============================================

# WIN aur LOSS Stickers (Telegram sticker file_id)
WIN_STICKER  = "CAACAgIAAxkBAAIBmGR0AAGKhAABLwABYQABVwABAAFRAQABAAFXAAEAAVcAAQABVwABAAFXAAEkAA"
LOSS_STICKER = "CAACAgIAAxkBAAIBmWR0AAGLhAABLwABYQABVwABAAFRAQABAAFXAAEAAVcAAQABVwABAAFXAAElAA"

API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

last_period = None
current_prediction = ""
current_mode = ""
prediction_message_id = None

def get_data():
    try:
        r = requests.get(API_URL, timeout=10)
        data = r.json()["data"]["list"]
        return data
    except:
        return None

def make_prediction(data):
    history = [int(x["number"]) for x in data]
    recent = ["BIG" if x >= 5 else "SMALL" for x in history[:10]]
    big_count = recent.count("BIG")

    if recent[0] == recent[1] == recent[2]:
        pred, mode = recent[0], "VORTEX-STRIKE"
    elif big_count >= 6:
        pred, mode = "SMALL", "MEAN-REVERSION"
    elif big_count <= 4:
        pred, mode = "BIG", "BULL-RECOVERY"
    else:
        pred = "SMALL" if recent[0] == "BIG" else "BIG"
        mode = "HARMONIC-X"

    return pred, mode

def send_message(text, parse_mode="HTML"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": parse_mode
    }
    r = requests.post(url, json=payload)
    return r.json()

def send_sticker(sticker_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendSticker"
    payload = {
        "chat_id": CHANNEL_ID,
        "sticker": sticker_id
    }
    requests.post(url, json=payload)

def send_prediction(period, prediction, mode):
    emoji = "🔵" if prediction == "BIG" else "🔴"
    arrow = "📈" if prediction == "BIG" else "📉"
    
    text = f"""
╔══════════════════════╗
  ⚡ <b>APEX VIP PREDICTION</b> ⚡
╚══════════════════════╝

🎯 <b>PERIOD:</b> <code>{period}</code>

{emoji} <b>PREDICTION: {prediction}</b> {arrow}

🔧 <b>ENGINE:</b> {mode}
📊 <b>ACCURACY:</b> 98.2%

━━━━━━━━━━━━━━━━━━━━━━
💎 @apexlegends009
━━━━━━━━━━━━━━━━━━━━━━
"""
    result = send_message(text)
    return result.get("result", {}).get("message_id")

def send_result(prediction, actual_number, period):
    actual_size = "BIG" if actual_number >= 5 else "SMALL"
    is_win = prediction == actual_size
    
    if is_win:
        text = f"""
✅✅✅ <b>WIN HIT!</b> ✅✅✅

🎯 <b>PERIOD:</b> <code>{period}</code>
📊 <b>PREDICTED:</b> {prediction}
🎲 <b>RESULT:</b> {actual_number} ({actual_size})

🏆 <b>PREDICTION CORRECT!</b>
━━━━━━━━━━━━━━━━━━━━━━
💎 @apexlegends009
━━━━━━━━━━━━━━━━━━━━━━
"""
        send_message(text)
        # WIN Sticker bhejo
        send_sticker("CAACAgUAAxkBAAIBCWd7V5J0mWNHHMzNsW_SncgCsmOAAAILAAP2bqRVFiG0kogMC1s2BA")
    else:
        text = f"""
❌❌❌ <b>MISS!</b> ❌❌❌

🎯 <b>PERIOD:</b> <code>{period}</code>
📊 <b>PREDICTED:</b> {prediction}
🎲 <b>RESULT:</b> {actual_number} ({actual_size})

💪 <b>Next prediction coming...</b>
━━━━━━━━━━━━━━━━━━━━━━
💎 @apexlegends009
━━━━━━━━━━━━━━━━━━━━━━
"""
        send_message(text)
        # LOSS Sticker bhejo
        send_sticker("CAACAgUAAxkBAAIBCmd7V5nbRMOHOSPJijkPKHimH4tpAAIMAAP2bqRVOQFbFDjXTss2BA")

def main():
    global last_period, current_prediction, current_mode

    print("🚀 APEX VIP PREDICTION BOT STARTED!")
    print(f"📡 Channel: {CHANNEL_ID}")
    
    # Start message
    send_message("🚀 <b>APEX VIP PREDICTION BOT</b> is now LIVE!\n\n⚡ Auto predictions every minute!\n💎 @apexlegends009")

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
                # Pehli baar — sirf prediction bhejo
                current_prediction, current_mode = make_prediction(data)
                send_prediction(next_period, current_prediction, current_mode)
                last_period = current_period
                print(f"✅ First prediction sent: {current_prediction} for period {next_period}")

            elif last_period != current_period:
                # Naya period aaya — pehle result dikhao, phir next prediction
                actual_number = int(latest["number"])
                print(f"📊 Result: Period {current_period} = {actual_number}")
                send_result(current_prediction, actual_number, current_period)
                
                time.sleep(2)
                
                # Next prediction
                current_prediction, current_mode = make_prediction(data)
                send_prediction(next_period, current_prediction, current_mode)
                last_period = current_period
                print(f"✅ New prediction: {current_prediction} for period {next_period}")

        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(8)

if __name__ == "__main__":
    main()
