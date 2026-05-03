import telebot
from telebot import types
import time
import re
import urllib.parse

# --- CONFIG ---
API_TOKEN = '8694242868:AAHw4p485GwDHnWQlxa7szVT8oqQZEtSf44'
bot = telebot.TeleBot(API_TOKEN, parse_mode="MarkdownV2")

CHANNELS = ["-1003815161090", "-1003973812867"]
LINKS = ["https://t.me/+_RZ0gN9HU6xhZTRl", "https://t.me/+7bNfhxLosYsxMmVl"]

# --- REAL DECRYPTION ENGINE ---
def real_decrypt(content):
    # 1. Hex codes (\x68\x74...) ko text mein badalna
    try:
        content = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), content)
    except: pass

    # 2. Unicode (\u0068...) ko text mein badalna
    try:
        content = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)
    except: pass

    # 3. unescape() functions ko decode karna
    if "unescape(" in content:
        matches = re.findall(r'unescape\([\'"](.[^\'"]*)[\'"]\)', content)
        for match in matches:
            decoded = urllib.parse.unquote(match)
            content = content.replace(f"unescape('{match}')", f"'{decoded}'")
            content = content.replace(f'unescape("{match}")', f'"{decoded}"')

    # 4. eval() aur document.write() tags ko saaf karna taaki hidden code dikhe
    content = re.sub(r'eval\(', '', content)
    content = re.sub(r'document\.write\(', '', content)
    
    return content

# --- UI & HANDLERS ---
@bot.message_handler(commands=['start'])
def welcome(message):
    # Check Join Request logic
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📢 𝐉𝐎𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝟏", url=LINKS[0])
    btn2 = types.InlineKeyboardButton("📢 𝐉𝐎𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝟐", url=LINKS[1])
    btn3 = types.InlineKeyboardButton("🔄 𝐂𝐇𝐄𝐂𝐊 𝐉𝐎𝐈𝐍", callback_data="check_join")
    markup.add(btn1, btn2)
    markup.add(btn3)
    
    bot.send_message(message.chat.id, """
*╔══════════════════════╗*
* ⚠️ 𝐏𝐋𝐄𝐀𝐒𝐄 𝐅𝐈𝐑𝐒𝐓 𝐉𝐎𝐈𝐍\!  *
*╚══════════════════════╝*

*𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐝𝐚𝐥𝐧𝐞 𝐤𝐞 𝐛𝐚𝐚𝐝 𝐂𝐡𝐞𝐜𝐤 𝐉𝐨𝐢𝐧 𝐝𝐚𝐛𝐚𝐲𝐞𝐢𝐧\.*
""", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "check_join":
        # Check if user is in channels
        is_joined = True
        for chat_id in CHANNELS:
            try:
                status = bot.get_chat_member(chat_id, call.from_user.id).status
                if status in ['left', 'kicked']: is_joined = False
            except: is_joined = False
        
        if is_joined:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📤 𝐔𝐏𝐋𝐎𝐀𝐃𝐈𝐍𝐆 𝐅𝐈𝐋𝐄", callback_data="upload"))
            markup.add(types.InlineKeyboardButton("👨‍💻 𝐂𝐔𝐒𝐓𝐎𝐌𝐄𝐑 𝐂𝐀𝐑𝐄", url="https://t.me/adityapaswan"))
            bot.edit_message_text("*👑 𝐀𝐃𝐈𝐓𝐘𝐀 𝐏𝐀𝐒𝐖𝐀𝐍 𝐕𝐈𝐏 𝐀𝐂𝐓𝐈𝐕𝐀𝐓𝐄𝐃\!*", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "❌ Join Request Not Found!", show_alert=True)
            
    elif call.data == "upload":
        bot.send_message(call.message.chat.id, "*📥 𝐀𝐛 𝐚𝐩𝐧𝐢 𝐄𝐧𝐜𝐫𝐲𝐩𝐭𝐞𝐝 𝐇𝐓𝐌𝐋 𝐟𝐢𝐥𝐞 𝐛𝐡𝐞𝐣𝐞𝐢𝐧\.*")

@bot.message_handler(content_types=['document'])
def handle_decrypt(message):
    if message.document.file_name.endswith('.html'):
        msg = bot.send_message(message.chat.id, "⚙️ *𝐏𝐑𝐎𝐂𝐄𝐒𝐒𝐈𝐍𝐆: 𝟎%*")
        
        # 10 Seconds Progress Bar
        for i in range(10, 101, 10):
            time.sleep(1)
            bar = "▓" * (i // 10) + "░" * (10 - (i // 10))
            bot.edit_message_text(f"⚡ *𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐈𝐍𝐆\.\.\.*\n\n`{bar}` *{i}%*", message.chat.id, msg.message_id)

        # Download & Real Decrypt
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        raw_content = downloaded_file.decode('utf-8', errors='ignore')
        
        # Real Decrypt Engine Call
        final_content = real_decrypt(raw_content)

        file_name = f"REAL_DECRYPTED_{message.document.file_name}"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(final_content)

        with open(file_name, "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ *𝐑𝐄𝐀𝐋 𝐇𝐓𝐌𝐋 𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐄𝐃 𝐁𝐘 𝐀𝐃𝐈𝐓𝐘𝐀 𝐏𝐀𝐒𝐖𝐀𝐍*")
        bot.delete_message(message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "❌ *𝐒𝐢𝐫𝐟 𝐇𝐓𝐌𝐋 𝐟𝐢𝐥𝐞 𝐝𝐨\!*")

bot.infinity_polling()
