import requests
import telebot
from telebot import types
import time
import os
from flask import Flask
from threading import Thread

# --- SERVER FOR RAILWAY ---
app = Flask('')
@app.route('/')
def home(): return "AFEEM HACK ACTIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- BOT CONFIG ---
API_TOKEN = '8753644667:AAFONCU_7vr313gJ2bIPpspviw6RqAn9p0w'
CHANNELS = ['@ADITYAVIPXPAPA', '@ADITYAVIPWIN']
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)
GAMES = ["RAJA GAME", "JALVA", "DU WIN", "DM WIN", "55 CLUB", "91 CLUB", "LOTTERY 7"]

# --- API DATA FETCH ---
def get_latest_data():
    try:
        response = requests.get(API_URL, timeout=10).json()
        latest = response['data']['list'][0]
        return {
            "period": latest['issueNumber'],
            "result": latest['colour'], # 'red', 'green', ya 'red_green'
            "number": latest['number']
        }
    except:
        return None

# --- MEMBER CHECK ---
def check_status(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status in ['left', 'kicked']: return False
        except: return False
    return True

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def start(message):
    if check_status(message.from_user.id):
        # Chat mein Game Select karne ke liye Button Menu
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(*[types.KeyboardButton(g) for g in GAMES])
        bot.send_message(message.chat.id, 
            "<b>🔥 ADITYA PAPA AFEEM HACK 🔥</b>\n\n"
            "<i>Select your game from the chat menu below:</i>", 
            parse_mode="HTML", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🚩 JOIN WAR ZONE 1", url="https://t.me/ADITYAVIPXPAPA"),
            types.InlineKeyboardButton("🚩 JOIN WAR ZONE 2", url="https://t.me/ADITYAVIPWIN"),
            types.InlineKeyboardButton("✅ VERIFY ACCESS", callback_data="verify")
        )
        bot.send_message(message.chat.id, "❌ <b>ACCESS DENIED!</b>\nJoin Both Channels First!", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    if check_status(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "Join kar pehle madrachod!", show_alert=True)

# --- PREDICTION LOGIC (WAIT & RESULT) ---
@bot.message_handler(func=lambda m: m.text in GAMES)
def handle_game(message):
    game = message.text
    bot.send_message(message.chat.id, f"💉 <b>{game} Injecting...</b>", parse_mode="HTML")
    
    # 1. Get Current Data
    data = get_latest_data()
    if not data:
        bot.send_message(message.chat.id, "⚠️ API Error! Try again later.")
        return

    current_period = data['period']
    next_period = int(current_period) + 1
    prediction = random.choice(["🔴 RED", "🟢 GREEN"])

    # 2. Show Prediction
    msg = bot.send_message(message.chat.id, 
        f"⚔️ <b>{game} WAR PREDICTION</b> ⚔️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔢 <b>PERIOD:</b> <code>{next_period}</code>\n"
        f"🎯 <b>PREDICTION: {prediction}</b>\n"
        f"⏳ <b>STATUS:</b> <i>Waiting for result...</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━", parse_mode="HTML")

    # 3. Wait for Period to Finish (30 Sec Game)
    time.sleep(30) 

    # 4. Fetch Result and Compare
    new_data = get_latest_data()
    actual_color = new_data['result'].upper()
    
    status_msg = "✅ <b>WINNER (AFEEM)</b>" if prediction.split()[1] in actual_color else "❌ <b>LOSS</b>"

    final_text = (
        f"⚔️ <b>{game} RESULT</b> ⚔️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔢 <b>PERIOD:</b> <code>{next_period}</code>\n"
        f"🎯 <b>RESULT:</b> {actual_color}\n"
        f"💉 <b>STATUS:</b> {status_msg}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🚀 <i>Next prediction starting...</i>"
    )
    bot.edit_message_text(final_text, message.chat.id, msg.message_id, parse_mode="HTML")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
