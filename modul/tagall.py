# modules/tagall.py
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler
from database import is_subscription_active

def tag_all(update: Update, context: CallbackContext):
    chat = update.effective_chat
    if chat.type not in ['group', 'supergroup']:
        update.message.reply_text("Perintah ini hanya dapat digunakan di grup.")
        return

    chat_id = chat.id
    if not is_subscription_active(chat_id):
        update.message.reply_text("Subscription tidak aktif. Hubungi owner untuk mengaktifkan bot.")
        return

    members_count = context.bot.get_chat_members_count(chat_id)
    if members_count > 200:
        update.message.reply_text("Jumlah anggota terlalu banyak untuk ditandai dalam satu pesan.")
        return

    # Mendapatkan semua anggota grup
    members = context.bot.get_chat(chat_id).get_members()

    # Membuat daftar mention
    mentions = []
    for member in members:
        user = member.user
        if user.username:
            mentions.append(f"@{user.username}")
        else:
            mentions.append(f"{user.first_name}")

    # Menggabungkan mention dengan spasi
    message = " ".join(mentions)

    update.message.reply_text(f"📣 {message}", parse_mode=ParseMode.MARKDOWN)

def setup(dp):
    dp.add_handler(CommandHandler("tagall", tag_all, Filters.user.is_admin))
