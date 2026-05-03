import telebot
from telebot import types
import re
import base64
import urllib.parse
import os
import time

# --- CONFIG ---
API_TOKEN = '8694242868:AAHw4p485GwDHnWQlxa7szVT8oqQZEtSf44'
bot = telebot.TeleBot(API_TOKEN)

# ASLI LINKS
LINKS = ["https://t.me/+_RZ0gN9HU6xhZTRl", "https://t.me/+7bNfhxLosYsxMmVl"]
OWNER_LINK = "https://t.me/ADITYAXVIPBOT"

# --- 🔥 HEAVY DECRYPTION ENGINE (FIXED) 🔥 ---
def heavy_decrypt(content):
    # Step 1: Extract hidden blocks from garbage
    # Ye wo "CjzxdH..." wale kachre ko dhoondh kar saaf karta hai
    for _ in range(30):
        old_content = content
        
        # Base64 Pattern matching
        b64_regex = r'[A-Za-z0-9+/]{50,}' 
        matches = re.findall(b64_regex, content)
        for block in matches:
            try:
                decoded = base64.b64decode(block).decode('utf-8', errors='ignore')
                if "<" in decoded or "var" in decoded: # Check if it's real code
                    content = content.replace(block, decoded)
            except: pass

        # Step 2: Hex & Unicode Clean
        content = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), content)
        content = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)
        
        # Step 3: Remove Protections
        content = content.replace('eval(unescape(', '').replace('eval(', '').replace('document.write(', '')

        if old_content == content: break
    return content

# --- 📥 FILE HANDLER (WITH 1-100% EFFECT) ---
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.file_name.lower().endswith('.html'):
        # Loading Effect
        m = bot.reply_to(message, "┌──────────────────────┐\n   🚀 DECRYPTING: 1%\n└──────────────────────┘")
        
        for p in [20, 50, 80, 100]:
            time.sleep(0.3)
            bot.edit_message_text(f"┌──────────────────────┐\n   🚀 DECRYPTING: {p}%\n└──────────────────────┘", message.chat.id, m.message_id)

        try:
            file_info = bot.get_file(message.document.file_id)
            data = bot.download_file(file_info.file_path).decode('utf-8', errors='ignore')
            
            # Asli Decryption Logic
            final_code = heavy_decrypt(data)

            # Save File
            new_file = f"DECRYPTED_{message.document.file_name}"
            with open(new_file, "w", encoding="utf-8") as f:
                f.write(final_code)
                
            with open(new_file, "rb") as f:
                # Clean Block Caption
                cap = (
                    "┌──────────────────────┐\n"
                    "   👑 HTML DECRYPTION DONE ✅\n"
                    "└──────────────────────┘\n\n"
                    "🎯 Channel 1:\n"
                    f"{LINKS[0]}\n\n"
                    "🎯 Channel 2:\n"
                    f"{LINKS[1]}"
                )
                bot.send_document(message.chat.id, f, caption=cap)
            
            bot.delete_message(message.chat.id, m.message_id)
            os.remove(new_file)
        except Exception as e:
            bot.edit_message_text(f"❌ ERROR: {str(e)}", message.chat.id, m.message_id)

# --- START & MENU ---
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎯 JOIN CHANNEL 1", url=LINKS[0]))
    markup.add(types.InlineKeyboardButton("🎯 JOIN CHANNEL 2", url=LINKS[1]))
    markup.add(types.InlineKeyboardButton("🔄 CHECK APPROVAL", callback_data="check"))
    
    msg = (
        "┌──────────────────────┐\n"
        "      👑 ADITYA X OWNER\n"
        "└──────────────────────┘\n\n"
        "⚠️ Access Denied! Please Join Both Channels."
    )
    bot.send_message(message.chat.id, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "check":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📤 UPLOAD HTML", callback_data="up"))
        markup.add(types.InlineKeyboardButton("👨‍💻 OWNER", url=OWNER_LINK))
        
        msg = (
            "┌──────────────────────┐\n"
            "   👑 VIP MENU ACTIVATED\n"
            "└──────────────────────┘\n\n"
            "System is Ready. Send File Now."
        )
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif call.data == "up":
        bot.send_message(call.message.chat.id, "🔮 PLEASE SEND YOUR HTML FILE")

bot.infinity_polling()
