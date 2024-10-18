from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from modules.subscription import is_subscription_active

blacklist = []

def add_blacklist(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        blacklist.append(user.id)
        update.message.reply_text(f"{user.first_name} telah ditambahkan ke blacklist.")
    elif context.args:
        try:
            user_id = int(context.args[0])
            blacklist.append(user_id)
            update.message.reply_text(f"User dengan ID {user_id} telah ditambahkan ke blacklist.")
        except ValueError:
            update.message.reply_text("User ID harus berupa angka.")
    else:
        update.message.reply_text("Penggunaan: /addblacklist <reply pesan> / <user_id>")

def remove_blacklist(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        if user.id in blacklist:
            blacklist.remove(user.id)
            update.message.reply_text(f"{user.first_name} telah dihapus dari blacklist.")
        else:
            update.message.reply_text(f"{user.first_name} tidak ada dalam blacklist.")
    elif context.args:
        try:
            user_id = int(context.args[0])
            if user_id in blacklist:
                blacklist.remove(user_id)
                update.message.reply_text(f"User dengan ID {user_id} telah dihapus dari blacklist.")
            else:
                update.message.reply_text(f"User dengan ID {user_id} tidak ada dalam blacklist.")
        except ValueError:
            update.message.reply_text("User ID harus berupa angka.")
    else:
        update.message.reply_text("Penggunaan: /removeblacklist <reply pesan> / <user_id>")

def check_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id
    if is_subscription_active(chat_id) and user_id in blacklist:
        update.message.delete()

def setup(dp):
    dp.add_handler(CommandHandler("addblacklist", add_blacklist))
    dp.add_handler(CommandHandler("removeblacklist", remove_blacklist))
    dp.add_handler(MessageHandler(Filters.all & Filters.chat_type.groups, check_message))
