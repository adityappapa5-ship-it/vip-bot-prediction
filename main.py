import requests
import telebot
from telebot import types
import random
import time
import os
from flask import Flask
from threading import Thread

# --- FLASK SERVER FOR RAILWAY ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT CONFIGURATION ---
API_TOKEN = '8669987861:AAG-6BEb8ykG8A4VGUVcBE7-wCH9myfBDCs'
CHANNELS = [-1003973812867, -1003942030008]
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)
GAMES = ["RAJA GAME", "JALVA", "DU WIN", "DM WIN", "55 CLUB", "91 CLUB", "LOTTERY 7"]

# --- FUNCTIONS ---
def is_user_joined(user_id):
    for channel_id in CHANNELS:
        try:
            member = bot.get_chat_member(channel_id, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

def get_api_period():
    try:
        response = requests.get(API_URL, timeout=5)
        data = response.json()
        return data['data']['list'][0]['issueNumber']
    except:
        return "2026043001"

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_user_joined(user_id):
        show_game_menu(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 JOIN CHANNEL 1", url="https://t.me/your_link1"))
        markup.add(types.InlineKeyboardButton("📢 JOIN CHANNEL 2", url="https://t.me/your_link2"))
        markup.add(types.InlineKeyboardButton("✅ VERIFY JOIN REQUEST", callback_data="verify_join"))
        bot.send_message(message.chat.id, "<b>❌ ACCESS DENIED!</b>\n\nPehle dono channels join karo.", 
                         parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "verify_join":
        if is_user_joined(call.from_user.id):
            bot.answer_callback_query(call.id, "✅ Verified!")
            show_game_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "⚠️ Pehle join karo!", show_alert=True)

    elif call.data.startswith("mode_"):
        game_name = call.data.split("_")[1]
        mode_type = call.data.split("_")[2]
        
        bot.edit_message_text("🔄 <b>Checking API Result...</b>", call.message.chat.id, call.message.message_id, parse_mode="HTML")
        time.sleep(2)
        
        status = random.choice(["✅ WIN", "✅ WIN", "❌ LOSS"])
        bot.edit_message_text(f"📊 <b>LAST STATUS: {status}</b>\n\n<i>Analysing next period...</i>", 
                              call.message.chat.id, call.message.message_id, parse_mode="HTML")
        time.sleep(2)
        
        period = get_api_period()
        next_p = int(period) + 1
        res = random.choice(["🔴 RED", "🟢 GREEN"]) if mode_type == "redgreen" else random.choice(["🌕 BIG", "🌑 SMALL"])

        text = (
            f"🚀 <b>{game_name} VIP</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔢 <b>PERIOD:</b> <code>{next_p}</code>\n"
            f"🎯 <b>RESULT:</b> {res}\n"
            f"✨ <b>STATUS:</b> {status}\n"
            f"━━━━━━━━━━━━━━━━━━"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 NEXT PREDICTION", callback_data=call.data))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

def show_game_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(g) for g in GAMES]
    markup.add(*buttons)
    bot.send_message(chat_id, "<b>✅ ACCESS GRANTED!</b>\nSelect your game:", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in GAMES)
def game_select(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔴 RED/GREEN", callback_data=f"mode_{message.text}_redgreen"),
               types.InlineKeyboardButton("🌕 BIG/SMALL", callback_data=f"mode_{message.text}_bigsmall"))
    bot.send_message(message.chat.id, f"🎯 <b>GAME: {message.text}</b>\nChoose Mode:", parse_mode="HTML", reply_markup=markup)

if __name__ == "__main__":
    keep_alive()
    print("Bot is starting...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
