import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Replace with your actual tokens
TELEGRAM_TOKEN = '<telegram key>'
OPENAI_API_KEY = '<api key>'

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set up logging
logging.basicConfig(level=logging.INFO)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm your AI assistant. Ask me anything!")

# Message handler (for text messages)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"You are a helpful assistant. User says: {user_message}",
            max_tokens=100,
            temperature=0.7
        )
        reply = response.choices[0].text.strip()
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("❌ Sorry, something went wrong.")

# Set up the application
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# Run the bot
print("🤖 Bot is running...")
app.run_polling()
