from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, Filters
from database import is_subscription_active
import threading

# Fungsi untuk menghapus pesan setelah beberapa detik
def delete_message_later(context: CallbackContext, message_id: int, chat_id: int, delay: int):
    threading.Timer(delay, lambda: context.bot.delete_message(chat_id=chat_id, message_id=message_id)).start()

# Fungsi untuk memeriksa apakah user adalah admin
def is_admin(update: Update):
    user_id = update.effective_user.id
    member = update.effective_chat.get_member(user_id)
    return member.status in ['administrator', 'creator']

def tag_all(update: Update, context: CallbackContext):
    chat = update.effective_chat
    chat_id = chat.id

    # Periksa apakah perintah dijalankan di grup atau supergrup
    if chat.type not in ['group', 'supergroup']:
        msg = update.message.reply_text("Perintah ini hanya dapat digunakan di grup.")
        delete_message_later(context, msg.message_id, chat_id, 5)
        return

    # Memastikan hanya admin yang bisa menggunakan perintah ini
    if not is_admin(update):
        msg = update.message.reply_text("Perintah ini hanya dapat digunakan oleh admin.")
        delete_message_later(context, msg.message_id, chat_id, 5)
        return

    # Periksa status subscription
    if not is_subscription_active(chat_id):
        msg = update.message.reply_text("Subscription tidak aktif. Hubungi owner untuk mengaktifkan bot.")
        delete_message_later(context, msg.message_id, chat_id, 5)
        return

    # Mendapatkan semua anggota grup
    members = context.bot.get_chat_administrators(chat_id) + context.bot.get_chat_members(chat_id)
    members = [member.user for member in members]  # Mendapatkan semua pengguna

    # Batasi batch untuk menghindari pesan yang terlalu panjang (max 4096 karakter per pesan)
    batch_size = 10
    mentions = []
    
    # Mulai proses tagall
    update.message.reply_text(f"Memulai tagall di grup: {chat.title} (Total anggota: {len(members)})")

    for member in members:
        if context.user_data.get('tagall_active') is False:
            update.message.reply_text("Tagall dibatalkan.")
            return

        if member.username:
            mentions.append(f"@{member.username}")
        else:
            mentions.append(f"[{member.first_name}](tg://user?id={member.id})")  # Mention menggunakan nama depan jika tidak ada username

        # Kirim dalam batch setelah jumlah mentions mencapai batas
        if len(mentions) == batch_size:
            message = " ".join(mentions)
            update.message.reply_text(f"📣 {message}", parse_mode=ParseMode.MARKDOWN)
            mentions = []

    # Kirim sisa mentions jika ada
    if mentions:
        message = " ".join(mentions)
        update.message.reply_text(f"📣 {message}", parse_mode=ParseMode.MARKDOWN)

    update.message.reply_text("Tagall selesai.")

def cancel_tagall(update: Update, context: CallbackContext):
    # Hentikan tagall
    context.user_data['tagall_active'] = False
    msg = update.message.reply_text("Tagall dibatalkan.")
    delete_message_later(context, msg.message_id, update.effective_chat.id, 5)

def setup(dp):
    dp.add_handler(CommandHandler("tagall", tag_all, Filters.chat_type.groups))
    dp.add_handler(CommandHandler("cancel", cancel_tagall, Filters.chat_type.groups))
