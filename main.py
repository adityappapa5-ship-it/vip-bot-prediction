import requests
import telebot
from telebot import types
import time
import os
import random
from flask import Flask
from threading import Thread

# --- SERVER FOR RAILWAY ---
app = Flask('')
@app.route('/')
def home(): return "WINGO 1M ENGINE LIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- CONFIG ---
API_TOKEN = '8216633914:AAEphghqpkKSTgvnWTD2ka95BlFwHTGRfyg'
CHANNELS = [-1003815161090, -1003973812867] 

# NEW API URL (WinGo 1M)
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)
stats = {"win": 0, "loss": 0, "count": 0}

# --- PRO API FETCH (WINGO 1M BYPASS) ---
def get_latest_data():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Origin': 'https://ar-lottery01.com',
        'Referer': 'https://ar-lottery01.com/'
    }
    try:
        # Multiple attempts to bypass lag
        for _ in range(3):
            response = requests.get(API_URL, headers=headers, timeout=15)
            if response.status_code == 200:
                json_data = response.json()
                if json_data.get('data') and json_data['data'].get('list'):
                    latest = json_data['data']['list'][0]
                    return {
                        "period": latest['issueNumber'],
                        "size": "BIG" if int(latest['number']) >= 5 else "SMALL"
                    }
            time.sleep(2)
    except Exception as e:
        print(f"API Error: {e}")
    return None

# --- REQUEST BYPASS LOGIC ---
def check_status(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']: return False
        except:
            return True # Allow if request is pending
    return True

# --- FLOW: START -> VERIFY -> PREDICT ---
@bot.message_handler(commands=['start'])
def start(message):
    if check_status(message.from_user.id):
        show_ready(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🚩 JOIN FIRST CHANNEL", url="https://t.me/+45fCzXzXxi0zMWI9"),
            types.InlineKeyboardButton("🚩 JOIN SECOND CHANNEL", url="https://t.me/+_RZ0gN9HU6xhZTRl"),
            types.InlineKeyboardButton("✅ VERIFY ACCESS ✅", callback_data="verify_final")
        )
        bot.send_message(message.chat.id, "⚔️ <b>WAR ZONE ACCESS LOCKED</b> ⚔️\n\nChannel join karke verify karo!", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify_final")
def verify(call):
    if check_status(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_ready(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "Request dalo pehle!", show_alert=True)

def show_ready(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔥 START PREDICTION 🔥"))
    bot.send_message(chat_id, "✅ <b>VERIFICATION SUCCESS</b>\nClick button for 1M Auto Prediction:", parse_mode="HTML", reply_markup=markup)

# --- AUTO ENGINE (BIG/SMALL ONLY) ---
@bot.message_handler(func=lambda m: m.text == "🔥 START PREDICTION 🔥")
def engine(message):
    global stats
    stats = {"win": 0, "loss": 0, "count": 0}
    bot.send_message(message.chat.id, "🚀 <b>ADITYA PAPA 1M ENGINE LIVE...</b>", parse_mode="HTML")

    while stats["count"] < 100:
        data = get_latest_data()
        
        if not data:
            bot.send_message(message.chat.id, "⚠️ <b>API SERVER BUSY</b>\nRetrying in 10s...", parse_mode="HTML")
            time.sleep(10)
            continue

        next_p = int(data['period']) + 1
        prediction = random.choice(["🌕 BIG", "🌑 SMALL"])
        stats["count"] += 1

        msg = (
            f"⚔️ <b>ROUND: {stats['count']}/100</b> ⚔️\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔢 <b>PERIOD:</b> <code>{next_p}</code>\n"
            f"🎯 <b>PREDICTION: {prediction}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        bot.send_message(message.chat.id, msg, parse_mode="HTML")
        
        # WinGo 1M Timing: Wait for 55 seconds (to be safe)
        time.sleep(55) 

        res_data = get_latest_data()
        if res_data:
            actual = res_data['size']
            win_loss = "✅ <b>WIN (AFEEM)</b>" if prediction.split()[1] == actual else "❌ <b>LOSS</b>"
            if "WIN" in win_loss: stats["win"] += 1
            else: stats["loss"] += 1

            bot.send_message(message.chat.id, f"📊 <b>RESULT: {actual}</b>\n💉 <b>STATUS: {win_loss}</b>", parse_mode="HTML")
        
        time.sleep(5) # Break before next period

    # Final Report
    bot.send_message(message.chat.id, f"🏁 <b>100 ROUNDS DONE!</b>\n\nTotal Wins: {stats['win']}\nTotal Loss: {stats['loss']}")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
