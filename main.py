import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVER FOR 24/7 ---
app = Flask('')
@app.route('/')
def home(): return "ADITYA TERMUX ENGINE LIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- CONFIG ---
API_TOKEN = '8618263406:AAHreGN69x_-g-_ZQ0VsieTWISgmxnCHBWo'
WIN_STICKER = 'CAACAgUAAxkBAAERJRhp9B-PkyNlzscUNGUAAUchyXw63g8AAisSAAJSEdhVkI_Ixu7liJU7BA'
LOSS_STICKER = 'CAACAgUAAxkBAAERJRpp9B-X_XQ3vbejkVPLEIBkdKki-QACkBQAAiMYmVWHXHRU3FIjKzsE'
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def get_data_cracked():
    """Termux-level Fast Bypass"""
    h = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
        'Origin': 'https://ar-lottery01.com'
    }
    try:
        r = requests.get(API_URL, headers=h, timeout=10)
        return r.json().get('data', {}).get('list', [])
    except: return None

@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🚀 START ADITYA VIP ENGINE 🚀"))
    bot.send_message(m.chat.id, "☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n\nStatus: <b>TERMUX MODE ACTIVE</b> ✅", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🚀 START ADITYA VIP ENGINE 🚀")
def engine(message):
    # Termux jaisa feel dene ke liye initial message
    msg = bot.send_message(message.chat.id, "<b>$ initializing crack...</b>", parse_mode="HTML")
    time.sleep(1)
    bot.edit_message_text("<b>$ bypassing wingo security...</b>", message.chat.id, msg.message_id, parse_mode="HTML")
    time.sleep(1)
    bot.edit_message_text("<b>$ connection established!</b>", message.chat.id, msg.message_id, parse_mode="HTML")
    
    last_p = None
    while True:
        try:
            history = get_data_cracked()
            if history:
                curr_p = history[0]['issueNumber']
                if curr_p != last_p:
                    last_p = curr_p
                    next_p = int(curr_p) + 1
                    
                    # Calculation
                    n = int(history[0]['number'])
                    pred = "🌕 𝗕𝗜𝗚" if n < 5 else "🌑 𝗦𝗠𝗔𝗟𝗟"
                    
                    # Direct Box
                    box = (
                        f"☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n"
                        f"━━━━━━━━━━━━━━━━━━━\n"
                        f"🔢 <b>PERIOD:</b> <code>{next_p}</code>\n"
                        f"🎯 <b>PREDICT:</b> <b>{pred}</b>\n"
                        f"━━━━━━━━━━━━━━━━━━━"
                    )
                    bot.send_message(message.chat.id, box, parse_mode="HTML")
                    
                    # Wait for Sticker
                    time.sleep(55)
                    new_data = get_data_cracked()
                    if new_data and int(new_data[0]['issueNumber']) == next_p:
                        actual = "BIG" if int(new_data[0]['number']) >= 5 else "SMALL"
                        bot.send_sticker(message.chat.id, WIN_STICKER if pred.split()[1] == actual else LOSS_STICKER)
            time.sleep(5)
        except: time.sleep(10)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
    
