from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, filters
from modules.subscription import is_subscription_active

blacklist_words = set()

def add_blacklist_word(update: Update, context: CallbackContext) -> None:
    word = " ".join(context.args)
    if word:
        blacklist_words.add(word.lower())
        update.message.reply_text(f"Kata '{word}' telah ditambahkan ke blacklist.")
    else:
        update.message.reply_text("Penggunaan: /addblacklistword <kata>")

def remove_blacklist_word(update: Update, context: CallbackContext) -> None:
    word = " ".join(context.args)
    if word:
        word_lower = word.lower()
        if word_lower in blacklist_words:
            blacklist_words.remove(word_lower)
            update.message.reply_text(f"Kata '{word}' telah dihapus dari blacklist.")
        else:
            update.message.reply_text(f"Kata '{word}' tidak ada dalam blacklist.")
    else:
        update.message.reply_text("Penggunaan: /removeblacklistword <kata>")

def check_blacklist_word(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    if update.message and update.message.text:
        message = update.message.text.lower()
        if is_subscription_active(chat_id) and any(word in message for word in blacklist_words):
            try:
                update.message.delete()
            except Exception as e:
                print(f"Gagal menghapus pesan: {e}")

def setup(application):
    application.add_handler(CommandHandler("addblacklistword", add_blacklist_word))
    application.add_handler(CommandHandler("removeblacklistword", remove_blacklist_word))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, check_blacklist_word))
