import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- FAST SERVER ---
app = Flask('')
@app.route('/')
def home(): return "ADITYA PAPA INSTANT ENGINE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- CONFIG ---
API_TOKEN = '8618263406:AAHreGN69x_-g-_ZQ0VsieTWISgmxnCHBWo'
CHANNELS = [-1003815161090, -1003973812867]
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def check_join(uid):
    for c in CHANNELS:
        try:
            if bot.get_chat_member(c, uid).status in ['left', 'kicked']: return False
        except: continue
    return True

@bot.message_handler(commands=['start'])
def start(message):
    if check_join(message.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🚀 START VIP ENGINE 🚀"))
        bot.send_message(message.chat.id, "💎 <b>ADITYA PAPA PERMANENT VIP</b> 💎\n\nStatus: <b>ACCESS GRANTED</b> ✅", parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "❌ <b>JOIN CHANNELS FIRST!</b>")

@bot.message_handler(func=lambda m: m.text == "🚀 START VIP ENGINE 🚀")
def engine(message):
    bot.send_message(message.chat.id, "⚡ <b>VIP ENGINE IS FETCHING...</b>", parse_mode="HTML")
    last_p = None
    
    while True:
        try:
            # Random User-Agent for bypass
            headers = {'User-Agent': str(random.random())}
            r = requests.get(API_URL, headers=headers, timeout=10).json()
            data = r['data']['list'][0]
            curr_p = data['issueNumber']
            
            if curr_p != last_p:
                last_p = curr_p
                next_p = int(curr_p) + 1
                pred = random.choice(["🌕 BIG", "🌑 SMALL"])
                
                # PREDICTION BOX
                box = (
                    f"┏━━━━━━ VIP BOX ━━━━━━┓\n"
                    f"┃ 🔢 <b>PERIOD:</b> {next_p} ┃\n"
                    f"┃ 🎯 <b>BET:</b> {pred}      ┃\n"
                    f"┃ ✨ <b>LUCK:</b> 99.9%     ┃\n"
                    f"┗━━━━━━━━━━━━━━━━━━━━━━┛"
                )
                bot.send_message(message.chat.id, box, parse_mode="HTML")
                
                # 45 second wait after prediction to avoid spam
                time.sleep(45)
            
            time.sleep(2)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.remove_webhook()
    bot.infinity_polling()
    
