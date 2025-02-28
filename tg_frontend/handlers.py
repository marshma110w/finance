from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def add_handlers(application) -> None:
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
