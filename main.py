import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVER KEEP-ALIVE (FOR 24/7) ---
app = Flask('')
@app.route('/')
def home(): return "ADITYA VIP CRACK IS ALIVE 24/7"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- CONFIG ---
API_TOKEN = '8618263406:AAHreGN69x_-g-_ZQ0VsieTWISgmxnCHBWo'
CHANNELS = [-1003815161090, -1003973812867]
WIN_STICKER = 'CAACAgUAAxkBAAERJRhp9B-PkyNlzscUNGUAAUchyXw63g8AAisSAAJSEdhVkI_Ixu7liJU7BA'
LOSS_STICKER = 'CAACAgUAAxkBAAERJRpp9B-X_XQ3vbejkVPLEIBkdKki-QACkBQAAiMYmVWHXHRU3FIjKzsE'
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def get_crack_logic(history):
    nums = [int(x['number']) for x in history[:5]]
    last = "BIG" if nums[0] >= 5 else "SMALL"
    if all(n >= 5 for n in nums[:2]) or all(n < 5 for n in nums[:2]):
        return "🌕 𝗕𝗜𝗚" if last == "SMALL" else "🌑 𝗦𝗠𝗔𝗟𝗟"
    return random.choice(["🌕 𝗕𝗜𝗚", "🌑 𝗦𝗠𝗔𝗟𝗟"])

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
        markup.add(types.KeyboardButton("🔥 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘 𝗖𝗥𝗔𝗖𝗞 𝗘𝗡𝗚𝗜𝗡𝗘 🔥"))
        bot.send_message(message.chat.id, "☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n\n<i>Status: 24/7 CLOUD ACTIVE</i>", parse_mode="HTML", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🚩 𝕵𝖔𝖎𝖓 𝖁𝕴𝕻 𝕮𝖍𝖆𝖓𝖓𝖊𝖑", url="https://t.me/+45fCzXzXxi0zMWI9"))
        bot.send_message(message.chat.id, "❌ Join kar Madrachod!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🔥 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘 𝗖𝗥𝗔𝗖𝗞 𝗘𝗡𝗚𝗜𝗡𝗘 🔥")
def engine(message):
    bot.send_message(message.chat.id, "🛰️ <b>𝕮𝖗𝖆𝖈𝖐𝖎𝖓𝖌 𝕬𝕻𝕴...</b>", parse_mode="HTML")
    last_p = None
    while True:
        try:
            r = requests.get(API_URL, timeout=10).json()
            history = r['data']['list']
            curr_p = history[0]['issueNumber']
            if curr_p != last_p:
                last_p = curr_p
                next_p = int(curr_p) + 1
                prediction = get_crack_logic(history)
                box = (
                    f"☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"🔢 <b>𝕻𝕰𝕽𝕴𝕺𝕯:</b> <code>{next_p}</code>\n"
                    f"🎯 <b>𝕻𝕽𝕰𝕯𝕴𝕮𝕿:</b> <b>{prediction}</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━"
                )
                bot.send_message(message.chat.id, box, parse_mode="HTML")
                time.sleep(55)
                res = requests.get(API_URL).json()['data']['list'][0]
                if int(res['issueNumber']) == next_p:
                    actual = "BIG" if int(res['number']) >= 5 else "SMALL"
                    bot.send_sticker(message.chat.id, WIN_STICKER if prediction.split()[1] == actual else LOSS_STICKER)
            time.sleep(2)
        except: time.sleep(5)

if __name__ == "__main__":
    # Threading start taaki Flask aur Bot dono saath chalein
    Thread(target=run).start()
    bot.infinity_polling()
