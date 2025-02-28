import logging
import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from handlers import add_handlers

load_dotenv()

KEY = os.getenv("TELEGRAM_BOT_KEY")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(KEY).build()

    add_handlers(application)

    application.run_polling()
