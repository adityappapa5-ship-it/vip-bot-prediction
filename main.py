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
def home(): return "BIG-SMALL ENGINE LIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- CONFIG ---
API_TOKEN = '8216633914:AAEphghqpkKSTgvnWTD2ka95BlFwHTGRfyg'
CHANNELS = [-1003815161090, -1003973812867] 
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)
stats = {"win": 0, "loss": 0, "count": 0}

def get_latest_data():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(API_URL, timeout=10, headers=headers).json()
        latest = response['data']['list'][0]
        return {
            "period": latest['issueNumber'],
            "size": "BIG" if int(latest['number']) >= 5 else "SMALL"
        }
    except: return None

def check_status(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status in ['left', 'kicked']: return False
        except: return False
    return True

# --- STEP 1: JOIN & VERIFY ---
@bot.message_handler(commands=['start'])
def start(message):
    if check_status(message.from_user.id):
        show_start_btn(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🚩 JOIN CHANNEL 1", url="https://t.me/+45fCzXzXxi0zMWI9"),
            types.InlineKeyboardButton("🚩 JOIN CHANNEL 2", url="https://t.me/+_RZ0gN9HU6xhZTRl"),
            types.InlineKeyboardButton("✅ VERIFY ACCESS", callback_data="verify_now")
        )
        bot.send_message(message.chat.id, "⚔️ <b>WAR ZONE LOCKED</b> ⚔️\n\nJoin both private channels to start hacking!", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify_now")
def verify(call):
    if check_status(call.from_user.id):
        bot.answer_callback_query(call.id, "Verified!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_start_btn(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "Join kar pehle madrachod!", show_alert=True)

def show_start_btn(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔥 START PREDICTION 🔥"))
    bot.send_message(chat_id, "💉 <b>SYSTEM READY</b> 💉\nClick the button below for 100 Round Auto Prediction (Big/Small):", parse_mode="HTML", reply_markup=markup)

# --- STEP 2: AUTO BIG/SMALL LOOP ---
@bot.message_handler(func=lambda m: m.text == "🔥 START PREDICTION 🔥")
def auto_loop(message):
    bot.send_message(message.chat.id, "🚀 <b>ADITYA PAPA BIG/SMALL ENGINE STARTED...</b>", parse_mode="HTML")
    global stats
    stats = {"win": 0, "loss": 0, "count": 0}

    while stats["count"] < 100:
        data = get_latest_data()
        if not data:
            time.sleep(5)
            continue

        next_p = int(data['period']) + 1
        # Sirf Big aur Small ki prediction
        prediction = random.choice(["🌕 BIG", "🌑 SMALL"])
        stats["count"] += 1

        msg = (
            f"⚔️ <b>ADITYA VIP ROUND: {stats['count']}/100</b> ⚔️\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔢 <b>PERIOD:</b> <code>{next_p}</code>\n"
            f"🎯 <b>PREDICTION: {prediction}</b>\n"
            f"⏳ <b>STATUS:</b> Analyzing Server...\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        bot.send_message(message.chat.id, msg, parse_mode="HTML")
        
        time.sleep(35) # WinGo 30S Wait

        res_data = get_latest_data()
        if res_data:
            actual = res_data['size']
            if prediction.split()[1] == actual:
                stats["win"] += 1
                res_icon = "✅ WIN"
            else:
                stats["loss"] += 1
                res_icon = "❌ LOSS"

            bot.send_message(message.chat.id, f"📊 <b>RESULT {next_p}:</b> {actual}\n💉 <b>STATUS:</b> {res_icon}", parse_mode="HTML")
        
        time.sleep(5)

    # FINAL REPORT
    report = (
        f"🏁 <b>100 ROUNDS FINISHED</b> 🏁\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>ADITYA PAPA VIP</b>\n"
        f"💰 <b>TOTAL WIN:</b> {stats['win']}\n"
        f"💀 <b>TOTAL LOSS:</b> {stats['loss']}\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, report, parse_mode="HTML")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
