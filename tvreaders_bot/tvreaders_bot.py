import os

import logging
import messages_text
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if not effective_chat:
        logger.warning('effective_chat is None')
    else:
        await context.bot.send_message(chat_id=effective_chat.id, text=messages_text.GREETINGS)


if __name__ == '__main__':
    if TELEGRAM_BOT_TOKEN:
        application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()
