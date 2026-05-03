import telebot
from telebot import types
import re
import urllib.parse
import base64
import os

# --- CONFIG ---
API_TOKEN = '8694242868:AAHw4p485GwDHnWQlxa7szVT8oqQZEtSf44'
bot = telebot.TeleBot(API_TOKEN, parse_mode="MarkdownV2")

# ASLI TERE LINKS (NO CHANGES)
CHANNELS = ["-1003815161090", "-1003973812867"]
LINKS = ["https://t.me/+_RZ0gN9HU6xhZTRl", "https://t.me/+7bNfhxLosYsxMmVl"]
OWNER_LINK = "https://t.me/ADITYAXVIPBOT"

# --- 🔥 DEEP SOURCE UNPACKER (UI SAFE) 🔥 ---
def final_stable_decrypt(content):
    # Loop for deep obfuscation layers
    for _ in range(15):
        old_content = content
        
        # 1. Base64/atob extraction without breaking UI tags
        b64_pattern = r'atob\s*\(\s*[\'"]([A-Za-z0-9+/=]{20,})[\'"]\s*\)'
        for b64 in re.findall(b64_pattern, content):
            try:
                decoded = base64.b64decode(b64).decode('utf-8', errors='ignore')
                # Replace content only, keep the surrounding code logic
                content = content.replace(f'atob("{b64}")', f'"{decoded}"')
                content = content.replace(f"atob('{b64}')", f"'{decoded}'")
            except: pass

        # 2. Hex (\x) & Unicode (\u) cleaner
        content = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), content)
        content = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)
        
        # 3. Fast URL Decode
        if "%" in content:
            content = urllib.parse.unquote(content)

        if old_content == content: break
            
    # CRITICAL: Strip eval/unescape but keep the HTML/CSS tags intact
    content = content.replace('eval(unescape(', '').replace('eval(', '').replace('document.write(', '')
    return content

# --- UI & HANDLERS ---
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
        markup.add(types.InlineKeyboardButton("📤 𝐔𝐏𝐋𝐎𝐀𝐃 𝐇𝐓𝐌𝐋", callback_data="up"))
        markup.add(types.InlineKeyboardButton("👨‍💻 𝐎𝐖𝐍𝐄𝐑", url=OWNER_LINK))
        bot.edit_message_text("*👑 𝐕𝐈𝐏 𝐌𝐄𝐍𝐔 𝐀𝐂𝐓𝐈𝐕𝐀𝐓𝐄𝐃\!*", call.message.chat.id, call.message.message_id, reply_markup=markup)
            
    elif call.data == "up":
        bot.send_message(call.message.chat.id, "*📥 𝐒𝐞𝐧𝐝 𝐘𝐨𝐮 r 𝐄𝐧𝐜𝐫𝐲𝐩𝐭𝐞𝐝 𝐇𝐓𝐌𝐋 𝐍𝐨𝐰\!*")

@bot.message_handler(content_types=['document'])
def handle_file(message):
    if message.document.file_name.endswith('.html'):
        m = bot.send_message(message.chat.id, "⚡ *𝐈𝐍𝐒𝐓𝐀𝐍𝐓 𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐈𝐍𝐆\.\.\.*")
        
        try:
            file_info = bot.get_file(message.document.file_id)
            data = bot.download_file(file_info.file_path).decode('utf-8', errors='ignore')
            
            # Super Fast Decrypt
            final_html = final_stable_decrypt(data)

            caption_text = f"""
👑 *𝐇𝐓𝐌𝐋 𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐈𝐎𝐍 𝐃𝐎𝐍𝐄* ✅

🔐 *𝐂𝐡𝐚𝐧𝐧 e𝐥 𝟏:* {LINKS[0]}
🔐 *𝐂𝐡𝐚𝐧𝐧 e𝐥 𝟐:* {LINKS[1]}
"""
            new_name = f"DECRYPTED_{message.document.file_name}"
            with open(new_name, "w", encoding="utf-8") as f:
                f.write(final_html)

            with open(new_name, "rb") as f:
                bot.send_document(message.chat.id, f, caption=caption_text)
            
            bot.delete_message(message.chat.id, m.message_id)
            os.remove(new_name)
        except Exception as e:
            bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, m.message_id)

bot.infinity_polling()
