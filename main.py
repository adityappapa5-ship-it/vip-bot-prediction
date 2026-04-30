import requests
import telebot
from telebot import types
import random
import time
import os
from flask import Flask
from threading import Thread

# --- SERVER ---
app = Flask('')
@app.route('/')
def home(): return "WAR ZONE ACTIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive():
    Thread(target=run).start()

# --- BOT CONFIG ---
API_TOKEN = '8753644667:AAFONCU_7vr313gJ2bIPpspviw6RqAn9p0w'
# PUBLIC CHANNELS (Direct Usernames)
CHANNELS = ['@ADITYAVIPXPAPA', '@ADITYAVIPWIN']
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)
GAMES = ["RAJA GAME", "JALVA", "DU WIN", "DM WIN", "55 CLUB", "91 CLUB", "LOTTERY 7"]

# --- DESIGN ---
WAR_LINE = "⚔️ ━━━━━━━━━━━━━━━━━━━━ ⚔️"
RED_WAR = "🛑 ━━━━━ VS ━━━━━ 🟢"

# --- MEMBER CHECK (PUBLIC METHOD) ---
def check_status(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status in ['left', 'kicked']:
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    return True

def get_api_period():
    try:
        data = requests.get(API_URL, timeout=5).json()
        return data['data']['list'][0]['issueNumber']
    except: return "2026043001"

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    if check_status(message.from_user.id):
        show_game_menu(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🚩 JOIN WAR ZONE 1", url="https://t.me/ADITYAVIPXPAPA"),
            types.InlineKeyboardButton("🚩 JOIN WAR ZONE 2", url="https://t.me/ADITYAVIPWIN"),
            types.InlineKeyboardButton("🔥 VERIFY MY POWER 🔥", callback_data="verify_join")
        )
        text = (
            f"{RED_WAR}\n"
            "       🚨 <b>SYSTEM LOCKED</b> 🚨\n"
            f"{RED_WAR}\n\n"
            "🔴 <b>Bhai, Public Channels join karo tabhi access milega!</b>"
        )
        bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "verify_join":
        if check_status(call.from_user.id):
            bot.answer_callback_query(call.id, "✅ Identity Confirmed!")
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_game_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ Join Kar Madrachod! System check fail.", show_alert=True)

    elif call.data.startswith("mode_"):
        game, m_type = call.data.split("_")[1], call.data.split("_")[2]
        bot.edit_message_text("💉 <b>Hacking Mainframe...</b>", call.message.chat.id, call.message.message_id, parse_mode="HTML")
        time.sleep(1)
        
        period = get_api_period()
        next_p = int(period) + 1
        
        if m_type == "redgreen":
            res = random.choice(["🔴 RED (WINNER) 🔴", "🟢 GREEN (WINNER) 🟢"])
            war_info = "🔥 BLOODY BATTLE 🔥"
        else:
            res = random.choice(["🌕 BIG 🌕", "🌑 SMALL 🌑"])
            war_info = "💰 MONEY WAR 💰"

        text = (
            f"⚔️ <b>{game} RED vs GREEN</b> ⚔️\n"
            f"{WAR_LINE}\n"
            f"👿 <b>WAR TYPE:</b> {war_info}\n"
            f"🔢 <b>PERIOD:</b> <code>{next_p}</code>\n"
            f"🎯 <b>RESULT: {res}</b>\n"
            f"🩸 <b>STATUS:</b> DEADLY ACCURATE\n"
            f"{WAR_LINE}\n"
            f"💀 <i>Next Attack in 30s...</i>"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 NEXT WAR ATTACK", callback_data=call.data))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

def show_game_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(g) for g in GAMES])
    bot.send_message(chat_id, 
        f"🩸 <b>ADITYA PAPA WAR DASHBOARD</b> 🩸\n"
        f"{RED_WAR}\n"
        "<b>Bhai, apna Shikaar select karo:</b>", 
        parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in GAMES)
def game_select(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔴 RED vs GREEN 🟢", callback_data=f"mode_{message.text}_redgreen"),
               types.InlineKeyboardButton("🌕 BIG vs SMALL 🌑", callback_data=f"mode_{message.text}_bigsmall"))
    bot.send_message(message.chat.id, f"🎯 <b>TARGET: {message.text}</b>\n\n<i>Mode Select Kar:</i>", parse_mode="HTML", reply_markup=markup)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
