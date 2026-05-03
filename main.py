import telebot
from telebot import types
import time

# --- CONFIG ---
API_TOKEN = '8694242868:AAHw4p485GwDHnWQlxa7szVT8oqQZEtSf44'
bot = telebot.TeleBot(API_TOKEN, parse_mode="MarkdownV2")

# Channels for Join Request
CHANNELS = ["-1003815161090", "-1003973812867"]
LINKS = ["https://t.me/+_RZ0gN9HU6xhZTRl", "https://t.me/+7bNfhxLosYsxMmVl"]

# --- TEXTURE FONTS & DESIGN ---
JOIN_TEXT = """
*╔══════════════════════╗*
* 📥 𝐉𝐎𝐈𝐍 𝐑𝐄𝐐𝐔𝐄𝐒𝐓 𝐏𝐄𝐍𝐃𝐈𝐍𝐆   *
*╚══════════════════════╝*

*⚠️ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐫𝐬𝐭 𝐉𝐨𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥𝐬\!*
*𝐀𝐚𝐩𝐤𝐨 𝐧𝐢𝐜𝐡𝐞 𝐝𝐢𝐲𝐞 𝐠𝐚𝐲𝐞 𝐛𝐮𝐭𝐭𝐨𝐧𝐬 𝐬𝐞*
*𝐫𝐞𝐪𝐮𝐞𝐬𝐭 𝐝𝐚𝐥𝐧𝐢 𝐡𝐨𝐠𝐢 𝐭𝐚𝐛𝐡𝐢 𝐛𝐨𝐭 𝐜𝐡𝐚𝐥𝐞𝐠𝐚\.*
"""

VIP_MENU = """
*╔══════════════════════╗*
* 👑 𝐀𝐃𝐈𝐓𝐘𝐀 𝐏𝐀𝐒𝐖𝐀𝐍 𝐕𝐈𝐏 👑   *
*╚══════════════════════╝*

*𝐒𝐭𝐚𝐭𝐮𝐬:* 🟢 𝐀𝐜𝐭𝐢𝐯𝐞
*𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐁𝐚𝐜𝐤 𝐀𝐝𝐢𝐭𝐲𝐚 𝐏𝐚𝐩𝐚\!*
"""

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    # Check if user is in channels or has sent request
    is_member = True
    for chat in CHANNELS:
        try:
            status = bot.get_chat_member(chat, user_id).status
            if status not in ['member', 'administrator', 'creator', 'restricted']:
                is_member = False
        except:
            is_member = False

    if not is_member:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 𝐉𝐎𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝟏", url=LINKS[0]))
        markup.add(types.InlineKeyboardButton("📢 𝐉𝐎𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝟐", url=LINKS[1]))
        markup.add(types.InlineKeyboardButton("🔄 𝐂𝐇𝐄𝐂𝐊 𝐉𝐎𝐈𝐍", callback_data="check_join"))
        bot.send_message(message.chat.id, JOIN_TEXT, reply_markup=markup)
    else:
        show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📤 𝐔𝐏𝐋𝐎𝐀𝐃𝐈𝐍𝐆 𝐅𝐈𝐋𝐄", callback_data="upload_mode")
    btn2 = types.InlineKeyboardButton("👨‍💻 𝐂𝐔𝐒𝐓𝐎𝐌𝐄𝐑 𝐂𝐀𝐑𝐄", url="https://t.me/adityapaswan") # Apna handle dal dena
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(chat_id, VIP_MENU, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "check_join":
        welcome(call.message)
    elif call.data == "upload_mode":
        bot.edit_message_text("*📥 𝐔𝐏𝐋𝐎𝐀𝐃 𝐘𝐎𝐔𝐑 𝐇𝐓𝐌𝐋 𝐅𝐈𝐋𝐄 𝐍𝐎𝐖\.\.\.*", call.message.chat.id, call.message.message_id)

@bot.message_handler(content_types=['document'])
def handle_file(message):
    if message.document.file_name.endswith('.html'):
        # Progress Bar Logic (10 Seconds total)
        msg = bot.send_message(message.chat.id, "⚙️ *𝐏𝐑𝐎𝐂𝐄𝐒𝐒𝐈𝐍𝐆: 𝟎%*")
        
        for i in range(10, 101, 10):
            time.sleep(1) # Har second 10% badhega (Total 10s)
            bar = "▓" * (i // 10) + "░" * (10 - (i // 10))
            bot.edit_message_text(f"⚡ *𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐈𝐍𝐆 𝐇𝐓𝐌𝐋\.\.\.*\n\n`{bar}` *{i}%*", message.chat.id, msg.message_id)

        # File Handling
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        content = downloaded_file.decode('utf-8', errors='ignore')
        
        # Automatic Decryption (Cleaning)
        decrypted = content.replace('eval(unescape(', '').replace('unescape(', '').replace('document.write(', '')
        
        file_name = f"𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐄𝐃_{message.document.file_name}"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(decrypted)

        with open(file_name, "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ *𝐅𝐈𝐋𝐄 𝐃𝐄𝐂𝐑𝐘𝐏𝐓𝐄𝐃 𝐁𝐘 𝐀𝐃𝐈𝐓𝐘𝐀 𝐏𝐀𝐒𝐖𝐀𝐍*")
        
        bot.delete_message(message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "❌ *𝐒𝐢𝐫𝐟 𝐇𝐓𝐌𝐋 𝐟𝐢𝐥𝐞 𝐛𝐡𝐞𝐣𝐞𝐢𝐧\!*")

bot.infinity_polling()
