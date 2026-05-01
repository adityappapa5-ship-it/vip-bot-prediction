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
def home(): return "1M ENGINE ACTIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- CONFIG ---
API_TOKEN = '8216633914:AAEphghqpkKSTgvnWTD2ka95BlFwHTGRfyg'
CHANNELS = [-1003815161090, -1003973812867] 
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)
stats = {"win": 0, "loss": 0, "count": 0}

# --- UNSTOPPABLE API FETCH ---
def get_latest_data():
    # Har baar naya identity
    agents = [
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.036) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
    ]
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': random.choice(agents),
        'Origin': 'https://ar-lottery01.com',
        'Referer': 'https://ar-lottery01.com/'
    }
    
    try:
        # Request with session for better stability
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
    except Exception as e:
        print(f"Fetch Error: {e}")
    return None

# --- REQUEST BYPASS ---
def check_status(user_id):
    for channel in CHANNELS:
        try:
            # Join request bypass logic
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']: return False
        except: return True 
    return True

# --- FLOW: START -> VERIFY -> PREDICT ---
@bot.message_handler(commands=['start'])
def start(message):
    if check_status(message.from_user.id):
        show_ready_btn(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🚩 JOIN PRIVATE CHANNEL 1", url="https://t.me/+45fCzXzXxi0zMWI9"),
            types.InlineKeyboardButton("🚩 JOIN PRIVATE CHANNEL 2", url="https://t.me/+_RZ0gN9HU6xhZTRl"),
            types.InlineKeyboardButton("✅ VERIFY MY ACCESS", callback_data="final_verify")
        )
        bot.send_message(message.chat.id, "⚔️ <b>WAR ZONE ACCESS LOCKED</b> ⚔️\nJoin channels karke verify karo!", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "final_verify")
def verify(call):
    if check_status(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_ready_btn(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "Request dalo pehle!", show_alert=True)

def show_ready_btn(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔥 START PREDICTION 🔥"))
    bot.send_message(chat_id, "✅ <b>VERIFICATION SUCCESS</b>\nNiche wala button dabao 1M prediction ke liye:", parse_mode="HTML", reply_markup=markup)

# --- 1M AUTOMATIC LOOP ---
@bot.message_handler(func=lambda m: m.text == "🔥 START PREDICTION 🔥")
def start_engine(message):
    global stats
    stats = {"win": 0, "loss": 0, "count": 0}
    bot.send_message(message.chat.id, "🚀 <b>ADITYA PAPA 1M ENGINE LIVE...</b>", parse_mode="HTML")

    while stats["count"] < 100:
        data = get_latest_data()
        
        if not data:
            # Agar busy aaye toh chup-chap retry karega bina spam kiye
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
        
        # 1-Minute Timing Logic (52s Wait)
        time.sleep(52) 

        res_data = get_latest_data()
        if res_data:
            actual = res_data['size']
            win_loss = "✅ <b>WIN (AFEEM)</b>" if prediction.split()[1] == actual else "❌ <b>LOSS</b>"
            if "WIN" in win_loss: stats["win"] += 1
            else: stats["loss"] += 1

            bot.send_message(message.chat.id, f"📊 <b>RESULT: {actual}</b>\n💉 <b>STATUS: {win_loss}</b>", parse_mode="HTML")
        
        time.sleep(5) # Short gap before next round

    bot.send_message(message.chat.id, f"🏁 <b>100 ROUNDS DONE!</b>\nWins: {stats['win']} | Loss: {stats['loss']}")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
