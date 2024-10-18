from telegram.ext import Updater
from modules import filterUser, blacklistword, mute, antiflood, tagall, subscription
from helpers import owner_only
import config

def main():
    updater = Updater(token=config.TOKEN, use_context=True)
    dp = updater.dispatcher

    # Daftarkan semua modul
    filterUser.setup(dp)
    blacklistword.setup(dp)
    mute.setup(dp)
    antiflood.setup(dp)
    tagall.setup(dp)
    subscription.setup(dp)

    # Mulai bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
