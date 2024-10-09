# modules/blacklistword.py
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters
import json
import os
from database import is_subscription_active
from modules import filterUser

BLACKLIST_WORDS_FILE = 'data/blacklist_words.json'

def load_blacklisted_words():
    if os.path.exists(BLACKLIST_WORDS_FILE):
        with open(BLACKLIST_WORDS_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def save_blacklisted_words(words):
    with open(BLACKLIST_WORDS_FILE, 'w') as f:
        json.dump(list(words), f, indent=4)

blacklisted_words = load_blacklisted_words()

def filter_blacklisted_words(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_subscription_active(chat_id):
        return  # Jangan lakukan apa pun jika subscription tidak aktif

    message_text = update.message.text.lower()
    for word in blacklisted_words:
        if word in message_text:
            try:
                update.message.delete()
                update.message.reply_text("Pesan Anda mengandung kata yang dilarang.")
            except Exception as e:
                print(f"Error deleting message: {e}")
            # Opsional: Menambahkan pengguna ke blacklist
            user_id = update.effective_user.id
            filterUser.blacklisted_users.add(user_id)
            filterUser.save_blacklisted_users(filterUser.blacklisted_users)
            break

def setup(dp):
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, filter_blacklisted_words))
