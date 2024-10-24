from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, filters
from modules.subscription import is_subscription_active

blacklist = set()

def add_blacklist(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        blacklist.add(user.id)
        update.message.reply_text(f"{user.first_name} telah ditambahkan ke daftar hitam.")
    elif context.args:
        try:
            user_id = int(context.args[0])
            blacklist.add(user_id)
            update.message.reply_text(f"Pengguna dengan ID {user_id} telah ditambahkan ke daftar hitam.")
        except ValueError:
            update.message.reply_text("ID pengguna harus berupa angka.")
    else:
        update.message.reply_text("Penggunaan: /addblacklist <balas pesan> / <id_pengguna>")

def remove_blacklist(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        if user.id in blacklist:
            blacklist.remove(user.id)
            update.message.reply_text(f"{user.first_name} telah dihapus dari daftar hitam.")
        else:
            update.message.reply_text(f"{user.first_name} tidak ada dalam daftar hitam.")
    elif context.args:
        try:
            user_id = int(context.args[0])
            if user_id in blacklist:
                blacklist.remove(user_id)
                update.message.reply_text(f"Pengguna dengan ID {user_id} telah dihapus dari daftar hitam.")
            else:
                update.message.reply_text(f"Pengguna dengan ID {user_id} tidak ada dalam daftar hitam.")
        except ValueError:
            update.message.reply_text("ID pengguna harus berupa angka.")
    else:
        update.message.reply_text("Penggunaan: /removeblacklist <balas pesan> / <id_pengguna>")

def filter_message(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    if is_subscription_active(chat_id) and user_id in blacklist:
        try:
            update.message.delete()
        except Exception as e:
            print(f"Gagal menghapus pesan: {e}")

def setup(application):
    application.add_handler(CommandHandler("addblacklist", add_blacklist))
    application.add_handler(CommandHandler("removeblacklist", remove_blacklist))
    application.add_handler(MessageHandler(filters.ALL & filters.ChatType.GROUPS, filter_message))
