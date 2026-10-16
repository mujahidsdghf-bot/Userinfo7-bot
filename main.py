import os
import logging
import sqlite3
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# .env ఫైల్ నుండి వేరియబుల్స్ లోడ్ చేయడం
load_dotenv()

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

# Render వెబ్ సర్వీస్ పోర్ట్ అవసరాలను తీర్చడానికి చిన్న వెబ్ సర్వర్
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is active and running successfully!")

def run_web_server():
    server_address = ('0.0.0.0', PORT)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f"Dummy web server running on port {PORT}")
    httpd.serve_forever()

# Database Setup (SQLite)
def init_db():
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name):
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)', 
                   (user_id, username, first_name))
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.first_name)
    
    welcome_text = (
        f"నమస్తే {user.first_name}! 👋\n\n"
        "మా స్మార్ట్ ఆటోమేషన్ బాట్‌కు స్వాగతం! 🤖\n"
        "ఈ బాట్ ద్వారా మీరు సేవలు, ఆర్డర్లు మరియు అప్‌డేట్‌లను పొందవచ్చు.\n\n"
        "కింది ఆప్షన్ల నుండి మీకు కావలసినదాన్ని ఎంచుకోండి:"
    )

    keyboard = [
        [
            InlineKeyboardButton("🛍️ సేవలు / ఉత్పత్తులు", callback_data="services"),
            InlineKeyboardButton("💎 ప్రీమియం సబ్స్క్రిప్షన్", callback_data="subscription")
        ],
        [
            InlineKeyboardButton("📢 ప్రకటనలు / Ads", callback_data="ads"),
            InlineKeyboardButton("📞 మమ్మల్ని సంప్రదించండి", callback_data="contact")
        ],
        [
            InlineKeyboardButton("ℹ️ బాట్ సమాచారం (Bot Info)", callback_data="about")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "services":
        text = "🛍️ **మా సేవలు & ఉత్పత్తులు:**\n\n• డిజిటల్ సేవలు మరియు బిజినెస్ ఆటోమేషన్\n• ఆరోగ్య మరియు ఉత్పత్తుల సమాచారం"
    elif query.data == "subscription":
        text = "💎 **ప్రీమియం సబ్స్క్రిప్షన్ వివరాలు:**\n\n• డైలీ స్పెషల్ అప్‌డేట్లు మరియు ఆఫర్లు\n• విఐపి గ్రూప్ యాక్సెస్"
    elif query.data == "ads":
        text = "📢 **ప్రకటనలు & స్పాన్సర్‌షిప్‌లు:**\n\nమీ వ్యాపారాన్ని మా బాట్ ద్వారా ప్రమోట్ చేయాలనుకుంటే సంప్రదించండి."
    elif query.data == "contact":
        text = "📞 **మమ్మల్ని సంప్రదించండి:**\n\nTelegram Bot: @userinfo17_bot"
    elif query.data == "about":
        text = "ℹ️ **Bot Status:** Fully Secured & Professional Source Code!"
    else:
        text = "చెల్లుబాటు కాని ఆప్షన్."

    back_button = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 వెనక్కి (Back)", callback_data="back_home")]])
    await query.edit_message_text(text, reply_markup=back_button, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("సహాయం కోసం /start అని టైప్ చేసి మెనూ చూడండి.")

def main():
    init_db()
    
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is missing!")
        return

    # వెబ్ సర్వర్ థ్రెడ్‌ను బ్యాక్‌గ్రౌండ్‌లో రన్ చేయడం
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()

    # Python 3.14 Compatible Event Loop Fix
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Application Build
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(start, pattern="^back_home$"))
    application.add_handler(CallbackQueryHandler(button_click))

    print("Bot is starting successfully...")
    application.run_polling()

if __name__ == '__main__':
    main()
