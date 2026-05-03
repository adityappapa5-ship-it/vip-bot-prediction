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

# TERE ASLI LINKS
LINKS = ["https://t.me/+_RZ0gN9HU6xhZTRl", "https://t.me/+7bNfhxLosYsxMmVl"]
OWNER_LINK = "https://t.me/ADITYAXVIPBOT"

# --- 🔥 ULTRA DEEP DECRYPTION (UI SAFE) 🔥 ---
def ultra_deep_decrypt(content):
    # Aapka Credit Link jo top pe jayega
    header_credit = f"\n"
    
    # Deep cleaning loop
    for _ in range(40):
        old_data = content
        
        # 1. Base64 Multi-Layer Extract
        b64_regex = r'[A-Za-z0-9+/]{40,}'
        for block in re.findall(b64_regex, content):
            try:
                decoded = base64.b64decode(block).decode('utf-8', errors='ignore')
                if any(x in decoded for x in ["<", "var", "function", "div"]):
                    content = content.replace(block, decoded)
            except: pass

        # 2. Hex & Unicode Fix
        content = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), content)
        content = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)
        
        # 3. URL Unescape
        if "%" in content:
            content = urllib.parse.unquote(content)

        if old_data == content: break

    # UI Cleanup: Sirf protection wrappers hatana, design nahi
    content = content.replace('eval(unescape(', '').replace('eval(', '').replace('document.write(', '')
    
    return header_credit + content

# --- 📥 FILE HANDLER ---
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.file_name.lower().endswith('.html'):
        # 1 to 100 Tik-Tik Effect
        m = bot.reply_to(message, "┌──────────────────────┐\n   🚀 DECRYPTING: 1%\n└──────────────────────┘")
        
        steps = [30, 65, 90, 100]
        for p in steps:
            time.sleep(0.3)
            bot.edit_message_text(f"┌──────────────────────┐\n   🚀 DECRYPTING: {p}%\n└──────────────────────┘", message.chat.id, m.message_id)

        try:
            file_info = bot.get_file(message.document.file_id)
            data = bot.download_file(file_info.file_path).decode('utf-8', errors='ignore')
            
            # Execute Final Logic
            final_code = ultra_deep_decrypt(data)

            # Save and Send
            new_file = f"DECRYPTED_{message.document.file_name}"
            with open(new_file, "w", encoding="utf-8") as f:
                f.write(final_code)
                
            with open(new_file, "rb") as f:
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
            "System Ready. Send Your HTML File Now."
        )
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif call.data == "up":
        bot.send_message(call.message.chat.id, "🔮 PLEASE SEND YOUR HTML FILE")

bot.infinity_polling()
                     
