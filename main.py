import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- CLOUD KEEP-ALIVE (Railway/Koyeb/Render ke liye) ---
app = Flask('')
@app.route('/')
def home(): return "ADITYA PAPA BOT IS ONLINE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- VIP CONFIG ---
API_TOKEN = '8618263406:AAHreGN69x_-g-_ZQ0VsieTWISgmxnCHBWo'
WIN_STICKER = 'CAACAgUAAxkBAAERJRhp9B-PkyNlzscUNGUAAUchyXw63g8AAisSAAJSEdhVkI_Ixu7liJU7BA'
LOSS_STICKER = 'CAACAgUAAxkBAAERJRpp9B-X_XQ3vbejkVPLEIBkdKki-QACkBQAAiMYmVWHXHRU3FIjKzsE'
CHANNELS = [-1003815161090, -1003973812867]
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def get_latest_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    try:
        # Timeout 15s rakha hai taaki cloud pe delay na ho
        r = requests.get(API_URL, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()['data']['list'][0]
            return {"period": data['issueNumber'], "size": "BIG" if int(data['number']) >= 5 else "SMALL"}
    except Exception as e:
        print(f"Fetch Error: {e}")
        return None

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
        bot.send_message(message.chat.id, "💎 <b>CLOUD PERMANENT ACTIVE</b> 💎\n24/7 Mode Ready!", parse_mode="HTML", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🚩 JOIN VIP", url="https://t.me/+45fCzXzXxi0zMWI9"), types.InlineKeyboardButton("✅ VERIFY", callback_data="v"))
        bot.send_message(message.chat.id, "❌ <b>ACCESS LOCKED</b>\nJoin and Verify first!", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🚀 START VIP ENGINE 🚀")
def engine(message):
    bot.send_message(message.chat.id, "🔥 <b>GHATAK ENGINE STARTED...</b>", parse_mode="HTML")
    last_p = None
    
    while True: # Unlimited Loop
        data = get_latest_data()
        if not data:
            time.sleep(5)
            continue
        
        current_p = data['period']
        if current_p != last_p:
            last_p = current_p
            next_p = int(current_p) + 1
            pred = random.choice(["🌕 BIG", "🌑 SMALL"])
            
            bot.send_message(message.chat.id, f"👑 <b>NEXT PERIOD: {next_p}</b>\n🎯 <b>BET: {pred}</b>\n━━━━━━━━━━━━━", parse_mode="HTML")
            
            # Wait for Result (1M Game logic)
            time.sleep(55) 
            
            res = get_latest_data()
            if res and int(res['period']) == next_p:
                if pred.split()[1] == res['size']:
                    bot.send_sticker(message.chat.id, WIN_STICKER)
                    txt = "✅ <b>WIN (AFEEM)</b>"
                else:
                    bot.send_sticker(message.chat.id, LOSS_STICKER)
                    txt = "❌ <b>LOSS</b>"
                
                time.sleep(1)
                bot.send_message(message.chat.id, f"📊 <b>RESULT: {res['size']}</b>\n💉 <b>{txt}</b>", parse_mode="HTML")
        
        time.sleep(2) # CPU pe load kam karne ke liye

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
    
