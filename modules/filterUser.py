
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, filters
from modules.subscription import is_subscription_active

filtered_users = {}

def add_filter(update: Update, context: CallbackContext) -> None:
    if not context.args or len(context.args) < 2:
        update.message.reply_text("Penggunaan: /filter <user_id> <alasan>")
        return

    try:
        user_id = int(context.args[0])
        reason = " ".join(context.args[1:])
        chat_id = update.effective_chat.id

        if chat_id not in filtered_users:
            filtered_users[chat_id] = {}

        filtered_users[chat_id][user_id] = reason
        update.message.reply_text(f"Pengguna dengan ID {user_id} telah ditambahkan ke daftar filter dengan alasan: {reason}")
    except ValueError:
        update.message.reply_text("ID pengguna harus berupa angka.")

def remove_filter(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.message.reply_text("Penggunaan: /unfilter <user_id>")
        return

    try:
        user_id = int(context.args[0])
        chat_id = update.effective_chat.id

        if chat_id in filtered_users and user_id in filtered_users[chat_id]:
            del filtered_users[chat_id][user_id]
            update.message.reply_text(f"Pengguna dengan ID {user_id} telah dihapus dari daftar filter.")
        else:
            update.message.reply_text(f"Pengguna dengan ID {user_id} tidak ada dalam daftar filter.")
    except ValueError:
        update.message.reply_text("ID pengguna harus berupa angka.")

def list_filters(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    if chat_id in filtered_users and filtered_users[chat_id]:
        message = "Daftar pengguna yang difilter:\n\n"
        for user_id, reason in filtered_users[chat_id].items():
            message += f"ID: {user_id}, Alasan: {reason}\n"
        update.message.reply_text(message)
    else:
        update.message.reply_text("Tidak ada pengguna yang difilter dalam grup ini.")

def filter_message(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    if is_subscription_active(chat_id) and chat_id in filtered_users and user_id in filtered_users[chat_id]:
        try:
            update.message.delete()
        except Exception as e:
            print(f"Gagal menghapus pesan: {e}")

def setup(application):
    application.add_handler(CommandHandler("filter", add_filter))
    application.add_handler(CommandHandler("unfilter", remove_filter))
    application.add_handler(CommandHandler("filterlist", list_filters))
    application.add_handler(MessageHandler(filters.ALL & filters.ChatType.GROUPS, filter_message))
