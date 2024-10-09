# modules/subscription.py
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, Filters
from database import add_subscription, remove_subscription, is_subscription_active, get_subscription
from datetime import datetime
from .helpers import owner_only
import config

@owner_only
def add_sub_command(update: Update, context: CallbackContext):
    if len(context.args) != 2:
        update.message.reply_text("Cara penggunaan: /addsub <chat_id> <durasi_hari>")
        return

    try:
        chat_id = int(context.args[0])
        duration_days = int(context.args[1])
    except ValueError:
        update.message.reply_text("Chat ID dan durasi hari harus berupa angka.")
        return

    buyer_username = f"@{update.message.from_user.username}" if update.message.from_user.username else "Unknown"

    add_subscription(chat_id, buyer_username, duration_days)
    update.message.reply_text(f"Subscription ditambahkan untuk chat ID {chat_id} selama {duration_days} hari.")

@owner_only
def remove_sub_command(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Cara penggunaan: /removesub <chat_id>")
        return

    try:
        chat_id = int(context.args[0])
    except ValueError:
        update.message.reply_text("Chat ID harus berupa angka.")
        return

    remove_subscription(chat_id)
    update.message.reply_text(f"Subscription dihapus untuk chat ID {chat_id}.")

def subscription_status(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    subscription = get_subscription(chat_id)
    if subscription:
        expiry_date = subscription[2]
        update.message.reply_text(f"Subscription Anda akan berakhir pada: {expiry_date}")
    else:
        update.message.reply_text("Anda tidak memiliki subscription aktif.")

def setup(dp):
    dp.add_handler(CommandHandler("addsub", add_sub_command))
    dp.add_handler(CommandHandler("removesub", remove_sub_command))
    dp.add_handler(CommandHandler("substatus", subscription_status))
