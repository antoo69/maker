import logging
from telegram.ext import Updater, Dispatcher, ApplicationBuilder
from modules import setup_all_handlers
import config

logging.basicConfig(level=logging.INFO)

def main():
    """
    Fungsi utama untuk menjalankan bot Telegram.
    """
    # Create an application builder
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Create a dispatcher
    dispatcher = app.builder.dispatcher

    # Panggil fungsi setup_all_handlers dari modules/__init__.py
    setup_all_handlers(dispatcher)

    # Start the bot
    app.start_polling()

    # Run the bot until the user stops it
    app.idle()

if __name__ == '__main__':
    main()
