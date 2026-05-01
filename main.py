import requests
import telebot
from telebot import types
import time
import os
import random
from flask import Flask
from threading import Thread

# --- SERVER KEEP ALIVE ---
app = Flask('')
@app.route('/')
def home(): return "API SERVER CONNECTED"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- CONFIG ---
API_TOKEN = '8216633914:AAEphghqpkKSTgvnWTD2ka95BlFwHTGRfyg'
# Dono Private Channel IDs
CHANNELS = [-1003815161090, -1003973812867] 
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)
GAMES = ["RAJA GAME", "JALVA", "DU WIN", "DM WIN", "55 CLUB", "91 CLUB", "LOTTERY 7"]

# --- API REAL CONNECTION ---
def get_latest_data():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(API_URL, timeout=10, headers=headers).json()
        if response and 'data' in response:
            latest = response['data']['list'][0]
            return {
                "period": latest['issueNumber'],
                "result_color": str(latest['colour']).upper(),
                "result_size": "BIG" if int(latest['number']) >= 5 else "SMALL"
            }
    except Exception as e:
        print(f"Server Error: {e}")
        return None

# --- MEMBER CHECK ---
def check_status(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status in ['left', 'kicked']: return False
        except: return False
    return True

# --- START FLOW ---
@bot.message_handler(commands=['start'])
def start(message):
    if check_status(message.from_user.id):
        show_game_menu(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        # TERE NAYE PRIVATE LINKS
        markup.add(
            types.InlineKeyboardButton("🚩 JOIN FIRST CHANNEL", url="https://t.me/+45fCzXzXxi0zMWI9"),
            types.InlineKeyboardButton("🚩 JOIN SECOND CHANNEL", url="https://t.me/+IPE8r37yMspjYjQ91"),
            types.InlineKeyboardButton("✅ VERIFY MY ACCESS", callback_data="verify")
        )
        bot.send_message(message.chat.id, "❌ <b>ACCESS DENIED!</b>\n\nBhai, dono private channels join karo tabhi prediction khulega!", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    if check_status(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_game_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "Join Both Channels First!", show_alert=True)

def show_game_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(g) for g in GAMES])
    bot.send_message(chat_id, "💉 <b>AFEEM VIP START</b> 💉\n\nSelect game target from keyboard:", parse_mode="HTML", reply_markup=markup)

# --- PREDICTION FLOW ---
@bot.message_handler(func=lambda m: m.text in GAMES)
def game_target(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔴 RED vs GREEN 🟢", callback_data=f"x_{message.text}_rg"),
               types.InlineKeyboardButton("🌕 BIG vs SMALL 🌑", callback_data=f"x_{message.text}_bs"))
    bot.send_message(message.chat.id, f"🎯 <b>TARGET: {message.text}</b>\nSelect Hack Mode:", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("x_"))
def handle_hack(call):
    _, game, mode = call.data.split("_")
    data = get_latest_data()
    
    if not data:
        bot.answer_callback_query(call.id, "⚠️ API Server Busy! Waiting for signal...")
        return

    next_p = int(data['period']) + 1
    pred = random.choice(["🔴 RED", "🟢 GREEN"]) if mode == "rg" else random.choice(["🌕 BIG", "🌑 SMALL"])

    bot.edit_message_text(
        f"⚔️ <b>{game} HACK LIVE</b> ⚔️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔢 <b>PERIOD:</b> <code>{next_p}</code>\n"
        f"🎯 <b>PREDICTION: {pred}</b>\n"
        f"⏳ <b>STATUS:</b> <i>Waiting for Result...</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━", 
        call.message.chat.id, call.message.message_id, parse_mode="HTML")

    time.sleep(30) # Wait for Wingo 30s

    new_data = get_latest_data()
    if new_data:
        actual = new_data['result_color'] if mode == "rg" else new_data['result_size']
        win_status = "✅ <b>WINNER (AFEEM)</b>" if pred.split()[1] in actual else "❌ <b>LOSS</b>"
    else:
        actual, win_status = "TIMEOUT", "RE-SCANNING..."

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 NEXT VIP ATTACK", callback_data=call.data))

    bot.edit_message_text(
        f"⚔️ <b>{game} ATTACK RESULT</b> ⚔️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔢 <b>PERIOD:</b> <code>{next_p}</code>\n"
        f"🎯 <b>RESULT:</b> {actual}\n"
        f"💉 <b>STATUS:</b> {win_status}\n"
        f"━━━━━━━━━━━━━━━━━━━━", 
        call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
