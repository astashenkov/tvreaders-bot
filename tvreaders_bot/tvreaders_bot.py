import os

import logging
import messages_text
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from books import get_all_books, get_current_book


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if not effective_chat:
        logger.warning('effective_chat is None in start function')
    else:
        await context.bot.send_message(chat_id=effective_chat.id, text=messages_text.GREETINGS)


async def all_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if not effective_chat:
        logger.warning('effective_chat is None in all_books function')
    else:
        all_books = await get_all_books()
        books_info = '\n'.join(f"{index+1}. {book.title} - {book.author}" for index, book in enumerate(all_books))
        await context.bot.send_message(chat_id=effective_chat.id, text=books_info)


async def current_book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if not effective_chat:
        logger.warning('effective_chat is None in current_book function')
    else:
        current_book_info = await get_current_book()
        if current_book_info:
            current_book_description = f'Readers Club is currently reading the book "{current_book_info.title}"'
            current_book_description += f' which was written by {current_book_info.author}.'
            current_book_description += f' This book was proposed by {current_book_info.host}.\n\n'
            current_book_description += "Don't forget that you can choose your next book by voting."
        else:
            current_book_description = 'Sorry, there is no book currently being read.'
        await context.bot.send_message(chat_id=effective_chat.id, text=current_book_description)
        

if __name__ == '__main__':

    if TELEGRAM_BOT_TOKEN:
        application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    allbooks_handler = CommandHandler('allbooks', all_books)
    current_book_handler = CommandHandler('now', current_book)
    application.add_handler(start_handler)
    application.add_handler(allbooks_handler)
    application.add_handler(current_book_handler)

    application.run_polling()
