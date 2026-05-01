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
def home(): return "AFEEM BOT ACTIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- BOT CONFIG ---
API_TOKEN = '8216633914:AAEphghqpkKSTgvnWTD2ka95BlFwHTGRfyg'
# Dono Private Channel IDs
CHANNELS = [-1003815161090, -1003973812867] 
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

# --- API DATA FETCH ---
def get_latest_data():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(API_URL, timeout=10, headers=headers).json()
        if response and 'data' in response:
            latest = response['data']['list'][0]
            return {
                "period": latest['issueNumber'],
                "color": str(latest['colour']).upper(),
                "size": "BIG" if int(latest['number']) >= 5 else "SMALL"
            }
    except: return None

# --- MEMBER CHECK ---
def check_status(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status in ['left', 'kicked']: return False
        except: return False
    return True

# --- 1. START: CHANNEL JOIN OPTION ---
@bot.message_handler(commands=['start'])
def start(message):
    if check_status(message.from_user.id):
        show_start_prediction_button(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        # Tere Private Links
        markup.add(
            types.InlineKeyboardButton("🚩 JOIN PRIVATE CHANNEL 1", url="https://t.me/+45fCzXzXxi0zMWI9"),
            types.InlineKeyboardButton("🚩 JOIN PRIVATE CHANNEL 2", url="https://t.me/+_RZ0gN9HU6xhZTRl"),
            types.InlineKeyboardButton("✅ VERIFY JOIN REQUEST", callback_data="verify_user")
        )
        bot.send_message(message.chat.id, 
            "⚔️ <b>WAR ZONE ACCESS LOCKED</b> ⚔️\n\n"
            "<i>Bhai, pehle dono private channels join karo tabhi verification success hoga!</i>", 
            parse_mode="HTML", reply_markup=markup)

# --- 2. VERIFICATION HANDLER ---
@bot.callback_query_handler(func=lambda call: call.data == "verify_user")
def verify(call):
    if check_status(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Verified Successfully!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_start_prediction_button(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ Join kar pehle! Access Denied.", show_alert=True)

# --- 3. SHOW "START PREDICTION" BUTTON ---
def show_start_prediction_button(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔥 START PREDICTION 🔥"))
    bot.send_message(chat_id, 
        "💉 <b>VERIFICATION COMPLETE!</b> 💉\n\n"
        "Click the button below to start automatic predictions:", 
        parse_mode="HTML", reply_markup=markup)

# --- 4. AUTOMATIC PREDICTION ENGINE ---
@bot.message_handler(func=lambda m: m.text == "🔥 START PREDICTION 🔥")
def handle_auto_loop(message):
    bot.send_message(message.chat.id, "🚀 <b>ADITYA PAPA AUTOMATIC ENGINE STARTED...</b>", parse_mode="HTML")
    
    # Loop starts here
    while True:
        data = get_latest_data()
        if not data:
            time.sleep(5)
            continue

        next_p = int(data['period']) + 1
        pred_color = random.choice(["🔴 RED", "🟢 GREEN"])
        pred_size = random.choice(["🌕 BIG", "🌑 SMALL"])

        msg_text = (
            f"⚔️ <b>ADITYA VIP HACK</b> ⚔️\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔢 <b>NEXT PERIOD:</b> <code>{next_p}</code>\n"
            f"🎨 <b>COLOR:</b> {pred_color}\n"
            f"📏 <b>SIZE:</b> {pred_size}\n"
            f"💉 <b>STATUS:</b> SIGNAL ACTIVE\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⏳ <i>Result aane mein 30s baki...</i>"
        )
        
        # Send Prediction
        msg = bot.send_message(message.chat.id, msg_text, parse_mode="HTML")
        
        # WinGo 30S Wait + Buffer
        time.sleep(35) 

        # Result Fetch and Show
        res_data = get_latest_data()
        if res_data:
            actual_c = res_data['color']
            win_loss = "✅ <b>WIN (AFEEM)</b>" if pred_color.split()[1] in actual_c else "❌ <b>LOSS</b>"
            
            result_text = (
                f"📊 <b>PERIOD {next_p} RESULT</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🎯 <b>RESULT:</b> {actual_c}\n"
                f"💉 <b>STATUS:</b> {win_loss}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🔄 <i>Next Attack in 5s...</i>"
            )
            bot.send_message(message.chat.id, result_text, parse_mode="HTML")
        
        time.sleep(5) # Delay before next cycle

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
