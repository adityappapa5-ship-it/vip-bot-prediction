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
def home(): return "WAR ZONE ACTIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- BOT CONFIG ---
API_TOKEN = '8753644667:AAFONCU_7vr313gJ2bIPpspviw6RqAn9p0w'
CHANNELS = ['@ADITYAVIPXPAPA', '@ADITYAVIPWIN']
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)
GAMES = ["RAJA GAME", "JALVA", "DU WIN", "DM WIN", "55 CLUB", "91 CLUB", "LOTTERY 7"]

# --- API DATA ---
def get_latest_data():
    try:
        response = requests.get(API_URL, timeout=10).json()
        latest = response['data']['list'][0]
        return {
            "period": latest['issueNumber'],
            "result_color": latest['colour'].upper(),
            "result_size": "BIG" if int(latest['number']) >= 5 else "SMALL"
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

# --- 1. START & JOIN CHECK ---
@bot.message_handler(commands=['start'])
def start(message):
    if check_status(message.from_user.id):
        show_game_menu(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🚩 JOIN ADITYAVIPXPAPA", url="https://t.me/ADITYAVIPXPAPA"),
            types.InlineKeyboardButton("🚩 JOIN ADITYAVIPWIN", url="https://t.me/ADITYAVIPWIN"),
            types.InlineKeyboardButton("✅ VERIFY & ENTER CHAT", callback_data="verify")
        )
        bot.send_message(message.chat.id, 
            "⚔️ <b>WAR ZONE ACCESS LOCKED</b> ⚔️\n\n"
            "<i>Bhai, pehle dono channels join karo tabhi verification success hoga!</i>", 
            parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    if check_status(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_game_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "Abe Join Kar Pehle! System check fail.", show_alert=True)

# --- 2. GAME SELECTION MENU ---
def show_game_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(g) for g in GAMES])
    bot.send_message(chat_id, 
        "🩸 <b>ADITYA PAPA VIP CHAT</b> 🩸\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<b>Bhai, Chat mein se apna Game select karo:</b>", 
        parse_mode="HTML", reply_markup=markup)

# --- 3. MODE SELECTION ---
@bot.message_handler(func=lambda m: m.text in GAMES)
def game_select(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔴 RED vs GREEN 🟢", callback_data=f"mode_{message.text}_rg"),
               types.InlineKeyboardButton("🌕 BIG vs SMALL 🌑", callback_data=f"mode_{message.text}_bs"))
    bot.send_message(message.chat.id, f"🎯 <b>TARGET: {message.text}</b>\nSelect Prediction Mode:", parse_mode="HTML", reply_markup=markup)

# --- 4. PREDICTION & WAIT LOGIC ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("mode_"))
def handle_prediction(call):
    _, game, mode = call.data.split("_")
    
    # API Se Period Lena
    data = get_latest_data()
    if not data:
        bot.answer_callback_query(call.id, "API Error!")
        return

    next_period = int(data['period']) + 1
    pred = random.choice(["🔴 RED", "🟢 GREEN"]) if mode == "rg" else random.choice(["🌕 BIG", "🌑 SMALL"])

    bot.edit_message_text(
        f"⚔️ <b>{game} PREDICTION</b> ⚔️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔢 <b>PERIOD:</b> <code>{next_period}</code>\n"
        f"🎯 <b>PREDICTION: {pred}</b>\n\n"
        f"⏳ <b>STATUS:</b> <i>Waiting for Result (30s)...</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━", 
        call.message.chat.id, call.message.message_id, parse_mode="HTML")

    # Game khatam hone ka wait
    time.sleep(30)

    # Result Check
    new_data = get_latest_data()
    actual = new_data['result_color'] if mode == "rg" else new_data['result_size']
    
    win_loss = "✅ <b>WINNER (AFEEM)</b>" if pred.split()[1] in actual else "❌ <b>LOSS</b>"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 NEXT PREDICTION", callback_data=call.data))

    bot.edit_message_text(
        f"⚔️ <b>{game} WAR RESULT</b> ⚔️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔢 <b>PERIOD:</b> <code>{next_period}</code>\n"
        f"🎯 <b>RESULT:</b> {actual}\n"
        f"💉 <b>STATUS:</b> {win_loss}\n"
        f"━━━━━━━━━━━━━━━━━━━━", 
        call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

