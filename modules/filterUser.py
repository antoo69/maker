from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, CommandHandler
import json
import os
from database import is_subscription_active

BLACKLIST_USERS_FILE = 'data/blacklist_users.json'

def load_blacklisted_users():
    if os.path.exists(BLACKLIST_USERS_FILE):
        with open(BLACKLIST_USERS_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def save_blacklisted_users(users):
    with open(BLACKLIST_USERS_FILE, 'w') as f:
        json.dump(list(users), f, indent=4)

blacklisted_users = load_blacklisted_users()

def is_admin(update: Update) -> bool:
    user_id = update.effective_user.id
    chat = update.effective_chat
    member = chat.get_member(user_id)
    return member.status in ['administrator', 'creator']

def add_filter_command(update: Update, context: CallbackContext):
    if not is_admin(update):
        update.message.reply_text("Perintah ini hanya bisa digunakan oleh admin grup.")
        return
    
    if update.message.reply_to_message:
        # Tambahkan user yang dibalas ke dalam blacklist
        user_id = update.message.reply_to_message.from_user.id
        blacklisted_users.add(user_id)
        save_blacklisted_users(blacklisted_users)
        update.message.reply_text(f"User dengan ID {user_id} Berhasil di tambahkan kedalam database.")
    elif len(context.args) == 1:
        try:
            user_id = int(context.args[0])
        except ValueError:
            update.message.reply_text("User ID harus berupa angka.")
            return
        blacklisted_users.add(user_id)
        save_blacklisted_users(blacklisted_users)
        update.message.reply_text(f"User dengan ID {user_id} Berhasil di tambahkan kedalam database.")
    else:
        update.message.reply_text("Cara penggunaan: /af <user_id> atau balas pesan pengguna.")

def remove_filter_command(update: Update, context: CallbackContext):
    if not is_admin(update):
        update.message.reply_text("Perintah ini hanya bisa digunakan oleh admin grup.")
        return
    
    if update.message.reply_to_message:
        # Hapus user yang dibalas dari blacklist
        user_id = update.message.reply_to_message.from_user.id
        blacklisted_users.discard(user_id)
        save_blacklisted_users(blacklisted_users)
        update.message.reply_text(f"User dengan ID {user_id} Berhasil di keluarkan dari database.")
    elif len(context.args) == 1:
        try:
            user_id = int(context.args[0])
        except ValueError:
            update.message.reply_text("User ID harus berupa angka.")
            return
        blacklisted_users.discard(user_id)
        save_blacklisted_users(blacklisted_users)
        update.message.reply_text(f"User dengan ID {user_id} Berhasil di keluarkan dari database.")
    else:
        update.message.reply_text("Cara penggunaan: /rf <user_id> atau balas pesan pengguna.")

def filter_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_subscription_active(chat_id):
        return  # Jangan lakukan apa pun jika subscription tidak aktif

    user_id = update.effective_user.id
    if user_id in blacklisted_users:
        try:
            update.message.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")

def setup(dp):
    dp.add_handler(MessageHandler(Filters.all & ~Filters.command, filter_user))
    dp.add_handler(CommandHandler("af", add_filter_command))
    dp.add_handler(CommandHandler("rf", remove_filter_command))
