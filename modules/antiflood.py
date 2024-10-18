from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
import time

# Variabel untuk menyimpan status antiflood aktif dan konfigurasi batas flood
antiflood_enabled = {}
flood_limit = 5  # Batas default pesan yang dianggap flood
flood_time_window = 10  # Waktu dalam detik untuk perhitungan flood
user_message_times = {}

def enable_antiflood(update: Update, context: CallbackContext):
    """Mengaktifkan antiflood untuk grup."""
    chat_id = str(update.effective_chat.id)
    antiflood_enabled[chat_id] = True
    update.message.reply_text("Antiflood diaktifkan di grup ini.")

def disable_antiflood(update: Update, context: CallbackContext):
    """Menonaktifkan antiflood untuk grup."""
    chat_id = str(update.effective_chat.id)
    if chat_id in antiflood_enabled:
        antiflood_enabled[chat_id] = False
        update.message.reply_text("Antiflood dinonaktifkan di grup ini.")
    else:
        update.message.reply_text("Antiflood tidak aktif di grup ini.")

def check_flood(update: Update, context: CallbackContext):
    """Memeriksa apakah pengguna sedang melakukan flood."""
    chat_id = str(update.effective_chat.id)
    
    if chat_id not in antiflood_enabled or not antiflood_enabled[chat_id]:
        return  # Jika antiflood tidak aktif di grup ini, abaikan

    user_id = update.effective_user.id
    now = time.time()

    if user_id not in user_message_times:
        user_message_times[user_id] = []

    # Tambahkan waktu pesan ke dalam daftar
    user_message_times[user_id].append(now)

    # Hapus pesan yang lebih lama dari window waktu yang ditentukan
    user_message_times[user_id] = [t for t in user_message_times[user_id] if now - t <= flood_time_window]

    if len(user_message_times[user_id]) > flood_limit:
        try:
            update.message.delete()
            update.message.reply_text(f"Pengguna {update.effective_user.first_name} telah melakukan flood.")
        except:
            pass  # Jika pesan tidak dapat dihapus, abaikan

def setup(dp):
    """Mendaftarkan handler untuk antiflood."""
    dp.add_handler(CommandHandler("enable_antiflood", enable_antiflood, Filters.chat_type.groups))
    dp.add_handler(CommandHandler("disable_antiflood", disable_antiflood, Filters.chat_type.groups))
    dp.add_handler(MessageHandler(Filters.text & Filters.chat_type.groups, check_flood))
