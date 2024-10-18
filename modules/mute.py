from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from modules.subscription import is_subscription_active

muted_users = []

def mute_user(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        muted_users.append(user.id)
        update.message.reply_text(f"{user.first_name} telah dimute.")
    elif context.args:
        try:
            user_id = int(context.args[0])
            muted_users.append(user_id)
            update.message.reply_text(f"User dengan ID {user_id} telah dimute.")
        except ValueError:
            update.message.reply_text("User ID harus berupa angka.")
    else:
        update.message.reply_text("Penggunaan: /mute <reply pesan> / <user_id>")

def unmute_user(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        if user.id in muted_users:
            muted_users.remove(user.id)
            update.message.reply_text(f"{user.first_name} telah di-unmute.")
        else:
            update.message.reply_text(f"{user.first_name} tidak dimute.")
    elif context.args:
        try:
            user_id = int(context.args[0])
            if user_id in muted_users:
                muted_users.remove(user_id)
                update.message.reply_text(f"User dengan ID {user_id} telah di-unmute.")
            else:
                update.message.reply_text(f"User dengan ID {user_id} tidak dimute.")
        except ValueError:
            update.message.reply_text("User ID harus berupa angka.")
    else:
        update.message.reply_text("Penggunaan: /unmute <reply pesan> / <user_id>")

def check_muted(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id
    if is_subscription_active(chat_id) and user_id in muted_users:
        update.message.delete()

def setup(dp):
    dp.add_handler(CommandHandler("mute", mute_user))
    dp.add_handler(CommandHandler("unmute", unmute_user))
    dp.add_handler(MessageHandler(Filters.all & Filters.chat_type.groups, check_muted))
