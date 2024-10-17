from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
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

def is_admin(update: Update):
    user = update.effective_user
    chat = update.effective_chat
    if chat is None:
        return False
    member = chat.get_member(user.id)
    return member.status in ['administrator', 'creator']

def add_blacklist_word(update: Update, context: CallbackContext):
    if not is_admin(update):
        update.message.reply_text("Perintah ini hanya dapat digunakan oleh admin.")
        return

    if update.message.reply_to_message:
        word = update.message.reply_to_message.text.lower()
    elif context.args:
        word = " ".join(context.args).lower()
    else:
        update.message.reply_text("Cara penggunaan: /bl <kata> atau balas pesan yang mengandung kata tersebut.")
        return

    if word in blacklisted_words:
        update.message.reply_text(f"Kata '{word}' sudah ada dalam daftar blacklist.")
        return

    blacklisted_words.add(word)
    save_blacklisted_words(blacklisted_words)
    update.message.reply_text(f"Kata '{word}' telah ditambahkan ke daftar blacklist.")

def remove_blacklist_word(update: Update, context: CallbackContext):
    if not is_admin(update):
        update.message.reply_text("Perintah ini hanya dapat digunakan oleh admin.")
        return

    if update.message.reply_to_message:
        word = update.message.reply_to_message.text.lower()
    elif context.args:
        word = " ".join(context.args).lower()
    else:
        update.message.reply_text("Cara penggunaan: /ul <kata> atau balas pesan yang mengandung kata tersebut.")
        return

    if word not in blacklisted_words:
        update.message.reply_text(f"Kata '{word}' tidak ada dalam daftar blacklist.")
        return

    blacklisted_words.discard(word)
    save_blacklisted_words(blacklisted_words)
    update.message.reply_text(f"Kata '{word}' telah dikeluarkan dari daftar blacklist.")

def filter_blacklisted_words(update: Update, context: CallbackContext):
    chat = update.effective_chat
    if chat is None:
        return
    
    chat_id = chat.id
    if not is_subscription_active(chat_id):
        return

    message = update.message
    if message is None or message.text is None:
        return

    message_text = message.text.lower()

    for word in blacklisted_words:
        if word in message_text:
            try:
                message.delete()
                context.bot.send_message(chat_id=chat_id, text="Pesan Anda mengandung kata yang dilarang.")
                user_id = update.effective_user.id
                filterUser.blacklisted_users.add(user_id)
                filterUser.save_blacklisted_users(filterUser.blacklisted_users)
            except Exception as e:
                print(f"Error deleting message: {e}")
            break

def setup(dp):
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, filter_blacklisted_words))
    dp.add_handler(CommandHandler("bl", add_blacklist_word, Filters.chat_type.groups))
    dp.add_handler(CommandHandler("ul", remove_blacklist_word, Filters.chat_type.groups))
