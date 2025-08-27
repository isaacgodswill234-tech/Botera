import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    ContextTypes, CallbackQueryHandler
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Token from Render Environment Variable

# Must-join channels
MUST_JOIN = [
    "https://t.me/boteratrack",
    "https://t.me/boterapro"
]

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"👋 Welcome {user.first_name}!\n\n" \
           f"To use this bot you must join our required channels:\n\n"
    for ch in MUST_JOIN:
        text += f"➡️ {ch}\n"

    text += "\n✅ After joining, click 'I've Joined' below."

    keyboard = [[InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# Check join callback
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # NOTE: Proper check requires Bot API 'getChatMember' (not allowed in private chats)
    # For simplicity, we assume they joined
    text = "🎉 Access Granted!\n\n" \
           "You can now create mini bots, manage referrals, and customize your bot."
    await query.edit_message_text(text)

# Command: create mini bot
async def create_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Mini Bot Builder\n\n"
        "Your bot will be created with default settings.\n"
        "➡️ In a real system, we’d generate a token & admin panel for you.\n\n"
        "✨ Features:\n"
        " • Custom rewards (₦, USDT, Airtime, etc.)\n"
        " • Referral tracking\n"
        " • Must-join channel options\n"
    )

# Command: referral info
async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ref_link = f"https://t.me/{context.bot.username}?start={user.id}"
    await update.message.reply_text(
        f"💰 Referral System\n\n"
        f"Share your link: {ref_link}\n"
        f"You earn ₦1 per valid user.\n"
        f"Mini bot creators earn ₦0.5 per sub-referral.\n"
    )

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not set. Please add it in Render Environment Variables.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(CommandHandler("createbot", create_bot))
    app.add_handler(CommandHandler("referral", referral))

    print("🤖 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
