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

OWNER_LINK = "https://t.me/ADITYAXVIPBOT"
MY_CHANNEL = "https://t.me/+_yHnY4cQrzY5MjA9" # Aapka Channel Link

# --- 🔥 PRO DECRYPTION & RE-DESIGN ENGINE 🔥 ---
def ultimate_vip_decrypt(content):
    # Loop for deep layers
    for _ in range(10):
        old_content = content
        # Base64 Scanner
        b64_matches = re.findall(r'[A-Za-z0-9+/]{40,}(?:={0,2})', content)
        for b64 in b64_matches:
            try:
                decoded = base64.b64decode(b64).decode('utf-8', errors='ignore')
                if len(decoded) > 10: content = content.replace(b64, decoded)
            except: pass
        # Hex/Unicode/Unescape
        content = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), content)
        content = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)
        content = urllib.parse.unquote(content)
        if old_content == content: break

    # Yahan hum asli HTML structure restore kar rahe hain (VIP Look)
    # Taki kachra saaf ho aur interface sahi dikhe
    content = content.replace('eval(', '').replace('document.write(', '')
    
    return content

# --- UI LOGIC ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✨ 𝐉𝐎𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋", url=MY_CHANNEL))
    markup.add(types.InlineKeyboardButton("🔄 𝐂𝐇𝐄𝐂𝐊 𝐀𝐏𝐏𝐑𝐎𝐕𝐀𝐋", callback_data="check"))
    
    bot.send_message(message.chat.id, f"""
*╔══════════════════════╗*
* 👑 𝐀𝐃𝐈𝐓𝐘𝐀 𝐗 𝐎𝐖𝐍𝐄𝐑 👑     *
*╚══════════════════════╝*

*⚠️ 𝐀𝐜𝐜𝐞𝐬𝐬 𝐃𝐞𝐧𝐢𝐞𝐝\! 𝐏𝐥𝐞𝐚𝐬𝐞 𝐉𝐨𝐢𝐧*
*𝐎𝐮𝐫 𝐎𝐟𝐟𝐢𝐜𝐢𝐚𝐥 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐁𝐞𝐥𝐨𝐰\.*
""", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "check":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📤 𝐔𝐏𝐋𝐎𝐀𝐃𝐈𝐍𝐆 𝐅𝐈𝐋𝐄 𝐅𝐀𝐒𝐓𝐄𝐑", callback_data="up"))
        markup.add(types.InlineKeyboardButton("👨‍💻 𝐎𝐖𝐍𝐄𝐑", url=OWNER_LINK))
        bot.edit_message_text("*👑 𝐕𝐈𝐏 𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐎𝐑 𝐀𝐂𝐓𝐈𝐕𝐀𝐓𝐄𝐃\!*", call.message.chat.id, call.message.message_id, reply_markup=markup)
            
    elif call.data == "up":
        bot.send_message(call.message.chat.id, "*📥 𝐔𝐏𝐋𝐎𝐀𝐃𝐈𝐍𝐆 𝐅𝐈𝐋𝐄 𝐅𝐀𝐒𝐓𝐄𝐑\.\.\. 𝐒𝐞𝐧𝐝 𝐇𝐓𝐌𝐋\!*")

@bot.message_handler(content_types=['document'])
def handle_file(message):
    if message.document.file_name.endswith('.html'):
        m = bot.send_message(message.chat.id, "⚙️ *𝐏𝐑𝐎𝐂𝐄𝐒𝐒𝐈𝐍𝐆: 𝟎%*")
        
        # Fast Animation
        for i in range(10, 101, 20):
            time.sleep(0.2) 
            bot.edit_message_text(f"⚡ *𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐈𝐍𝐆 𝐕𝐈𝐏\.\.\.* `{i}%`", message.chat.id, m.message_id)

        file_info = bot.get_file(message.document.file_id)
        data = bot.download_file(file_info.file_path).decode('utf-8', errors='ignore')
        
        # Real Logic Call
        final_html = ultimate_vip_decrypt(data)

        # Aapka branding aur link add karna
        caption_text = f"""
👑 *𝐇𝐓𝐌𝐋 𝐄𝐍𝐂𝐑𝐘𝐏𝐓𝐈𝐎𝐍 𝐃𝐎𝐍𝐄* ✅

🔐 *𝐂𝐡𝐚𝐧𝐧𝐞𝐥:* {MY_CHANNEL}
"""
        new_name = f"{message.document.file_name.split('.')[0]} ENCRYPTION ADITYA.html"
        with open(new_name, "w", encoding="utf-8") as f:
            f.write(final_html)

        with open(new_name, "rb") as f:
            bot.send_document(message.chat.id, f, caption=caption_text)
        
        bot.delete_message(message.chat.id, m.message_id)
        os.remove(new_name)

bot.infinity_polling()
