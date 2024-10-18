from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from modules.subscription import is_subscription_active

blacklist_words = []

def add_blacklist_word(update: Update, context: CallbackContext):
    word = " ".join(context.args)
    if word:
        blacklist_words.append(word.lower())
        update.message.reply_text(f"Kata '{word}' telah ditambahkan ke blacklist.")
    else:
        update.message.reply_text("Penggunaan: /addblacklistword <kata>")

def remove_blacklist_word(update: Update, context: CallbackContext):
    word = " ".join(context.args)
    if word:
        if word.lower() in blacklist_words:
            blacklist_words.remove(word.lower())
            update.message.reply_text(f"Kata '{word}' telah dihapus dari blacklist.")
        else:
            update.message.reply_text(f"Kata '{word}' tidak ada dalam blacklist.")
    else:
        update.message.reply_text("Penggunaan: /removeblacklistword <kata>")

def check_blacklist_word(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = update.message.text.lower()
    if is_subscription_active(chat_id) and any(word in message for word in blacklist_words):
        update.message.delete()

def setup(dp):
    dp.add_handler(CommandHandler("addblacklistword", add_blacklist_word))
    dp.add_handler(CommandHandler("removeblacklistword", remove_blacklist_word))
    dp.add_handler(MessageHandler(Filters.text & Filters.chat_type.groups, check_blacklist_word))
