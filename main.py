import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVER FOR 24/7 ---
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

def get_data_ultimate():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Origin': 'https://ar-lottery01.com'
    }
    try:
        r = requests.get(API_URL, headers=headers, timeout=15)
        return r.json().get('data', {}).get('list', [])
    except: return None

@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔥 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘 𝗖𝗥𝗔𝗖𝗞 𝗘𝗡𝗚𝗜𝗡𝗘 🔥"))
    bot.send_message(m.chat.id, "☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n\nStatus: <b>READY TO KILL</b> 🚀", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🔥 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘 𝗖𝗥𝗔𝗖𝗞 𝗘𝗡𝗚𝗜𝗡𝗘 🔥")
def engine(message):
    # DIRECT ACTION - NO DELAY
    last_p = None
    bot.send_message(message.chat.id, "🚀 <b>𝕰𝖓𝖌𝖎𝖓𝖊 𝕾𝖙𝖆𝖗𝖙𝖊𝕯... 𝖂𝖆𝖎𝖙 𝖋𝖔𝖗 𝕻𝖊𝖗𝖎𝖔𝕯</b>", parse_mode="HTML")
    
    while True:
        try:
            history = get_data_ultimate()
            if history:
                curr_p = history[0]['issueNumber']
                
                if curr_p != last_p:
                    last_p = curr_p
                    next_p = int(curr_p) + 1
                    
                    # VIP Logic
                    nums = [int(x['number']) for x in history[:3]]
                    pred = "🌕 𝗕𝗜𝗚" if sum(nums)/3 >= 5 else "🌑 𝗦𝗠𝗔𝗟𝗟"
                    
                    # FINAL PREDICTION BOX
                    box = (
                        f"☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n"
                        f"━━━━━━━━━━━━━━━━━━━\n"
                        f"🔢 <b>PERIOD:</b> <code>{next_p}</code>\n"
                        f"🎯 <b>PREDICT:</b> <b>{pred}</b>\n"
                        f"🔥 <b>STATUS:</b> 𝕮𝕽𝕬𝕮𝕶𝕰𝕯\n"
                        f"━━━━━━━━━━━━━━━━━━━"
                    )
                    bot.send_message(message.chat.id, box, parse_mode="HTML")
                    
                    # Result Analysis for Stickers
                    time.sleep(55)
                    res_data = get_data_ultimate()
                    if res_data and int(res_data[0]['issueNumber']) == next_p:
                        actual = "BIG" if int(res_data[0]['number']) >= 5 else "SMALL"
                        bot.send_sticker(message.chat.id, WIN_STICKER if pred.split()[1] == actual else LOSS_STICKER)
            
            time.sleep(5) # API Check Interval
        except Exception as e:
            time.sleep(10)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
