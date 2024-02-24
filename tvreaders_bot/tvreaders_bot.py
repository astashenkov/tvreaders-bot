import os

import logging
import messages_text
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from books import get_all_books


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


async def allbooks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if not effective_chat:
        logger.warning('effective_chat is None')
    else:
        all_books = await get_all_books()
        books_info = '\n'.join(f"{book.title} - {book.author}" for book in all_books)
        await context.bot.send_message(chat_id=effective_chat.id, text=books_info)


if __name__ == '__main__':
    if TELEGRAM_BOT_TOKEN:
        application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    allbooks_handler = CommandHandler('allbooks', allbooks)
    application.add_handler(start_handler)
    application.add_handler(allbooks_handler)
    
    application.run_polling()
