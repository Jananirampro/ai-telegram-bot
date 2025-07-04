from dotenv import load_dotenv
import os
import logging
import openai
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

load_dotenv()

# 📋 Logs will be written ONLY to this file (nothing shown in console)
logging.basicConfig(
    filename="chat_logs.log",  # Customize the filename if you'd like
    filemode="a",              # "a" = append; use "w" to overwrite on each run
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# 🔑 OpenRouter API Key
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"


# 📌 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm your AI assistant powered by Cypher Alpha. Ask me anything!")

# 💬 Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"

    try:
        # Show typing action
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

        # Call OpenRouter (Cypher Alpha)
        response = openai.ChatCompletion.create(
            model="openrouter/cypher-alpha:free",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content.strip()

        # Send reply
        await update.message.reply_text(reply)

        # 📝 Log chat message
        logging.info(f"[User: {username} | ID: {user_id}] ➜ {user_message}")
        logging.info(f"[Bot] ➜ {reply}")

    except Exception as e:
        logging.error(f"OpenRouter API Error: {e}")
        await update.message.reply_text("❌ Something went wrong. Please try again later.")

# 🚀 Main app
def main():
    print("🚀 Bot is running... Press Ctrl+C to stop.")

# Log to file
    logging.info("✅ Telegram bot is starting...Logging has started successfully")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("🤖 Bot is running...")
    logging.info("✅ Telegram bot started successfully and is polling for messages.")
    app.run_polling()

if __name__ == "__main__":
    main()
