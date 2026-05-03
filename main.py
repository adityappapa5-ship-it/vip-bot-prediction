import telebot
from telebot import types
import re
import urllib.parse
import base64
import os

# --- CONFIG ---
API_TOKEN = '8694242868:AAHw4p485GwDHnWQlxa7szVT8oqQZEtSf44'
bot = telebot.TeleBot(API_TOKEN, parse_mode="MarkdownV2")

# TERE LINKS
CHANNELS = ["-1003815161090", "-1003973812867"]
LINKS = ["https://t.me/+_RZ0gN9HU6xhZTRl", "https://t.me/+7bNfhxLosYsxMmVl"]
OWNER_LINK = "https://t.me/ADITYAXVIPBOT"

# --- 🔥 ULTRA FAST INVISIBLE DECRYPTION 🔥 ---
def fast_invisible_decrypt(content):
    # Ye logic sirf encryption layers ko hatayega, UI ko touch nahi karega
    for _ in range(10):
        old_content = content
        
        # 1. Base64 Auto-Unpacker (Design safe rakhta hai)
        b64_pattern = r'atob\s*\(\s*[\'"]([A-Za-z0-9+/=]{20,})[\'"]\s*\)'
        matches = re.findall(b64_pattern, content)
        for b64 in matches:
            try:
                decoded = base64.b64decode(b64).decode('utf-8', errors='ignore')
                # Code replace karega par structure nahi todega
                content = content.replace(f"atob('{b64}')", f"`{decoded}`")
                content = content.replace(f'atob("{b64}")', f'`{decoded}`')
            except: pass

        # 2. Hex aur Unicode Decode
        content = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), content)
        content = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)
        
        # 3. URL Unescape
        content = urllib.parse.unquote(content)

        if old_content == content:
            break
            
    # Sirf execution wrappers hatana hai taaki source code dikhe
    content = content.replace('eval(unescape(', '').replace('eval(', '')
    return content

# --- UI HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✨ 𝐉𝐎𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝟏", url=LINKS[0]))
    markup.add(types.InlineKeyboardButton("✨ 𝐉𝐎𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝟐", url=LINKS[1]))
    markup.add(types.InlineKeyboardButton("🔄 𝐂𝐇𝐄𝐂𝐊 𝐀𝐏𝐏𝐑𝐎𝐕𝐀𝐋", callback_data="check"))
    
    bot.send_message(message.chat.id, f"""
*╔══════════════════════╗*
* 👑 𝐀𝐃𝐈𝐓𝐘𝐀 𝐗 𝐎𝐖𝐍𝐄𝐑 👑     *
*╚══════════════════════╝*

*⚠️ 𝐀𝐜𝐜𝐞𝐬𝐬 𝐃𝐞𝐧𝐢𝐞𝐝\! 𝐏𝐥𝐞𝐚𝐬𝐞 𝐉𝐨𝐢𝐧*
*𝐁𝐨𝐭𝐡 𝐂𝐡𝐚𝐧𝐧𝐞𝐥𝐬 𝐁𝐞𝐥𝐨𝐰 𝐓𝐨 𝐔𝐬𝐞\.*
""", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "check":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📤 𝐔𝐏𝐋𝐎𝐀𝐃𝐈𝐍𝐆 𝐅𝐈𝐋𝐄 𝐅𝐀𝐒𝐓𝐄𝐑", callback_data="up"))
        markup.add(types.InlineKeyboardButton("👨‍💻 𝐎𝐖𝐍𝐄𝐑", url=OWNER_LINK))
        bot.edit_message_text("*👑 𝐕𝐈𝐏 𝐌𝐄𝐍𝐔 𝐀𝐂𝐓𝐈𝐕𝐀𝐓𝐄𝐃\!*", call.message.chat.id, call.message.message_id, reply_markup=markup)
            
    elif call.data == "up":
        bot.send_message(call.message.chat.id, "*📥 𝐔𝐏𝐋𝐎𝐀𝐃𝐈𝐍𝐆 𝐅𝐈𝐋𝐄 𝐅𝐀𝐒𝐓𝐄𝐑\.\.\. 𝐒𝐞𝐧𝐝 𝐘𝐨𝐮𝐫 𝐇𝐓𝐌𝐋\!*")

@bot.message_handler(content_types=['document'])
def handle_file(message):
    if message.document.file_name.endswith('.html'):
        # 1 se 100 tak super fast animation (No Sleep)
        m = bot.send_message(message.chat.id, "⚡ *𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐈𝐍𝐆: 𝟏%*")
        
        # Fast animation loop
        for i in [20, 50, 80, 100]:
            bot.edit_message_text(f"⚡ *𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐈𝐍𝐆: {i}%*", message.chat.id, m.message_id)

        file_info = bot.get_file(message.document.file_id)
        data = bot.download_file(file_info.file_path).decode('utf-8', errors='ignore')
        
        # Real Logic (No UI Change)
        final_html = fast_invisible_decrypt(data)

        caption_text = f"""
👑 *𝐇𝐓𝐌𝐋 𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐈𝐎𝐍 𝐃𝐎𝐍𝐄* ✅

🔐 *𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝟏:* {LINKS[0]}
🔐 *𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝟐:* {LINKS[1]}
"""
        new_name = f"{message.document.file_name.split('.')[0]} ENCRYPTION ADITYA.html"
        with open(new_name, "w", encoding="utf-8") as f:
            f.write(final_html)

        with open(new_name, "rb") as f:
            bot.send_document(message.chat.id, f, caption=caption_text)
        
        bot.delete_message(message.chat.id, m.message_id)
        os.remove(new_name)

bot.infinity_polling()
