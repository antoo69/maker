import logging
from telegram.ext import Updater
import config
import database
from modules import start, filterUser, blacklistword, mute, tagall, subscription
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

# Konfigurasi logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def notify_expiring_subscriptions(context):
    current_time = datetime.now()
    warning_time = current_time + timedelta(days=1)  # Notifikasi 1 hari sebelum berakhir
    subscriptions = database.get_all_subscriptions()
    for sub in subscriptions:
        chat_id, buyer_username, expiry_date_str = sub
        expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d %H:%M:%S')
        if current_time <= expiry_date <= warning_time:
            message = f"⚠️ **Subscription Anda akan berakhir pada {expiry_date.strftime('%Y-%m-%d')}**\nSilakan hubungi owner untuk memperpanjang."
            context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

def main():
    # Inisialisasi database
    database.init_db()

    # Inisialisasi Updater dan Dispatcher
    updater = Updater(config.TOKEN, use_context=True)
    dp = updater.dispatcher

    # Tambahkan handler dari modul
    start.setup(dp)
    filterUser.setup(dp)
    blacklistword.setup(dp)
    mute.setup(dp)
    tagall.setup(dp)
    subscription.setup(dp)

    # Setup scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(notify_expiring_subscriptions, 'interval', hours=24, args=[updater.job_queue])
    scheduler.start()

    # Start polling
    updater.start_polling()

    # Jalankan bot hingga Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
