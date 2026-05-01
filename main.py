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
def home(): return "AFEEM ENGINE V5 LIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- CONFIG ---
API_TOKEN = '8216633914:AAEphghqpkKSTgvnWTD2ka95BlFwHTGRfyg'
# Dono Private Channel IDs
CHANNELS = [-1003815161090, -1003973812867] 
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

# Stats for 100 Rounds
stats = {"win": 0, "loss": 0, "count": 0}

def get_latest_data():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        # WinGo 30S API Connection
        response = requests.get(API_URL, timeout=12, headers=headers).json()
        if response and 'data' in response and 'list' in response['data']:
            latest = response['data']['list'][0]
            return {
                "period": latest['issueNumber'],
                "size": "BIG" if int(latest['number']) >= 5 else "SMALL"
            }
    except Exception as e:
        print(f"API Error: {e}")
        return None

# --- REQUEST BYPASS LOGIC ---
def check_status(user_id):
    # Agar banda request bhi dal chuka hai, toh verify kar dega
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            # member, administrator, creator, ya restricted... sabko allow karega
            if status in ['left', 'kicked']: return False
        except: 
            # Agar bot admin hai aur banda request me hai, toh allow kar do
            return True
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
            types.InlineKeyboardButton("✅ VERIFY MY REQUEST", callback_data="verify_now")
        )
        bot.send_message(message.chat.id, "⚔️ <b>ACCESS LOCKED</b> ⚔️\n\nChannel join karo ya Request dalo, fir Verify dabao!", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify_now")
def verify(call):
    # Request dalne par bhi allow kar dega
    if check_status(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_start_btn(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "Request ya Join karo pehle!", show_alert=True)

def show_start_btn(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔥 START PREDICTION 🔥"))
    bot.send_message(chat_id, "💉 <b>VERIFICATION COMPLETE</b> 💉\nAb niche wala button dabao prediction ke liye:", parse_mode="HTML", reply_markup=markup)

# --- STEP 2: AUTO PREDICTION LOOP (BIG/SMALL ONLY) ---
@bot.message_handler(func=lambda m: m.text == "🔥 START PREDICTION 🔥")
def auto_loop(message):
    global stats
    stats = {"win": 0, "loss": 0, "count": 0}
    bot.send_message(message.chat.id, "🚀 <b>ADITYA PAPA ENGINE LIVE...</b>", parse_mode="HTML")

    while stats["count"] < 100:
        data = get_latest_data()
        if not data:
            bot.send_message(message.chat.id, "⚠️ <i>API Busy... Waiting 5s</i>", parse_mode="HTML")
            time.sleep(5)
            continue

        next_p = int(data['period']) + 1
        prediction = random.choice(["🌕 BIG", "🌑 SMALL"])
        stats["count"] += 1

        msg_text = (
            f"⚔️ <b>ROUND: {stats['count']}/100</b> ⚔️\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔢 <b>PERIOD:</b> <code>{next_p}</code>\n"
            f"🎯 <b>PREDICTION: {prediction}</b>\n"
            f"⏳ <b>STATUS:</b> WAITING FOR RESULT...\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        bot.send_message(message.chat.id, msg_text, parse_mode="HTML")
        
        # 30s Game + Buffer
        time.sleep(35) 

        res_data = get_latest_data()
        if res_data:
            actual = res_data['size']
            win_loss = "✅ <b>WIN (AFEEM)</b>" if prediction.split()[1] == actual else "❌ <b>LOSS</b>"
            if "WIN" in win_loss: stats["win"] += 1
            else: stats["loss"] += 1

            result_msg = (
                f"📊 <b>RESULT: {actual}</b>\n"
                f"💉 <b>STATUS: {win_loss}</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━"
            )
            bot.send_message(message.chat.id, result_msg, parse_mode="HTML")
        
        time.sleep(3) # Next round break

    # Final Summary Report
    bot.send_message(message.chat.id, f"🏁 <b>100 ROUNDS DONE!</b>\n\nTotal Wins: {stats['win']}\nTotal Loss: {stats['loss']}")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
