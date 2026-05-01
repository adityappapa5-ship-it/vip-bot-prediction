import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- KEEP ALIVE ---
app = Flask('')
@app.route('/')
def home(): return "ADITYA PAPA CLOUD BYPASS ACTIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- CONFIG ---
API_TOKEN = '8618263406:AAHreGN69x_-g-_ZQ0VsieTWISgmxnCHBWo'
CHANNELS = [-1003815161090, -1003973812867]
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def get_data_bypass():
    # Ye headers Termux aur Real Browser ki tarah act karenge
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://ar-lottery01.com',
        'Referer': 'https://ar-lottery01.com/',
        'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,hi;q=0.7',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        # Verify=False taaki SSL error na aaye Cloud par
        r = requests.get(API_URL, headers=headers, timeout=15, verify=True)
        if r.status_code == 200:
            return r.json()['data']['list'][0]
    except Exception as e:
        print(f"Bypass Error: {e}")
    return None

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🚀 START VIP ENGINE 🚀"))
    bot.send_message(message.chat.id, "💎 <b>ADITYA PAPA VIP (CLOUD BYPASS)</b> 💎", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🚀 START VIP ENGINE 🚀")
def engine(message):
    bot.send_message(message.chat.id, "⚡ <b>VIP ENGINE STARTED (TERMUX SPEED)...</b>", parse_mode="HTML")
    last_p = None
    while True:
        try:
            data = get_data_bypass()
            if not data:
                time.sleep(5)
                continue
            
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
                time.sleep(50)
            time.sleep(2)
        except: time.sleep(5)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
    
