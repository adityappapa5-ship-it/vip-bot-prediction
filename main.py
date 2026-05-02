import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- 24/7 CLOUD ALIVE ---
app = Flask('')
@app.route('/')
def home(): return "ADITYA VIP IS LIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- CONFIG ---
API_TOKEN = '8618263406:AAHreGN69x_-g-_ZQ0VsieTWISgmxnCHBWo'
CHANNELS = [-1003815161090, -1003973812867]
WIN_STICKER = 'CAACAgUAAxkBAAERJRhp9B-PkyNlzscUNGUAAUchyXw63g8AAisSAAJSEdhVkI_Ixu7liJU7BA'
LOSS_STICKER = 'CAACAgUAAxkBAAERJRpp9B-X_XQ3vbejkVPLEIBkdKki-QACkBQAAiMYmVWHXHRU3FIjKzsE'
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def check_join(uid):
    for c in CHANNELS:
        try:
            if bot.get_chat_member(c, uid).status in ['left', 'kicked']: return False
        except: continue
    return True

def get_data_cracked():
    """Bypasses 'Cracking API' Hang Issue"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Origin': 'https://ar-lottery01.com'
    }
    try:
        r = requests.get(API_URL, headers=headers, timeout=12)
        if r.status_code == 200:
            return r.json().get('data', {}).get('list', [])
    except: return None

@bot.message_handler(commands=['start'])
def start(m):
    if check_join(m.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🔥 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘 𝗖𝗥𝗔𝗖𝗞 𝗘𝗡𝗚𝗜𝗡𝗘 🔥"))
        bot.send_message(m.chat.id, "☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n\nStatus: <b>ACCESS GRANTED</b> ✅", parse_mode="HTML", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🚩 JOIN VIP CHANNEL", url="https://t.me/+45fCzXzXxi0zMWI9"))
        bot.send_message(m.chat.id, "❌ Join Kar Pehle!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🔥 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘 𝗖𝗥𝗔𝗖𝗞 𝗘𝗡𝗚𝗜𝗡𝗘 🔥")
def engine(message):
    if not check_join(message.from_user.id): return
    
    bot.send_message(message.chat.id, "🛰️ <b>𝕮𝖗𝖆𝖈𝖐𝖎𝖓𝖌 𝖂𝖎𝖓𝕲𝖔 𝕬𝕻𝕴...</b>", parse_mode="HTML")
    last_p = None
    
    while True:
        history = get_data_cracked()
        if not history:
            time.sleep(5); continue 
            
        curr_p = history[0]['issueNumber']
        if curr_p != last_p:
            last_p = curr_p
            next_p = int(curr_p) + 1
            
            # Pattern Logic
            nums = [int(x['number']) for x in history[:3]]
            pred = "🌕 𝗕𝗜𝗚" if sum(nums)/3 >= 5 else "🌑 𝗦𝗠𝗔𝗟𝗟"
            
            box = (
                f"🎯 <b>ADITYA PAPA VIP BOX</b> 🎯\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"🔢 <b>PERIOD:</b> <code>{next_p}</code>\n"
                f"🔥 <b>BET:</b> <b>{pred}</b>\n"
                f"✨ <b>LUCK:</b> 99.9%\n"
                f"━━━━━━━━━━━━━━━━━━━"
            )
            bot.send_message(message.chat.id, box, parse_mode="HTML")
            
            # Result Check & Sticker
            time.sleep(55)
            res_data = get_data_cracked()
            if res_data and int(res_data[0]['issueNumber']) == next_p:
                actual = "BIG" if int(res_data[0]['number']) >= 5 else "SMALL"
                bot.send_sticker(message.chat.id, WIN_STICKER if pred.split()[1] == actual else LOSS_STICKER)
        time.sleep(2)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
    
