import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# కొత్త బాట్ టోకెన్
BOT_TOKEN = "8948161372:AAERMx3jYYJCQg1zPtapWxmCW2QrR4bAR-s"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start కమాండ్ వచ్చినప్పుడు స్వాగత మెసేజ్ మరియు మెనూ చూపిస్తుంది."""
    user = update.effective_user
    welcome_text = (
        f"నమస్తే {user.first_name}! 👋\n\n"
        "మా స్మార్ట్ ఆటోమేషన్ బాట్‌కు స్వాగతం! 🤖\n"
        "ఈ బాట్ ద్వారా మీరు సేవలు, ఆర్డర్లు మరియు అప్‌డేట్‌లను పొందవచ్చు.\n\n"
        "కింది ఆప్షన్ల నుండి మీకు కావలసినదాన్ని ఎంచుకోండి:"
    )

    # Inline Keyboard Buttons (మెనూ బటన్లు)
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
    """బటన్ క్లిక్ చేసినప్పుడు సమాధానం ఇస్తుంది."""
    query = update.callback_query
    await query.answer()

    if query.data == "services":
        text = (
            "🛍️ **మా సేవలు & ఉత్పత్తులు:**\n\n"
            "• డిజిటల్ సేవలు మరియు బిజినెస్ ఆటోమేషన్\n"
            "• ఆరోగ్య మరియు ఉత్పత్తుల సమాచారం\n\n"
            "మరిన్ని వివరాలకు సంప్రదించండి!"
        )
    elif query.data == "subscription":
        text = (
            "💎 **ప్రీమియం సబ్స్క్రిప్షన్ వివరాలు:**\n\n"
            "• డైలీ స్పెషల్ అప్‌డేట్లు మరియు ఆఫర్లు\n"
            "• విఐపి గ్రూప్ యాక్సెస్\n\n"
            "సబ్స్క్రిప్షన్ తీసుకోవడానికి మమ్మల్ని సంప్రదించండి."
        )
    elif query.data == "ads":
        text = (
            "📢 **ప్రకటనలు & స్పాన్సర్‌షిప్‌లు:**\n\n"
            "మీ వ్యాపారాన్ని లేదా ఛానెల్‌ని మా బాట్ ద్వారా వేలాది మందికి ప్రమోట్ చేయాలనుకుంటే సంప్రదించండి."
        )
    elif query.data == "contact":
        text = "📞 **మమ్మల్ని సంప్రదించండి:**\n\nTelegram Bot: @Userinfo7_bot"
    elif query.data == "about":
        text = (
            "ℹ️ **Bot Status:** Fully Automated & Ready for Sale!\n"
            "Includes: Source Code + Database + Technical Support."
        )
    else:
        text = "చెల్లుబాటు కాని ఆప్షన్."

    back_button = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 వెనక్కి (Back)", callback_data="back_home")]])
    await query.edit_message_text(text, reply_markup=back_button, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/help కమాండ్ సహాయం."""
    await update.message.reply_text("సహాయం కోసం /start అని టైప్ చేసి మెనూ చూడండి.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(start, pattern="^back_home$"))
    app.add_handler(CallbackQueryHandler(button_click))

    print("Bot is running...")
    app.run_polling()
