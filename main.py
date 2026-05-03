import telebot
from telebot import types
import time
import os

# --- CONFIG ---
# Tera Token yahan hai
API_TOKEN = '8694242868:AAHw4p485GwDHnWQlxa7szVT8oqQZEtSf44'
bot = telebot.TeleBot(API_TOKEN, parse_mode="MarkdownV2")

# --- UI DESIGN ---
START_TEXT = """
*╔══════════════════════╗*
* 👑 CHANNEL JOIN DECRYPT BOT 👑   *
*╚══════════════════════╝*

*Status:* 🟢 Online
*Developer:* [Aditya Paswan](https://t.me/adityapaswan)

✨ *Aapka swagat hai\!* File bhejo, main use 2 minute mein decrypt kar dunga\.
"""

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("✅ VERIFICATION", callback_data="verify")
    markup.add(btn1)
    bot.send_message(message.chat.id, START_TEXT, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify_user(call):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton("📤 UPLOAD FILE", callback_data="upload_mode")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="*✅ Verification Successful\!\n\nAb apni HTML file upload karein\.*",
        reply_markup=markup
    )

@bot.message_handler(content_types=['document'])
def process_file(message):
    if not message.document.file_name.endswith('.html'):
        bot.reply_to(message, "❌ *Error: Sirf \.html file bhejein\!*")
        return

    # Progress Bar (1 se 100 tak)
    prog_msg = bot.send_message(message.chat.id, "🔍 *Processing: 0%*")
    for i in range(10, 101, 20):
        time.sleep(1) # Processing speed
        bar = "▓" * (i // 10) + "░" * (10 - (i // 10))
        bot.edit_message_text(f"⚡ *Decrypting\.\.\.*\n\n`{bar}` *{i}%*", message.chat.id, prog_msg.message_id)

    # Decryption Logic
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    content = downloaded_file.decode('utf-8', errors='ignore')

    # Cleaning the HTML code
    clean_content = content.replace('eval(unescape(', '').replace('unescape(', '').replace('));', '')
    
    output_name = f"DECRYPTED_{message.document.file_name}"
    with open(output_name, "w", encoding="utf-8") as f:
        f.write(clean_content)

    # Sending back the file
    with open(output_name, "rb") as f:
        bot.send_document(message.chat.id, f, caption="✅ *File Decrypted By Aditya Paswan*")
    
    bot.delete_message(message.chat.id, prog_msg.message_id)

bot.infinity_polling()
    
