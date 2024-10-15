from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
import json
import os
from database import is_subscription_active
from modules import filterUser

BLACKLIST_WORDS_FILE = 'data/blacklist_words.json'

# Memuat daftar kata blacklist dari file
def load_blacklisted_words():
    if os.path.exists(BLACKLIST_WORDS_FILE):
        with open(BLACKLIST_WORDS_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

# Menyimpan kata blacklist ke file
def save_blacklisted_words(words):
    with open(BLACKLIST_WORDS_FILE, 'w') as f:
        json.dump(list(words), f, indent=4)

# Memuat daftar kata blacklist saat bot dijalankan
blacklisted_words = load_blacklisted_words()

# Memeriksa apakah pengguna adalah admin
def is_admin(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    return member.status in ['administrator', 'creator']

# Menambahkan kata ke blacklist dengan perintah /bl
def add_blacklist_word(update: Update, context: CallbackContext):
    if not is_admin(update, context):
        update.message.reply_text("Perintah ini hanya dapat digunakan oleh admin.")
        return

    if update.message.reply_to_message:
        # Tambahkan kata dari pesan yang di-reply ke blacklist
        word = update.message.reply_to_message.text.lower()
        blacklisted_words.add(word)
        save_blacklisted_words(blacklisted_words)
        update.message.reply_text(f"Kata '{word}' telah ditambahkan ke daftar blacklist melalui balasan pesan.")
    elif context.args:
        # Tambahkan kata dari argumen ke blacklist
        word = " ".join(context.args).lower()
        blacklisted_words.add(word)
        save_blacklisted_words(blacklisted_words)
        update.message.reply_text(f"Kata '{word}' telah ditambahkan ke daftar blacklist.")
    else:
        update.message.reply_text("Cara penggunaan: /bl <kata> atau balas pesan yang mengandung kata tersebut.")

# Menghapus kata dari blacklist dengan perintah /ul
def remove_blacklist_word(update: Update, context: CallbackContext):
    if not is_admin(update, context):
        update.message.reply_text("Perintah ini hanya dapat digunakan oleh admin.")
        return

    if update.message.reply_to_message:
        # Hapus kata dari pesan yang di-reply dari blacklist
        word = update.message.reply_to_message.text.lower()
        if word in blacklisted_words:
            blacklisted_words.discard(word)
            save_blacklisted_words(blacklisted_words)
            update.message.reply_text(f"Kata '{word}' telah dikeluarkan dari daftar blacklist melalui balasan pesan.")
        else:
            update.message.reply_text(f"Kata '{word}' tidak ada dalam daftar blacklist.")
    elif context.args:
        # Hapus kata dari argumen dari blacklist
        word = " ".join(context.args).lower()
        if word in blacklisted_words:
            blacklisted_words.discard(word)
            save_blacklisted_words(blacklisted_words)
            update.message.reply_text(f"Kata '{word}' telah dikeluarkan dari daftar blacklist.")
        else:
            update.message.reply_text(f"Kata '{word}' tidak ada dalam daftar blacklist.")
    else:
        update.message.reply_text("Cara penggunaan: /ul <kata> atau balas pesan yang mengandung kata tersebut.")

# Filter pesan untuk memeriksa apakah mengandung kata blacklist
def filter_blacklisted_words(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_subscription_active(chat_id):
        return  # Jangan lakukan apa pun jika subscription tidak aktif

    message_text = update.message.text.lower()

    print(f"Pesan diterima: {message_text}")  # Debug: cek pesan yang diterima

    for word in blacklisted_words:
        if word in message_text:
            try:
                print(f"Kata blacklist '{word}' ditemukan dalam pesan.")  # Debug: kata blacklist ditemukan
                update.message.delete()  # Menghapus pesan
                context.bot.send_message(chat_id=chat_id, text="Pesan Anda mengandung kata yang dilarang.")
                return  # Keluar setelah pesan dihapus
            except Exception as e:
                print(f"Error deleting message: {e}")
            # Opsional: Tambahkan user ke blacklist
            user_id = update.effective_user.id
            filterUser.blacklisted_users.add(user_id)
            filterUser.save_blacklisted_users(filterUser.blacklisted_users)
            break

# Setup handler untuk bot
def setup(dp):
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, filter_blacklisted_words))
    dp.add_handler(CommandHandler("bl", add_blacklist_word))
    dp.add_handler(CommandHandler("ul", remove_blacklist_word))
