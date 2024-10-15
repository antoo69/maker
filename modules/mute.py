# modules/mute.py
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler
import json
import os
from database import is_subscription_active

MUTED_USERS_FILE = 'data/muted_users.json'

def load_muted_users():
    if os.path.exists(MUTED_USERS_FILE):
        with open(MUTED_USERS_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def save_muted_users(users):
    with open(MUTED_USERS_FILE, 'w') as f:
        json.dump(list(users), f, indent=4)

muted_users = load_muted_users()

def mute_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_subscription_active(chat_id):
        update.message.reply_text("Subscription tidak aktif. Hubungi owner untuk mengaktifkan bot.")
        return

    if not update.message.reply_to_message:
        update.message.reply_text("Balas pesan pengguna yang ingin dimute.")
        return

    user = update.message.reply_to_message.from_user
    muted_users.add(user.id)
    save_muted_users(muted_users)
    update.message.reply_text(f"Pengguna {user.first_name} telah dimute.")

def unmute_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_subscription_active(chat_id):
        update.message.reply_text("Subscription tidak aktif. Hubungi owner untuk mengaktifkan bot.")
        return

    if not update.message.reply_to_message:
        update.message.reply_text("Balas pesan pengguna yang ingin di-unmute.")
        return

    user = update.message.reply_to_message.from_user
    muted_users.discard(user.id)
    save_muted_users(muted_users)
    update.message.reply_text(f"Pengguna {user.first_name} telah di-unmute.")

def check_muted(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_subscription_active(chat_id):
        return

    user_id = update.effective_user.id
    if user_id in muted_users:
        try:
            update.message.delete()
            update.message.reply_text("Anda telah dimute dan tidak dapat mengirim pesan.")
        except Exception as e:
            print(f"Error deleting message: {e}")

def is_user_admin(update: Update):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Memeriksa apakah pengguna adalah admin di grup
    chat_member = update.effective_chat.get_member(user_id)
    return chat_member.status in ['administrator', 'creator']

def setup(dp):
    dp.add_handler(CommandHandler("mute", mute_user, Filters.reply & Filters.chat_type.groups & Filters.user(user_id=is_user_admin)))
    dp.add_handler(CommandHandler("unmute", unmute_user, Filters.reply & Filters.chat_type.groups & Filters.user(user_id=is_user_admin)))
    dp.add_handler(MessageHandler(Filters.all & ~Filters.command, check_muted))
