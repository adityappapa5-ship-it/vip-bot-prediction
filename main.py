import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- CLOUD SERVER (TAKI BAND NA HO) ---
app = Flask('')
@app.route('/')
def home(): return "BOT IS ALIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- VIP CONFIG ---
API_TOKEN = '8618263406:AAHreGN69x_-g-_ZQ0VsieTWISgmxnCHBWo'
WIN_STICKER = 'CAACAgUAAxkBAAERJRhp9B-PkyNlzscUNGUAAUchyXw63g8AAisSAAJSEdhVkI_Ixu7liJU7BA'
LOSS_STICKER = 'CAACAgUAAxkBAAERJRpp9B-X_XQ3vbejkVPLEIBkdKki-QACkBQAAiMYmVWHXHRU3FIjKzsE'
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def get_latest_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(API_URL, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()['data']['list'][0]
            return {"period": data['issueNumber'], "size": "BIG" if int(data['number']) >= 5 else "SMALL"}
    except: return None

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔥 START UNSTOPPABLE VIP 🔥"))
    bot.send_message(message.chat.id, "💎 <b>ADITYA PAPA CLOUD ENGINE</b> 💎\nStatus: 24/7 Online Active", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🔥 START UNSTOPPABLE VIP 🔥")
def engine(message):
    bot.send_message(message.chat.id, "🚀 <b>PREDICTION STARTING FOR NEXT PERIOD...</b>", parse_mode="HTML")
    while True:
        data = get_latest_data()
        if not data:
            time.sleep(2)
            continue
        
        # ZERO DELAY LOGIC: Agle period ki prediction pahle hi dena
        current_p = int(data['period'])
        next_p = current_p + 1 
        pred = random.choice(["🌕 BIG", "🌑 SMALL"])
        
        bot.send_message(message.chat.id, f"👑 <b>NEXT PERIOD: {next_p}</b>\n🎯 <b>BET: {pred}</b>\n━━━━━━━━━━━━━\n<i>Wait for result...</i>", parse_mode="HTML")
        
        # Wait for period to end (approx 50s)
        time.sleep(50)
        
        # Result Fetching
        new_data = get_latest_data()
        if new_data and int(new_data['period']) == next_p:
            if pred.split()[1] == new_data['size']:
                bot.send_sticker(message.chat.id, WIN_STICKER)
            else:
                bot.send_sticker(message.chat.id, LOSS_STICKER)
            
            time.sleep(1)
            bot.send_message(message.chat.id, f"📊 <b>PERIOD {next_p} RESULT: {new_data['size']}</b>", parse_mode="HTML")
        
        time.sleep(5) # Gap before next cycle

if __name__ == "__main__":
    Thread(target=run).start() # Flask server chalu karega
    bot.infinity_polling()
    
