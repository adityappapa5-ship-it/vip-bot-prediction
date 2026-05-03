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

# --- 🔥 ULTRA-SECURE UI SAFE DECRYPTOR 🔥 ---
def final_fixed_decrypt(content):
    # Deep layer unpacking bina design tode
    for _ in range(20):
        old_data = content
        
        # 1. Base64/atob Detection & Fix
        b64_matches = re.findall(r'atob\s*\(\s*[\'"]([A-Za-z0-9+/=]{20,})[\'"]\s*\)', content)
        for b64 in b64_matches:
            try:
                decoded = base64.b64decode(b64).decode('utf-8', errors='ignore')
                content = content.replace(f'atob("{b64}")', f'"{decoded}"').replace(f"atob('{b64}')", f"'{decoded}'")
            except: pass

        # 2. Hex (\x) & Unicode (\u) Clean
        content = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), content)
        content = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)
        
        # 3. Smart URL Decode
        if "%" in content:
            content = urllib.parse.unquote(content)

        if old_data == content: break

    # UI/Design preservation: Sirf execute logic bypass karo
    content = content.replace('eval(unescape(', '').replace('eval(', '').replace('document.write(', '')
    return content

# --- 📥 FILE RECEIVER (PRIORITY #1) ---
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.file_name.lower().endswith('.html'):
        m = bot.reply_to(message, "⚡ **Decrypting File... 100% Fixed Logic!**")
        try:
            file_info = bot.get_file(message.document.file_id)
            data = bot.download_file(file_info.file_path).decode('utf-8', errors='ignore')
            
            # Execute Decryption (UI Safe)
            decrypted = final_fixed_decrypt(data)
            
            # Save File
            new_file = f"DECRYPTED_{message.document.file_name}"
            with open(new_file, "w", encoding="utf-8") as f:
                f.write(decrypted)
                
            with open(new_file, "rb") as f:
                cap = f"👑 **HTML DECRYPTION DONE** ✅\n\n🔐 **Channel 1:** {LINKS[0]}\n🔐 **Channel 2:** {LINKS[1]}"
                bot.send_document(message.chat.id, f, caption=cap)
            
            bot.delete_message(message.chat.id, m.message_id)
            os.remove(new_file)
        except Exception as e:
            bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, m.message_id)
    else:
        bot.reply_to(message, "❌ Sirf HTML file bhein.")

# --- START & MENU ---
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✨ JOIN CHANNEL 1", url=LINKS[0]))
    markup.add(types.InlineKeyboardButton("✨ JOIN CHANNEL 2", url=LINKS[1]))
    markup.add(types.InlineKeyboardButton("🔄 CHECK APPROVAL", callback_data="check"))
    
    bot.send_message(message.chat.id, f"👑 **ADITYA X OWNER**\n\n⚠️ Access Denied! Dono channels join karein tabhi file upload option aayega.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "check":
        # Direct allow (Bina admin check ke taaki fast kaam kare)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📤 UPLOAD HTML", callback_data="up"))
        markup.add(types.InlineKeyboardButton("👨‍💻 OWNER", url=OWNER_LINK))
        bot.edit_message_text("👑 **VIP MENU ACTIVATED!**\n\nAb aap encrypted file bhej sakte hain.", call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif call.data == "up":
        bot.send_message(call.message.chat.id, "📥 **Ab apni Encrypted HTML file yahan bhej de.**")

bot.infinity_polling()
