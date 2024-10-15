# modules/tagall.py
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, Filters
from database import is_subscription_active

# Definisikan state untuk percakapan
TAGGING, = range(1)

# Fungsi untuk memeriksa apakah user adalah admin
def is_admin(update: Update):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    member = update.effective_chat.get_member(user_id)
    return member.status in ['administrator', 'creator']

def tag_all(update: Update, context: CallbackContext):
    chat = update.effective_chat
    if chat.type not in ['group', 'supergroup']:
        update.message.reply_text("Perintah ini hanya dapat digunakan di grup.")
        return

    # Memastikan hanya admin yang bisa menggunakan perintah ini
    if not is_admin(update):
        update.message.reply_text("Perintah ini hanya dapat digunakan oleh admin.")
        return

    chat_id = chat.id
    if not is_subscription_active(chat_id):
        update.message.reply_text("Subscription tidak aktif. Hubungi owner untuk mengaktifkan bot.")
        return

    members_count = context.bot.get_chat_members_count(chat_id)
    
    # Mendapatkan anggota grup dalam batch untuk menghindari pesan yang terlalu panjang
    batch_size = 10  # Tentukan berapa banyak anggota per batch
    mentions = []
    
    # Simpan status tagall di konteks
    context.user_data['tagall_active'] = True

    for i in range(members_count):
        # Cek jika tagall dibatalkan
        if context.user_data.get('tagall_active') is False:
            update.message.reply_text("Tagall dibatalkan.")
            return

        member = context.bot.get_chat_member(chat_id, i)
        user = member.user
        if user.username:
            mentions.append(f"@{user.username}")
        else:
            mentions.append(user.first_name)  # Menggunakan nama depan jika tidak ada username

        # Jika jumlah mention sudah mencapai batch_size, kirim pesan
        if len(mentions) == batch_size:
            message = " ".join(mentions)
            update.message.reply_text(f"📣 {message}", parse_mode=ParseMode.MARKDOWN)
            mentions = []  # Reset daftar mentions

    # Kirim sisa mentions jika ada
    if mentions:
        message = " ".join(mentions)
        update.message.reply_text(f"📣 {message}", parse_mode=ParseMode.MARKDOWN)

def cancel_tagall(update: Update, context: CallbackContext):
    # Hentikan tagall
    context.user_data['tagall_active'] = False
    update.message.reply_text("Tagall dibatalkan.")

def setup(dp):
    dp.add_handler(CommandHandler("tagall", tag_all, Filters.chat_type.groups))
    dp.add_handler(CommandHandler("cancel", cancel_tagall, Filters.chat_type.groups))
