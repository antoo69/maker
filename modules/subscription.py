# modules/subscription.py
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, Filters
from database import add_subscription, remove_subscription, is_subscription_active, get_subscription
from datetime import datetime, timedelta
from .helpers import owner_only, dev_only
import config

@owner_only
@dev_only
def add_sub_command(update: Update, context: CallbackContext):
    if len(context.args) != 2:
        update.message.reply_text("Cara penggunaan: /addsub <chat_id/username> <durasi_hari>")
        return

    chat_id_or_username, duration_days = context.args

    if chat_id_or_username.isdigit():
        chat_id = int(chat_id_or_username)
    else:
        try:
            user = context.bot.get_chat(chat_id_or_username)
            chat_id = user.id
        except Exception as e:
            update.message.reply_text("Chat ID atau username tidak valid.")
            return

    buyer_username = f"@{update.message.from_user.username}" if update.message.from_user.username else "Unknown"

    add_subscription(chat_id, buyer_username, int(duration_days))

    expiry_date = datetime.now() + timedelta(days=int(duration_days))
    update.message.reply_text(f"Subscription ditambahkan untuk chat ID {chat_id} selama {duration_days} hari.\n"
                              f"Group ini masih memiliki durasi {duration_days} hari dan akan habis pada tanggal {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}.")

@owner_only
@dev_only
def remove_sub_command(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Cara penggunaan: /removesub <chat_id/username>")
        return

    chat_id_or_username = context.args[0]

    if chat_id_or_username.isdigit():
        chat_id = int(chat_id_or_username)
    else:
        try:
            user = context.bot.get_chat(chat_id_or_username)
            chat_id = user.id
        except Exception as e:
            update.message.reply_text("Chat ID atau username tidak valid.")
            return

    remove_subscription(chat_id)
    update.message.reply_text(f"Subscription dihapus untuk chat ID {chat_id}.")

@check_subscription
def subscription_status(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    subscription = get_subscription(chat_id)
    if subscription:
        expiry_date = subscription[2]
        remaining_days = (expiry_date - datetime.now()).days
        update.message.reply_text(f"Subscription Anda masih memiliki durasi {remaining_days} hari dan akan habis pada tanggal {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}.")
    else:
        update.message.reply_text("Anda tidak memiliki subscription aktif. Bot tidak dapat digunakan sampai subscription diaktifkan oleh owner atau developer.")

def check_subscription(func):
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        chat_id = update.effective_chat.id
        if is_subscription_active(chat_id):
            return func(update, context, *args, **kwargs)
        else:
            update.message.reply_text("Maaf, Anda tidak memiliki subscription aktif. Silakan hubungi owner atau developer untuk mengaktifkan bot.")
    return wrapper

def setup(dp):
    dp.add_handler(CommandHandler("addsub", add_sub_command))
    dp.add_handler(CommandHandler("removesub", remove_sub_command))
    dp.add_handler(CommandHandler("substatus", subscription_status))
