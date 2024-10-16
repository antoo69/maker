from telegram import Update, ChatPermissions
from telegram.ext import CallbackContext, CommandHandler, Filters
from datetime import timedelta
from database import is_subscription_active
import threading

# Fungsi untuk menghapus pesan setelah beberapa detik
def delete_message_later(context: CallbackContext, message_id: int, chat_id: int, delay: int):
    threading.Timer(delay, lambda: context.bot.delete_message(chat_id=chat_id, message_id=message_id)).start()

# Fungsi untuk mendapatkan user ID berdasarkan username
def get_user_id_by_username(context: CallbackContext, username: str):
    try:
        user = context.bot.get_chat(username)
        return user.id
    except Exception as e:
        return None

# Fungsi untuk membatasi pengguna (mute)
def mute_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if not is_subscription_active(chat_id):
        msg = update.message.reply_text("Subscription tidak aktif. Hubungi owner untuk mengaktifkan bot.")
        delete_message_later(context, msg.message_id, chat_id, 5)
        return

    if not update.effective_user.status in ['administrator', 'creator']:
        msg = update.message.reply_text("Perintah ini hanya bisa digunakan oleh admin grup.")
        delete_message_later(context, msg.message_id, chat_id, 5)
        return

    # Menggunakan reply atau username/user ID
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    elif len(context.args) == 1:
        target = context.args[0]
        if target.isdigit():
            user_id = int(target)
        else:
            user_id = get_user_id_by_username(context, target)

        if user_id is None:
            msg = update.message.reply_text("Username atau ID pengguna tidak valid.")
            delete_message_later(context, msg.message_id, chat_id, 5)
            return
        user = context.bot.get_chat(user_id)
    else:
        msg = update.message.reply_text("Balas pesan pengguna atau masukkan username/ID pengguna.")
        delete_message_later(context, msg.message_id, chat_id, 5)
        return

    # Mute pengguna dengan membatasi semua izin kecuali melihat pesan
    try:
        context.bot.restrict_chat_member(
            chat_id,
            user.id,
            ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False, can_add_web_page_previews=False)
        )
        msg = update.message.reply_text(f"Pengguna {user.first_name} telah dimute.")
        delete_message_later(context, msg.message_id, chat_id, 5)
    except Exception as e:
        msg = update.message.reply_text(f"Gagal memute pengguna: {e}")
        delete_message_later(context, msg.message_id, chat_id, 5)

# Fungsi untuk mengembalikan izin pengguna (unmute)
def unmute_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if not is_subscription_active(chat_id):
        msg = update.message.reply_text("Subscription tidak aktif. Hubungi owner untuk mengaktifkan bot.")
        delete_message_later(context, msg.message_id, chat_id, 5)
        return

    if not update.effective_user.status in ['administrator', 'creator']:
        msg = update.message.reply_text("Perintah ini hanya bisa digunakan oleh admin grup.")
        delete_message_later(context, msg.message_id, chat_id, 5)
        return

    # Menggunakan reply atau username/user ID
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    elif len(context.args) == 1:
        target = context.args[0]
        if target.isdigit():
            user_id = int(target)
        else:
            user_id = get_user_id_by_username(context, target)

        if user_id is None:
            msg = update.message.reply_text("Username atau ID pengguna tidak valid.")
            delete_message_later(context, msg.message_id, chat_id, 5)
            return
        user = context.bot.get_chat(user_id)
    else:
        msg = update.message.reply_text("Balas pesan pengguna atau masukkan username/ID pengguna.")
        delete_message_later(context, msg.message_id, chat_id, 5)
        return

    # Kembalikan izin pengguna (unmute)
    try:
        context.bot.restrict_chat_member(
            chat_id,
            user.id,
            ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        )
        msg = update.message.reply_text(f"Pengguna {user.first_name} telah di-unmute.")
        delete_message_later(context, msg.message_id, chat_id, 5)
    except Exception as e:
        msg = update.message.reply_text(f"Gagal mengunmute pengguna: {e}")
        delete_message_later(context, msg.message_id, chat_id, 5)

# Setup handler untuk mute dan unmute
def setup(dp):
    dp.add_handler(CommandHandler("mute", mute_user, Filters.chat_type.groups))
    dp.add_handler(CommandHandler("unmute", unmute_user, Filters.chat_type.groups))
