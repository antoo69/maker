from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, Filters
import asyncio

# Variable to store the status of the tagall command
tagall_active = False

async def delete_pesan_nanti(context: CallbackContext, message_id: int, chat_id: int, delay: int):
    await asyncio.sleep(delay)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass

async def tag_semua(update: Update, context: CallbackContext):
    global tagall_active
    tagall_active = True

    chat = update.effective_chat
    chat_id = chat.id

    if chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("Perintah ini hanya bisa digunakan di grup.")
        await delete_pesan_nanti(context, update.message.message_id, chat_id, 5)
        return

    if not await adalah_admin(update, context):
        await update.message.reply_text("Hanya admin yang bisa menggunakan perintah ini.")
        await delete_pesan_nanti(context, update.message.message_id, chat_id, 5)
        return

    try:
        members = await context.bot.get_chat_members(chat_id)
    except Exception as e:
        await update.message.reply_text(f"Gagal mengambil daftar anggota: {str(e)}")
        return

    batch_size = 5
    mentions = []

    await update.message.reply_text(f"Memulai tag semua di grup: {chat.title} (Total anggota: {len(members)})")

    for member in members:
        if not tagall_active:
            await update.message.reply_text("Tag semua dibatalkan.")
            return

        user = member.user
        if user.username:
            mentions.append(f"@{user.username}")
        else:
            mentions.append(f"[{user.first_name}](tg://user?id={user.id})")

        if len(mentions) == batch_size:
            message = " ".join(mentions)
            try:
                await update.message.reply_text(f"📢 {message}", parse_mode=ParseMode.MARKDOWN)
            except Exception:
                await update.message.reply_text("Gagal mengirim pesan mention.")
            mentions = []
            await asyncio.sleep(1)  # Jeda untuk menghindari flood

    if mentions:
        message = " ".join(mentions)
        try:
            await update.message.reply_text(f"📢 {message}", parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await update.message.reply_text("Gagal mengirim pesan mention terakhir.")

    await update.message.reply_text("Tag semua selesai.")

async def batal_tag_semua(update: Update, context: CallbackContext):
    global tagall_active
    tagall_active = False
    await update.message.reply_text("Tag semua dibatalkan.")
    await delete_pesan_nanti(context, update.message.message_id, update.effective_chat.id, 5)

async def adalah_admin(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id
        chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return chat_member.status in ['administrator', 'creator']
    except Exception:
        return False

def setup(dp):
    dp.add_handler(CommandHandler("tagsemua", tag_semua, Filters.chat_type.groups))
    dp.add_handler(CommandHandler("bataltag", batal_tag_semua, Filters.chat_type.groups))
