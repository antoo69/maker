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
            update.message.reply_text("Anda tidak memiliki izin untuk menggunakan perintah ini.")
            return  # Menambahkan return untuk menghentikan eksekusi fungsi
    return wrapper
