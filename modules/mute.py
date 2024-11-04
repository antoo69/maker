from telegram import Update, ChatPermissions, Bot
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, filters
from telegram.error import BadRequest
from modules.subscription import is_subscription_active
import time

bot = Bot('7536984860:AAETJTVKhHAzRAKG8XZjp0gyqjSXuLTp16s')

def mute_user(update: Update, context: CallbackContext):
    if not is_subscription_active(update.effective_user.id):
        update.message.reply_text("Anda tidak memiliki izin untuk menggunakan perintah ini.")
        return

    chat_id = update.effective_chat.id
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        user_id = user.id
    elif context.args:
        try:
            user_id = int(context.args[0])
        except ValueError:
            update.message.reply_text("ID pengguna harus berupa angka.")
            return
    else:
        update.message.reply_text("Penggunaan: /mute <reply pesan> atau /mute <user_id> <durasi> <satuan>")
        return

    duration = 0
    if len(context.args) >= 3:
        try:
            duration = int(context.args[1])
            unit = context.args[2].lower()
            if unit in ['m', 'menit']:
                duration *= 60
            elif unit in ['j', 'jam']:
                duration *= 3600
            elif unit in ['h', 'hari']:
                duration *= 86400
        except ValueError:
            update.message.reply_text("Format durasi tidak valid.")
            return

    try:
        bot.restrict_chat_member(
            chat_id,
            user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=time.time() + duration if duration > 0 else None
        )
        if duration > 0:
            update.message.reply_text(f"Pengguna telah dibisukan selama {duration//60} menit.")
        else:
            update.message.reply_text("Pengguna telah dibisukan.")
    except BadRequest as e:
        update.message.reply_text(f"Gagal membisukan pengguna: {str(e)}")

def unmute_user(update: Update, context: CallbackContext):
    if not is_subscription_active(update.effective_user.id):
        update.message.reply_text("Anda tidak memiliki izin untuk menggunakan perintah ini.")
        return

    chat_id = update.effective_chat.id
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        user_id = user.id
    elif context.args:
        try:
            user_id = int(context.args[0])
        except ValueError:
            update.message.reply_text("ID pengguna harus berupa angka.")
            return
    else:
        update.message.reply_text("Penggunaan: /unmute <reply pesan> atau /unmute <user_id>")
        return

    try:
        bot.restrict_chat_member(
            chat_id,
            user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_invite_users=True
            )
        )
        update.message.reply_text("Pengguna telah diizinkan berbicara kembali.")
    except BadRequest as e:
        update.message.reply_text(f"Gagal mengizinkan pengguna berbicara: {str(e)}")

def setup(application):
    application.add_handler(CommandHandler("mute", mute_user))
    application.add_handler(CommandHandler("unmute", unmute_user))
