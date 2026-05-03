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

# TERE ASLI TELEGRAM LINKS
LINKS = ["https://t.me/+_RZ0gN9HU6xhZTRl", "https://t.me/+7bNfhxLosYsxMmVl"]
OWNER_LINK = "https://t.me/ADITYAXVIPBOT"

# --- 🔥 SMART UI-SAFE DECRYPTION 🔥 ---
def smart_decrypt(content):
    # File ke top pe tera credit link (Comment style takki design na bigde)
    my_credit = f"# CHANNEL 1: {LINKS[0]}\n# CHANNEL 2: {LINKS[1]}\n\n"
    
    # Check if content is already clean
    if "<html>" in content.lower() and "<script>" not in content:
        return my_credit + content

    # Deep layer unpacking for JS only
    for _ in range(50):
        old_data = content
        
        # 1. Base64 Cleaner (Sirf lambe encrypted blocks target karega)
        b64_pattern = r'[A-Za-z0-9+/]{50,}'
        for block in re.findall(b64_pattern, content):
            try:
                decoded = base64.b64decode(block).decode('utf-8', errors='ignore')
                # Sirf tab replace karega agar decoded code mein kaam ki cheez ho
                if any(kw in decoded for kw in ["var", "function", "document", "eval"]):
                    content = content.replace(block, decoded)
            except: pass

        # 2. Hex & Unicode Raw Fix
        content = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), content)
        content = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)
        
        # 3. URL Decode
        if "%" in content:
            content = urllib.parse.unquote(content)

        if old_data == content: break

    # UI PROTECTION: Eva aur document.write ko cleanup karega design chhede bina
    content = content.replace('eval(unescape(', '').replace('eval(', '').replace('document.write(', '')
    
    return my_credit + content

# --- 📥 FILE HANDLER (WITH 1-100% LOADING) ---
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.file_name.lower().endswith('.html'):
        # 1 to 100 Animation
        m = bot.reply_to(message, "┌──────────────────────┐\n   🚀 DECRYPTING: 1%\n└──────────────────────┘")
        
        for p in [25, 55, 85, 100]:
            time.sleep(0.3)
            bot.edit_message_text(f"┌──────────────────────┐\n   🚀 DECRYPTING: {p}%\n└──────────────────────┘", message.chat.id, m.message_id)

        try:
            file_info = bot.get_file(message.document.file_id)
            data = bot.download_file(file_info.file_path).decode('utf-8', errors='ignore')
            
            # Run Final Logic
            final_html = smart_decrypt(data)

            # Save File
            new_file = f"DECRYPTED_{message.document.file_name}"
            with open(new_file, "w", encoding="utf-8") as f:
                f.write(final_html)
                
            with open(new_file, "rb") as f:
                # Professional Block Caption
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
            "System Ready. Send File Now."
        )
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif call.data == "up":
        bot.send_message(call.message.chat.id, "🔮 PLEASE SEND YOUR HTML FILE")

bot.infinity_polling()
