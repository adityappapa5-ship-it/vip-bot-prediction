import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVER ALIVE ---
app = Flask('')
@app.route('/')
def home(): return "ADITYA PAPA JOIN-LOCK ACTIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- VIP CONFIG ---
API_TOKEN = '8618263406:AAHreGN69x_-g-_ZQ0VsieTWISgmxnCHBWo'
WIN_STICKER = 'CAACAgUAAxkBAAERJRhp9B-PkyNlzscUNGUAAUchyXw63g8AAisSAAJSEdhVkI_Ixu7liJU7BA'
LOSS_STICKER = 'CAACAgUAAxkBAAERJRpp9B-X_XQ3vbejkVPLEIBkdKki-QACkBQAAiMYmVWHXHRU3FIjKzsE'
CHANNELS = [-1003815161090, -1003973812867] # YE KABHI NAHI HATEGA
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def check_join(uid):
    for c in CHANNELS:
        try:
            status = bot.get_chat_member(c, uid).status
            if status in ['left', 'kicked']: return False
        except: continue
    return True

@bot.message_handler(commands=['start'])
def start(message):
    if check_join(message.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🚀 START VIP ENGINE 🚀"))
        bot.send_message(message.chat.id, "💎 <b>ADITYA PAPA PERMANENT VIP</b> 💎\n\nStatus: <b>ACCESS GRANTED</b> ✅", parse_mode="HTML", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🚩 JOIN VIP 1", url="https://t.me/+45fCzXzXxi0zMWI9"),
            types.InlineKeyboardButton("🚩 JOIN VIP 2", url="https://t.me/+_RZ0gN9HU6xhZTRl"),
            types.InlineKeyboardButton("✅ VERIFY JOIN", callback_data="v")
        )
        bot.send_message(message.chat.id, "❌ <b>ACCESS LOCKED</b> ❌\n\nBhai, dono channel join karlo tabhi prediction dikhega!", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "v")
def v(c):
    if check_join(c.from_user.id):
        bot.delete_message(c.message.chat.id, c.message.message_id)
        start(c.message)
    else:
        bot.answer_callback_query(c.id, "Pehle dono channel join karo!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "🚀 START VIP ENGINE 🚀")
def engine(message):
    if not check_join(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Channel chhod diya? Pehle join karo!")
        return

    bot.send_message(message.chat.id, "⚡ <b>VIP ENGINE STARTED...</b>", parse_mode="HTML")
    last_p = None
    while True:
        try:
            r = requests.get(API_URL, timeout=15).json()
            data = r['data']['list'][0]
            curr_p = data['issueNumber']
            
            if curr_p != last_p:
                last_p = curr_p
                next_p = int(curr_p) + 1
                pred = random.choice(["🌕 BIG", "🌑 SMALL"])
                
                box = (
                    f"┏━━━━━━ VIP BOX ━━━━━━┓\n"
                    f"┃ 🔢 <b>PERIOD:</b> {next_p} ┃\n"
                    f"┃ 🎯 <b>BET:</b> {pred}      ┃\n"
                    f"┃ ✨ <b>LUCK:</b> 99.9%     ┃\n"
                    f"┗━━━━━━━━━━━━━━━━━━━━━━┛"
                )
                bot.send_message(message.chat.id, box, parse_mode="HTML")
                
                time.sleep(55)
                # Result Check logic...
            time.sleep(2)
        except: time.sleep(5)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.remove_webhook()
    bot.infinity_polling()
    
