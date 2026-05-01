import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- CLOUD SERVER (Bot ko 24/7 zinda rakhne ke liye) ---
app = Flask('')
@app.route('/')
def home(): return "ADITYA PAPA VIP ENGINE IS ONLINE 24/7"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- CONFIG ---
API_TOKEN = '8618263406:AAHreGN69x_-g-_ZQ0VsieTWISgmxnCHBWo'
WIN_STICKER = 'CAACAgUAAxkBAAERJRhp9B-PkyNlzscUNGUAAUchyXw63g8AAisSAAJSEdhVkI_Ixu7liJU7BA'
LOSS_STICKER = 'CAACAgUAAxkBAAERJRpp9B-X_XQ3vbejkVPLEIBkdKki-QACkBQAAiMYmVWHXHRU3FIjKzsE'
CHANNELS = [-1003815161090, -1003973812867]
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def get_latest_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': 'https://ar-lottery01.com/'
    }
    try:
        r = requests.get(API_URL, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()['data']['list'][0]
            return {"period": data['issueNumber'], "size": "BIG" if int(data['number']) >= 5 else "SMALL"}
    except: return None

def check_status(user_id):
    for c in CHANNELS:
        try:
            if bot.get_chat_member(c, user_id).status in ['left', 'kicked']: return False
        except: return True
    return True

@bot.message_handler(commands=['start'])
def start(message):
    if check_status(message.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🚀 START VIP ENGINE 🚀"))
        bot.send_message(message.chat.id, "💎 <b>100% FIXED CLOUD ENGINE</b> 💎\nStatus: 24/7 Non-Stop Active", parse_mode="HTML", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🚩 JOIN CHANNEL 1", url="https://t.me/+45fCzXzXxi0zMWI9"),
            types.InlineKeyboardButton("🚩 JOIN CHANNEL 2", url="https://t.me/+_RZ0gN9HU6xhZTRl"),
            types.InlineKeyboardButton("✅ VERIFY JOIN", callback_data="v")
        )
        bot.send_message(message.chat.id, "❌ <b>ACCESS LOCKED</b>\nBhai, join channels first!", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "v")
def v(c):
    if check_status(c.from_user.id):
        bot.delete_message(c.message.chat.id, c.message.message_id)
        start(c.message)
    else: bot.answer_callback_query(c.id, "Join karlo pehle!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "🚀 START VIP ENGINE 🚀")
def engine(message):
    bot.send_message(message.chat.id, "🔥 <b>GHATAK ENGINE INITIALIZED</b>", parse_mode="HTML")
    last_p = None
    
    while True:
        data = get_latest_data()
        if not data:
            time.sleep(3)
            continue
        
        current_p = data['period']
        if current_p != last_p:
            last_p = current_p
            next_p = int(current_p) + 1
            pred = random.choice(["🌕 BIG", "🌑 SMALL"])
            
            # Prediction turant jayegi bina delay ke
            bot.send_message(message.chat.id, f"👑 <b>NEXT PERIOD: {next_p}</b>\n🎯 <b>BET: {pred}</b>\n━━━━━━━━━━━━━", parse_mode="HTML")
            
            # Wait for Result (1M logic)
            time.sleep(54) 
            
            res = get_latest_data()
            if res and int(res['period']) == next_p:
                sticker = WIN_STICKER if pred.split()[1] == res['size'] else LOSS_STICKER
                bot.send_sticker(message.chat.id, sticker)
                time.sleep(1)
                bot.send_message(message.chat.id, f"📊 <b>RESULT: {res['size']}</b>", parse_mode="HTML")
        
        time.sleep(2)

if __name__ == "__main__":
    # Flask ko thread mein chalayenge taaki bot bhi chalta rahe
    Thread(target=run).start()
    bot.remove_webhook()
    bot.infinity_polling(timeout=60, long_polling_timeout=30)
