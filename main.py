from telegram.ext import Updater
from modules import setup_all_handlers
import config

def main():
    # Buat updater dan dispatcher menggunakan token bot dari config.py
    updater = Updater(token=config.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Panggil fungsi setup_all_handlers dari modules/__init__.py
    setup_all_handlers(dp)

    # Mulai polling untuk menerima pesan dari Telegram
    updater.start_polling()

    # Berhenti hanya jika ada perintah manual untuk stop bot
    updater.idle()

if __name__ == '__main__':
    main()
