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

CHANNELS = ["-1003815161090", "-1003973812867"]
LINKS = ["https://t.me/+_RZ0gN9HU6xhZTRl", "https://t.me/+7bNfhxLosYsxMmVl"]

# --- 🔥 DECRYPTION ENGINE (FIXED) 🔥 ---
def real_decrypt_engine(content):
    # Layer 1: JavaScript Obfuscation removal (eval/unescape/hex)
    # Hum content ko damage nahi karenge, sirf encoding badlenge
    try:
        # Hex strings decode (\x...)
        content = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), content)
        # Unicode strings decode (\u...)
        content = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)
    except: pass

    # unescape() logic
    if "unescape(" in content:
        content = urllib.parse.unquote(content)

    # Base64 logic (sirf agar valid string mile)
    b64_pattern = r'atob\([\'"]([A-Za-z0-9+/=]{20,})[\'"]\)'
    matches = re.findall(b64_pattern, content)
    for b64_str in matches:
        try:
            decoded = base64.b64decode(b64_str).decode('utf-8', errors='ignore')
            content = content.replace(b64_str, decoded)
        except: pass

    # Important: Hum 'eval' ko sirf tab hatate hain jab wo string ke bahar ho
    # Taki HTML tags (like <script>) kharab na ho
    content = content.replace('eval(unescape(', '').replace('document.write(', '')
    
    return content

# --- UI & BUTTONS ---
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
                markup.add(types.InlineKeyboardButton("👨‍💻 𝐎𝐖𝐍𝐄𝐑", url="https://t.me/adityapaswan"))
                bot.edit_message_text("*👑 𝐕𝐈𝐏 𝐌𝐄𝐍𝐔 𝐀𝐂𝐓𝐈𝐕𝐀𝐓𝐄𝐃\!*", call.message.chat.id, call.message.message_id, reply_markup=markup)
            else:
                bot.answer_callback_query(call.id, "❌ Request Pending! Dono join karo.", show_alert=True)
        except:
            bot.answer_callback_query(call.id, "❌ Error! Bot ko admin banao.", show_alert=True)
            
    elif call.data == "up":
        bot.send_message(call.message.chat.id, "*📥 𝐔𝐏𝐋𝐎𝐀𝐃𝐈𝐍𝐆 𝐅𝐈𝐋𝐄 𝐅𝐀𝐒𝐓𝐄𝐑\.\.\. 𝐒𝐞𝐧𝐝 𝐇𝐓𝐌𝐋 𝐧𝐨𝐰\!*")

@bot.message_handler(content_types=['document'])
def handle_file(message):
    if message.document.file_name.endswith('.html'):
        m = bot.send_message(message.chat.id, "⚙️ *𝐏𝐑𝐎𝐂𝐄𝐒𝐒𝐈𝐍𝐆: 𝟎%*")
        
        # Super Fast Animation (Har step 0.5s)
        for i in range(10, 101, 10):
            time.sleep(0.5)
            bar = "▓" * (i // 10) + "░" * (10 - (i // 10))
            bot.edit_message_text(f"⚡ *𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐈𝐍𝐆\.\.\.*\n\n`{bar}` *{i}%*", message.chat.id, m.message_id)

        file_info = bot.get_file(message.document.file_id)
        data = bot.download_file(file_info.file_path).decode('utf-8', errors='ignore')
        
        # Real Decrypt Call
        final_html = real_decrypt_engine(data)

        # File Naming
        new_name = f"{message.document.file_name.split('.')[0]} ENCRYPTION ADITYA.html"
        with open(new_name, "w", encoding="utf-8") as f:
            f.write(final_html)

        with open(new_name, "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ *𝐅𝐈𝐋𝐄 𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐄𝐃 𝐁𝐘 𝐀𝐃𝐈𝐓𝐘𝐀 𝐗 𝐎𝐖𝐍𝐄𝐑*")
        
        bot.delete_message(message.chat.id, m.message_id)
        os.remove(new_name)
    else:
        bot.reply_to(message, "❌ *𝐒𝐞𝐧𝐝 𝐎𝐧𝐥𝐲 𝐇𝐓𝐌𝐋\!*")

bot.infinity_polling()
