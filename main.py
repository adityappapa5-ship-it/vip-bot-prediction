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
def home(): return "API FIXED LIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- CONFIG ---
API_TOKEN = '8216633914:AAEphghqpkKSTgvnWTD2ka95BlFwHTGRfyg'
CHANNELS = [-1003815161090, -1003973812867] 
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)
stats = {"win": 0, "loss": 0, "count": 0}

# --- PRO API FETCH (WINGO 1M BYPASS) ---
def get_latest_data():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Origin': 'https://ar-lottery01.com',
        'Referer': 'https://ar-lottery01.com/',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    try:
        # Session use karne se block nahi hoga
        with requests.Session() as s:
            response = s.get(API_URL, headers=headers, timeout=15)
            if response.status_code == 200:
                json_data = response.json()
                if json_data.get('data') and json_data['data'].get('list'):
                    latest = json_data['data']['list'][0]
                    return {
                        "period": latest['issueNumber'],
                        "size": "BIG" if int(latest['number']) >= 5 else "SMALL"
                    }
    except: pass
    return None

def check_status(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']: return False
        except: return True # Request bypass
    return True

# --- FLOW: START & VERIFY ---
@bot.message_handler(commands=['start'])
def start(message):
    if check_status(message.from_user.id):
        show_btn(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🚩 JOIN CHANNEL 1", url="https://t.me/+45fCzXzXxi0zMWI9"),
            types.InlineKeyboardButton("🚩 JOIN CHANNEL 2", url="https://t.me/+_RZ0gN9HU6xhZTRl"),
            types.InlineKeyboardButton("✅ VERIFY MY REQUEST", callback_data="v_now")
        )
        bot.send_message(message.chat.id, "⚔️ <b>WAR ZONE ACCESS LOCKED</b> ⚔️", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "v_now")
def verify(call):
    if check_status(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_btn(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "Pehle Request dalo!", show_alert=True)

def show_btn(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔥 START PREDICTION 🔥"))
    bot.send_message(chat_id, "✅ <b>VERIFICATION SUCCESS</b>\nClick below to start 1M Auto Prediction:", parse_mode="HTML", reply_markup=markup)

# --- THE AUTO ENGINE ---
@bot.message_handler(func=lambda m: m.text == "🔥 START PREDICTION 🔥")
def run_prediction(message):
    global stats
    stats = {"win": 0, "loss": 0, "count": 0}
    bot.send_message(message.chat.id, "🚀 <b>ADITYA PAPA ENGINE LIVE...</b>", parse_mode="HTML")

    while stats["count"] < 100:
        data = get_latest_data()
        if not data:
            time.sleep(10) # API Busy hone par wait karega
            continue

        next_p = int(data['period']) + 1
        prediction = random.choice(["🌕 BIG", "🌑 SMALL"])
        stats["count"] += 1

        msg = (
            f"⚔️ <b>ADITYA VIP ROUND: {stats['count']}/100</b> ⚔️\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔢 <b>PERIOD:</b> <code>{next_p}</code>\n"
            f"🎯 <b>PREDICTION: {prediction}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        bot.send_message(message.chat.id, msg, parse_mode="HTML")
        
        # 1-Minute Game Wait
        time.sleep(55) 

        res_data = get_latest_data()
        if res_data:
            actual = res_data['size']
            win_l = "✅ <b>WIN</b>" if prediction.split()[1] == actual else "❌ <b>LOSS</b>"
            if "WIN" in win_l: stats["win"] += 1
            else: stats["loss"] += 1
            bot.send_message(message.chat.id, f"📊 <b>RESULT: {actual}</b>\n💉 <b>STATUS: {win_l}</b>", parse_mode="HTML")
        
        time.sleep(5)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
    
