import telebot
from telebot import types
import time
import re
import urllib.parse
import base64
import os

# --- CONFIG ---
API_TOKEN = '8694242868:AAHw4p485GwDHnWQlxa7szVT8oqQZEtSf44'
bot = telebot.TeleBot(API_TOKEN, parse_mode="MarkdownV2")

# Tera Owner Link aur Channel Links
OWNER_LINK = "https://t.me/ADITYAXVIPBOT"
CHANNELS = ["-1003815161090", "-1003973812867"]
LINKS = ["https://t.me/+_RZ0gN9HU6xhZTRl", "https://t.me/+7bNfhxLosYsxMmVl"]

# --- 🔥 ULTIMATE RECURSIVE DECRYPTION ENGINE 🔥 ---
def ultimate_decrypt(content):
    # Multiple layers ko scan karne ke liye loop
    for _ in range(15):
        old_content = content
        
        # 1. Base64 Auto-Detector (Teri image wala encryption todne ke liye)
        b64_pattern = r'[A-Za-z0-9+/]{40,}(?:={0,2})'
        b64_matches = re.findall(b64_pattern, content)
        for b64 in b64_matches:
            try:
                decoded = base64.b64decode(b64).decode('utf-8', errors='ignore')
                if len(decoded) > 5:
                    content = content.replace(b64, decoded)
            except: pass

        # 2. Hex (\x) & Unicode (\u) Decoding
        content = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), content)
        content = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)
        
        # 3. URL/Unescape Decoding
        content = urllib.parse.unquote(content)

        # 4. JS Packing removal (Hum tags nahi hatayenge, sirf junk saaf karenge)
        content = content.replace('eval(unescape(', '').replace('document.write(', '').replace('unescape(', '')
        
        if old_content == content: # Jab file poori tarah saaf ho jaye
            break
            
    return content

# --- UI & HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✨ 𝐉𝐎𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝟏", url=LINKS[0]))
    markup.add(types.InlineKeyboardButton("✨ 𝐉𝐎𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝟐", url=LINKS[1]))
    markup.add(types.InlineKeyboardButton("🔄 𝐂𝐇𝐄𝐂𝐊 𝐀𝐏𝐏𝐑𝐎𝐕𝐀𝐋", callback_data="check"))
    
    bot.send_message(message.chat.id, """
*╔══════════════════════╗*
* 👑 𝐀𝐃𝐈𝐓𝐘𝐀 𝐗 𝐎𝐖𝐍𝐄𝐑 👑     *
*╚══════════════════════╝*

*⚠️ 𝐀𝐜𝐜𝐞𝐬𝐬 𝐃𝐞𝐧𝐢𝐞𝐝\! 𝐏𝐥𝐞𝐚𝐬𝐞 𝐉𝐨𝐢𝐧*
*𝐂𝐡𝐚𝐧𝐧𝐞𝐥𝐬 𝐭𝐨 𝐮𝐬𝐞 𝐃𝐞𝐜𝐫𝐲𝐩𝐭𝐨𝐫\.*
""", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "check":
        try:
            status1 = bot.get_chat_member(CHANNELS[0], call.from_user.id).status
            status2 = bot.get_chat_member(CHANNELS[1], call.from_user.id).status
            if status1 != 'left' and status2 != 'left':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("📤 𝐔𝐏𝐋𝐎𝐀𝐃𝐈𝐍𝐆 𝐅𝐈𝐋𝐄 𝐅𝐀𝐒𝐓𝐄𝐑", callback_data="up"))
                markup.add(types.InlineKeyboardButton("👨‍💻 𝐎𝐖𝐍𝐄𝐑", url=OWNER_LINK))
                bot.edit_message_text("*👑 𝐕𝐈𝐏 𝐌𝐄𝐍𝐔 𝐀𝐂𝐓𝐈𝐕𝐀𝐓𝐄𝐃\!*", call.message.chat.id, call.message.message_id, reply_markup=markup)
            else:
                bot.answer_callback_query(call.id, "❌ Requests Pending! Dono join karo.", show_alert=True)
        except:
            bot.answer_callback_query(call.id, "❌ Admin Error! Bot ko channel mein admin banao.", show_alert=True)
            
    elif call.data == "up":
        bot.send_message(call.message.chat.id, "*📥 𝐔𝐏𝐋𝐎𝐀𝐃𝐈𝐍𝐆 𝐅𝐈𝐋𝐄 𝐅𝐀𝐒𝐓𝐄𝐑\.\.\. 𝐒𝐞𝐧𝐝 𝐘𝐨𝐮𝐫 𝐇𝐓𝐌𝐋\!*")

@bot.message_handler(content_types=['document'])
def handle_file(message):
    if message.document.file_name.endswith('.html'):
        m = bot.send_message(message.chat.id, "⚙️ *𝐏𝐑𝐎𝐂𝐄𝐒𝐒𝐈𝐍𝐆: 𝟎%*")
        
        # Super Fast Professional Animation
        for i in range(10, 101, 10):
            time.sleep(0.3) 
            bar = "▓" * (i // 10) + "░" * (10 - (i // 10))
            bot.edit_message_text(f"⚡ *𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐈𝐍𝐆 𝐑𝐄𝐀𝐋 𝐃𝐀𝐓𝐀\.\.\.*\n\n`{bar}` *{i}%*", message.chat.id, m.message_id)

        file_info = bot.get_file(message.document.file_id)
        data = bot.download_file(file_info.file_path).decode('utf-8', errors='ignore')
        
        # Ultimate Decrypt Call
        final_html = ultimate_decrypt(data)

        # File Naming with "ENCRYPTION ADITYA"
        new_name = f"{message.document.file_name.split('.')[0]} ENCRYPTION ADITYA.html"
        with open(new_name, "w", encoding="utf-8") as f:
            f.write(final_html)

        with open(new_name, "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ *𝐅𝐈𝐋𝐄 𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐄𝐃 𝐁𝐘 𝐀𝐃𝐈𝐓𝐘𝐀 𝐗 𝐎𝐖𝐍𝐄𝐑*")
        
        bot.delete_message(message.chat.id, m.message_id)
        os.remove(new_name)
    else:
        bot.reply_to(message, "❌ *𝐒𝐞𝐧𝐝 𝐎𝐧𝐥𝐲 𝐇𝐓𝐌𝐋 𝐅𝐢𝐥𝐞𝐬\!*")

bot.infinity_polling()
