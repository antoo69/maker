# modules/helpers.py
from telegram import Update
from telegram.ext import CallbackContext
from functools import wraps
import config

def owner_only(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user = update.effective_user
        if user and user.id == config.OWNER_ID:
            return func(update, context, *args, **kwargs)
        else:
            if update.message:
                update.message.reply_text("Anda tidak memiliki izin untuk menggunakan perintah ini.")
            elif update.callback_query:
                update.callback_query.answer("Anda tidak memiliki izin untuk menggunakan perintah ini.")
    return wrapper

def admin_only(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user = update.effective_user
        chat = update.effective_chat
        if chat and user:
            member = chat.get_member(user.id)
            if member.status in ['administrator', 'creator']:
                return func(update, context, *args, **kwargs)
        if update.message:
            update.message.reply_text("Perintah ini hanya dapat digunakan oleh admin.")
        elif update.callback_query:
            update.callback_query.answer("Perintah ini hanya dapat digunakan oleh admin.")
    return wrapper
