import telebot
from telebot import types
import re
import urllib.parse
import base64
import os

# --- CONFIG ---
API_TOKEN = '8694242868:AAHw4p485GwDHnWQlxa7szVT8oqQZEtSf44'
bot = telebot.TeleBot(API_TOKEN)

# ASLI TERE LINKS
LINKS = ["https://t.me/+_RZ0gN9HU6xhZTRl", "https://t.me/+7bNfhxLosYsxMmVl"]
OWNER_LINK = "https://t.me/ADITYAXVIPBOT"

# --- 🔥 ULTIMATE SOURCE UNPACKER (UI SAFE) 🔥 ---
def ultimate_unpacker(content):
    # Deep layer loop to crack complex encryption
    for _ in range(25):
        old_data = content
        
        # 1. Base64/atob Crack (Invisible replacement)
        b64_matches = re.findall(r'atob\s*\(\s*[\'"]([A-Za-z0-9+/=]{20,})[\'"]\s*\)', content)
        for b64 in b64_matches:
            try:
                decoded = base64.b64decode(b64).decode('utf-8', errors='ignore')
                content = content.replace(f'atob("{b64}")', f'"{decoded}"').replace(f"atob('{b64}')", f"'{decoded}'")
            except: pass

        # 2. Hex (\x) & Unicode (\u) Raw Fix
        content = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), content)
        content = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)
        
        # 3. URL Component Fix
        if "%" in content:
            content = urllib.parse.unquote(content)

        if old_data == content: break

    # Logic extraction (Bina UI bigade)
    content = content.replace('eval(unescape(', '').replace('eval(', '').replace('document.write(', '')
    return content

# --- 📥 FILE RECEIVING (FASTEST HANDLER) ---
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.file_name.lower().endswith('.html'):
        m = bot.reply_to(message, "⚡ **PRO-MAX DECRYPTION IN PROGRESS... 100%**")
        try:
            file_info = bot.get_file(message.document.file_id)
            data = bot.download_file(file_info.file_path).decode('utf-8', errors='ignore')
            
            # Execute Hard Decryption
            decrypted = ultimate_unpacker(data)
            
            # Save and Return
            new_file = f"DECRYPTED_ADITYA_{message.document.file_name}"
            with open(new_file, "w", encoding="utf-8") as f:
                f.write(decrypted)
                
            with open(new_file, "rb") as f:
                # Clean Block Style Caption
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
            bot.edit_message_text(f"❌ CRITICAL ERROR: {str(e)}", message.chat.id, m.message_id)
    else:
        bot.reply_to(message, "❌ BHEI SIRF HTML FILE BHEJEIN!")

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
        "⚠️ Access Denied! Dono channels join karein tabhi system kaam karega."
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
            "Ab aap file bhej sakte hain."
        )
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif call.data == "up":
        bot.send_message(call.message.chat.id, "🔮 **PLEASE SEND YOUR HTML FILE**")

bot.infinity_polling()
