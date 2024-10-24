
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, filters
import time

# Variabel untuk menyimpan konfigurasi antiflood per grup
antiflood_config = {}

def set_antiflood(update: Update, context: CallbackContext):
    """Mengatur konfigurasi antiflood untuk grup."""
    chat_id = str(update.effective_chat.id)
    args = context.args
    
    if len(args) != 2:
        update.message.reply_text("Penggunaan: /setflood [jumlah] [waktu dalam detik]")
        return
    
    try:
        limit = int(args[0])
        time_window = int(args[1])
        if limit < 1 or time_window < 1:
            raise ValueError
    except ValueError:
        update.message.reply_text("Masukkan angka yang valid untuk jumlah pesan dan waktu.")
        return
    
    antiflood_config[chat_id] = {
        'limit': limit,
        'time_window': time_window,
        'user_messages': {}
    }
    update.message.reply_text(f"Antiflood diatur: {limit} pesan dalam {time_window} detik.")

def disable_antiflood(update: Update, context: CallbackContext):
    """Menonaktifkan antiflood untuk grup."""
    chat_id = str(update.effective_chat.id)
    if chat_id in antiflood_config:
        del antiflood_config[chat_id]
        update.message.reply_text("Antiflood dinonaktifkan di grup ini.")
    else:
        update.message.reply_text("Antiflood tidak aktif di grup ini.")

def check_flood(update: Update, context: CallbackContext):
    """Memeriksa apakah pengguna sedang melakukan flood."""
    chat_id = str(update.effective_chat.id)
    
    if chat_id not in antiflood_config:
        return  # Jika antiflood tidak diatur di grup ini, abaikan

    user_id = update.effective_user.id
    now = time.time()
    config = antiflood_config[chat_id]

    if user_id not in config['user_messages']:
        config['user_messages'][user_id] = []

    # Tambahkan waktu pesan ke dalam daftar
    config['user_messages'][user_id].append(now)

    # Hapus pesan yang lebih lama dari window waktu yang ditentukan
    config['user_messages'][user_id] = [t for t in config['user_messages'][user_id] if now - t <= config['time_window']]

    if len(config['user_messages'][user_id]) > config['limit']:
        try:
            context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
            context.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, permissions=None, until_date=int(time.time() + 300))
            context.bot.send_message(chat_id=chat_id, text=f"Pengguna {update.effective_user.first_name} telah melakukan flood dan dibisukan selama 5 menit.")
        except Exception as e:
            print(f"Error saat menangani flood: {e}")

def setup(application):
    """Mendaftarkan handler untuk antiflood."""
    application.add_handler(CommandHandler("setflood", set_antiflood, filters.ChatType.GROUPS))
    application.add_handler(CommandHandler("disableflood", disable_antiflood, filters.ChatType.GROUPS))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, check_flood))
