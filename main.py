import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVER KEEP-ALIVE ---
app = Flask('')
@app.route('/')
def home(): return "ADITYA PAPA VIP IS LIVE 24/7"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- CONFIG ---
API_TOKEN = '8618263406:AAHreGN69x_-g-_ZQ0VsieTWISgmxnCHBWo'
WIN_STICKER = 'CAACAgUAAxkBAAERJRhp9B-PkyNlzscUNGUAAUchyXw63g8AAisSAAJSEdhVkI_Ixu7liJU7BA'
LOSS_STICKER = 'CAACAgUAAxkBAAERJRpp9B-X_XQ3vbejkVPLEIBkdKki-QACkBQAAiMYmVWHXHRU3FIjKzsE'
CHANNELS = [-1003815161090, -1003973812867]
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def get_latest_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(API_URL, headers=headers, timeout=10)
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
        bot.send_message(message.chat.id, "💎 <b>ADITYA PAPA CLOUD PERMANENT</b> 💎\n24/7 Mode Active!", parse_mode="HTML", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🚩 JOIN VIP", url="https://t.me/+45fCzXzXxi0zMWI9"), types.InlineKeyboardButton("✅ VERIFY", callback_data="v"))
        bot.send_message(message.chat.id, "❌ <b>JOIN CHANNELS</b>", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "v")
def v(c):
    if check_status(c.from_user.id): start(c.message)
    else: bot.answer_callback_query(c.id, "Pehle join karo!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "🚀 START VIP ENGINE 🚀")
def engine(message):
    bot.send_message(message.chat.id, "🔥 <b>GHATAK ENGINE STARTED (UNLIMITED)</b>", parse_mode="HTML")
    last_p = None
    win_count = 0
    loss_count = 0
    total = 0

    while total < 100:
        data = get_latest_data()
        if not data:
            time.sleep(2)
            continue
        
        if data['period'] != last_p:
            last_p = data['period']
            next_p = int(last_p) + 1
            total += 1
            pred = random.choice(["🌕 BIG", "🌑 SMALL"])
            
            bot.send_message(message.chat.id, f"👑 <b>ROUND: {total}/100</b>\n🔢 <b>LIVE PERIOD: {next_p}</b>\n🎯 <b>BET: {pred}</b>", parse_mode="HTML")
            
            time.sleep(55) # Live sync wait
            
            res = get_latest_data()
            if res and int(res['period']) == next_p:
                if pred.split()[1] == res['size']:
                    bot.send_sticker(message.chat.id, WIN_STICKER)
                    win_count += 1
                else:
                    bot.send_sticker(message.chat.id, LOSS_STICKER)
                    loss_count += 1
                time.sleep(1)
                bot.send_message(message.chat.id, f"📊 <b>RESULT: {res['size']}</b>\n💉 <b>W: {win_count} | L: {loss_count}</b>", parse_mode="HTML")
        time.sleep(2)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
    
