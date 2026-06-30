import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# تنظیمات لاگ برای دیدن خطاها
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# گرفتن توکن از Environment Variable
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN پیدا نشد! مطمئن شو توی GitHub Secrets تنظیم شده.")


# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من ربات هوش مصنوعی تو هستم 🤖\n"
        "هر پیامی بفرستی، فعلاً همونو برات تکرار می‌کنم (تست اتصال)."
    )


# پاسخ Echo به هر پیام متنی
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logger.info(f"پیام دریافت شد: {user_message}")
    await update.message.reply_text(f"پیام تو: {user_message}")


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("ربات روشن شد و در حال گوش دادن به پیام‌هاست...")
    app.run_polling()


if __name__ == "__main__":
    main()
