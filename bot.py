import os
import re
import logging
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_TOKEN = re.sub(r'[^\x20-\x7E]', '' ,TELEGRAM_TOKEN).strip()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN پیدا نشد!")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY پیدا نشد!")

client = Groq(api_key=GROQ_API_KEY)

chat_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من دستیار هوش مصنوعی توام 🤖\n"
        "هر سوالی داری بپرس!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_message = update.message.text
    logger.info(f"پیام از {user_id}: {user_message}")
    if user_id not in chat_histories:
        chat_histories[user_id] = []
    chat_histories[user_id].append({"role": "user", "content": user_message})
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_histories[user_id],
        )
        reply = response.choices[0].message.content
        chat_histories[user_id].append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply)
    except Exception as e:
        logger.error(f"خطا: {e}")
        await update.message.reply_text("مشکلی پیش اومد، دوباره امتحان کن.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("ربات با Groq روشن شد...")
    app.run_polling()

if __name__ == "__main__":
    main()

