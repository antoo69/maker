from telegram import Update
from telegram.ext import CallbackContext
import json
import os
import threading
from database import is_subscription_active

BLACKLIST_USERS_FILE = 'data/blacklist_users.json'

def load_blacklisted_users():
    """Memuat daftar pengguna yang di-blacklist dari file."""
    if os.path.exists(BLACKLIST_USERS_FILE):
        with open(BLACKLIST_USERS_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def save_blacklisted_users(users):
    """Menyimpan daftar pengguna yang di-blacklist ke file."""
    with open(BLACKLIST_USERS_FILE, 'w') as f:
        json.dump(list(users), f, indent=4)

blacklisted_users = load_blacklisted_users()

def is_admin(update: Update) -> bool:
    """Memeriksa apakah pengguna yang menjalankan perintah adalah admin grup."""
    user_id = update.effective_user.id
    chat = update.effective_chat
    member = chat.get_member(user_id)
    return member.status in ['administrator', 'creator']

def delete_message_later(context: CallbackContext, message_id: int, chat_id: int, delay: int):
    """Menghapus pesan setelah jeda waktu tertentu."""
    threading.Timer(delay, lambda: context.bot.delete_message(chat_id=chat_id, message_id=message_id)).start()

def add_filter_command(update: Update, context: CallbackContext):
    """Menambahkan pengguna ke blacklist."""
    if not is_admin(update):
        msg = update.message.reply_text("Perintah ini hanya bisa digunakan oleh admin grup.")
        delete_message_later(context, msg.message_id, update.effective_chat.id, 5)
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        blacklisted_users.add(user_id)
        save_blacklisted_users(blacklisted_users)
        msg = update.message.reply_text(f"User dengan ID {user_id} berhasil ditambahkan ke dalam blacklist.")
    elif len(context.args) == 1:
        try:
            user_id = int(context.args[0])
        except ValueError:
            msg = update.message.reply_text("User ID harus berupa angka.")
            delete_message_later(context, msg.message_id, update.effective_chat.id, 5)
            return
        blacklisted_users.add(user_id)
        save_blacklisted_users(blacklisted_users)
        msg = update.message.reply_text(f"User dengan ID {user_id} berhasil ditambahkan ke dalam blacklist.")
    else:
        msg = update.message.reply_text("Cara penggunaan: /af <user_id> atau balas pesan pengguna.")
        delete_message_later(context, msg.message_id, update.effective_chat.id, 5)
        return

    # Menghapus balasan bot secara otomatis setelah 5 detik
    delete_message_later(context, msg.message_id, update.effective_chat.id, 5)

def remove_filter_command(update: Update, context: CallbackContext):
    """Menghapus pengguna dari blacklist."""
    if not is_admin(update):
        msg = update.message.reply_text("Perintah ini hanya bisa digunakan oleh admin grup.")
        delete_message_later(context, msg.message_id, update.effective_chat.id, 5)
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        blacklisted_users.discard(user_id)
        save_blacklisted_users(blacklisted_users)
        msg = update.message.reply_text(f"User dengan ID {user_id} berhasil dihapus dari blacklist.")
    elif len(context.args) == 1:
        try:
            user_id = int(context.args[0])
        except ValueError:
            msg = update.message.reply_text("User ID harus berupa angka.")
            delete_message_later(context, msg.message_id, update.effective_chat.id, 5)
            return
        blacklisted_users.discard(user_id)
        save_blacklisted_users(blacklisted_users)
        msg = update.message.reply_text(f"User dengan ID {user_id} berhasil dihapus dari blacklist.")
    else:
        msg = update.message.reply_text("Cara penggunaan: /rf <user_id> atau balas pesan pengguna.")
        delete_message_later(context, msg.message_id, update.effective_chat.id, 5)
        return

    # Menghapus balasan bot secara otomatis setelah 5 detik
    delete_message_later(context, msg.message_id, update.effective_chat.id, 5)

def filter_user(update: Update, context: CallbackContext):
    """Memfilter pesan dari pengguna yang ada di blacklist."""
    chat_id = update.effective_chat.id
    if not is_subscription_active(chat_id):
        return  # Tidak lakukan apa pun jika subscription tidak aktif

    user_id = update.effective_user.id
    if user_id in blacklisted_users:
        try:
            update.message.delete()  # Menghapus pesan dari pengguna yang di-blacklist
        except Exception as e:
            print(f"Error deleting message: {e}")

def setup(dp):
    """Mendaftarkan handler untuk perintah dan filter."""
    dp.add_handler(MessageHandler(Filters.all & ~Filters.command, filter_user))
    dp.add_handler(CommandHandler("af", add_filter_command))  # /af untuk menambahkan blacklist
    dp.add_handler(CommandHandler("rf", remove_filter_command))  # /rf untuk menghapus blacklist
