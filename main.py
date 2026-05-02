import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVER FOR 24/7 CLOUD ---
app = Flask('')
@app.route('/')
def home(): return "ADITYA VIP CRACK IS LIVE 24/7"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- CONFIG (STAY ACTIVE) ---
API_TOKEN = '8618263406:AAHreGN69x_-g-_ZQ0VsieTWISgmxnCHBWo'
CHANNELS = [-1003815161090, -1003973812867]
WIN_STICKER = 'CAACAgUAAxkBAAERJRhp9B-PkyNlzscUNGUAAUchyXw63g8AAisSAAJSEdhVkI_Ixu7liJU7BA'
LOSS_STICKER = 'CAACAgUAAxkBAAERJRpp9B-X_XQ3vbejkVPLEIBkdKki-QACkBQAAiMYmVWHXHRU3FIjKzsE'
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def check_join(uid):
    """Bhai bina join kiye access block rahega"""
    for c in CHANNELS:
        try:
            status = bot.get_chat_member(c, uid).status
            if status in ['left', 'kicked']: return False
        except: continue
    return True

def get_data_safe():
    """Anti-Block API Fetcher"""
    h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Origin': 'https://ar-lottery01.com',
        'Referer': 'https://ar-lottery01.com/'
    }
    try:
        r = requests.get(API_URL, headers=h, timeout=20)
        return r.json()['data']['list']
    except: return None

@bot.message_handler(commands=['start'])
def start(message):
    if check_join(message.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🔥 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘 𝗖𝗥𝗔𝗖𝗞 𝗘𝗡𝗚𝗜𝗡𝗘 🔥"))
        bot.send_message(message.chat.id, "☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n\nStatus: <b>ACCESS GRANTED</b> ✅", parse_mode="HTML", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🚩 JOIN VIP CHANNEL 1", url="https://t.me/+45fCzXzXxi0zMWI9"),
            types.InlineKeyboardButton("🚩 JOIN VIP CHANNEL 2", url="https://t.me/+_RZ0gN9HU6xhZTRl"),
            types.InlineKeyboardButton("✅ VERIFY JOIN", callback_data="v")
        )
        bot.send_message(message.chat.id, "❌ <b>ACCESS LOCKED</b> ❌\nPehle Join Kar Madrachod!", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "v")
def v(c):
    if check_join(c.from_user.id):
        bot.answer_callback_query(c.id, "Success! Start pe click karo.")
        start(c.message)
    else:
        bot.answer_callback_query(c.id, "Join kar pehle!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "🔥 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘 𝗖𝗥𝗔𝗖𝗞 𝗘𝗡𝗚𝗜𝗡𝗘 🔥")
def engine(message):
    if not check_join(message.from_user.id): return
    bot.send_message(message.chat.id, "🛰️ <b>𝕮𝖗𝖆𝖈𝖐𝖎𝖓𝖌 𝖂𝖎𝖓𝕲𝖔 𝕬𝕻𝕴...</b>", parse_mode="HTML")
    last_p = None
    while True:
        try:
            history = get_data_safe()
            if not history:
                time.sleep(5); continue
            
            curr_p = history[0]['issueNumber']
            if curr_p != last_p:
                last_p = curr_p
                next_p = int(curr_p) + 1
                
                # Crack Logic
                nums = [int(x['number']) for x in history[:3]]
                pred = "🌕 𝗕𝗜𝗚" if sum(nums)/3 >= 5 else "🌑 𝗦𝗠𝗔𝗟𝗟"
                
                box = (
                    f"☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"🔢 <b>𝕻𝕰𝕽𝕴𝕺𝕯:</b> <code>{next_p}</code>\n"
                    f"🎯 <b>𝕻𝕽𝕰𝕯𝕴𝕮𝕿:</b> <b>{pred}</b>\n"
                    f"🔥 <b>𝕾𝕿𝕬𝕿𝖀𝕾:</b> 𝕮𝕽𝕬𝕮𝕶𝕰𝕯\n"
                    f"━━━━━━━━━━━━━━━━━━━"
                )
                bot.send_message(message.chat.id, box, parse_mode="HTML")
                
                # Waiting for result to show sticker
                time.sleep(55)
                res = requests.get(API_URL).json()['data']['list'][0]
                if int(res['issueNumber']) == next_p:
                    actual = "BIG" if int(res['number']) >= 5 else "SMALL"
                    bot.send_sticker(message.chat.id, WIN_STICKER if pred.split()[1] == actual else LOSS_STICKER)
            time.sleep(2)
        except: time.sleep(5)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling(timeout=20)
