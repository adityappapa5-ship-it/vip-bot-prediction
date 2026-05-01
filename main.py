import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVER FOR 24/7 CLOUD ---
app = Flask('')
@app.route('/')
def home(): return "ADITYA VIP BYPASS ACTIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- CONFIG ---
API_TOKEN = '8618263406:AAHreGN69x_-g-_ZQ0VsieTWISgmxnCHBWo'
CHANNELS = [-1003815161090, -1003973812867]
WIN_STICKER = 'CAACAgUAAxkBAAERJRhp9B-PkyNlzscUNGUAAUchyXw63g8AAisSAAJSEdhVkI_Ixu7liJU7BA'
LOSS_STICKER = 'CAACAgUAAxkBAAERJRpp9B-X_XQ3vbejkVPLEIBkdKki-QACkBQAAiMYmVWHXHRU3FIjKzsE'
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def get_data_bypass():
    """Advanced Human-Like Headers to fix API Error"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    ]
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://ar-lottery01.com',
        'Referer': 'https://ar-lottery01.com/',
        'Sec-Ch-Ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }
    try:
        r = requests.get(API_URL, headers=headers, timeout=20)
        if r.status_code == 200:
            return r.json()['data']['list']
        else:
            print(f"API Error Code: {r.status_code}")
            return None
    except Exception as e:
        print(f"Request Failed: {e}")
        return None

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔥 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘 𝗖𝗥𝗔𝗖𝗞 𝗘𝗡𝗚𝗜𝗡𝗘 🔥"))
    bot.send_message(message.chat.id, "☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n\nStatus: <b>BYPASS SYSTEM ACTIVE</b> ✅", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🔥 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘 𝗖𝗥𝗔𝗖𝗞 𝗘𝗡𝗚𝗜𝗡𝗘 🔥")
def engine(message):
    bot.send_message(message.chat.id, "🛰️ <b>𝕮𝖗𝖆𝖈𝖐𝖎𝖓𝖌 𝖂𝖎𝖓𝕲𝖔 𝕬𝕻𝕴...</b>", parse_mode="HTML")
    last_p = None
    while True:
        try:
            history = get_data_bypass()
            if not history:
                time.sleep(10); continue # API Error wait
            
            curr_p = history[0]['issueNumber']
            if curr_p != last_p:
                last_p = curr_p
                next_p = int(curr_p) + 1
                
                nums = [int(x['number']) for x in history[:3]]
                pred = "🌕 𝗕𝗜𝗚" if sum(nums)/3 >= 5 else "🌑 𝗦𝗠𝗔𝗟𝗟"
                
                box = (
                    f"☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"🔢 <b>𝕻𝕰𝕽𝕴𝕺𝕯:</b> <code>{next_p}</code>\n"
                    f"🎯 <b>𝕻𝕽𝕰𝕯𝕴𝕮𝕿:</b> <b>{pred}</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━"
                )
                bot.send_message(message.chat.id, box, parse_mode="HTML")
                time.sleep(55)
            time.sleep(2)
        except: time.sleep(5)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
    
