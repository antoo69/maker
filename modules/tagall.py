from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, Filters
import asyncio

# Variabel untuk menyimpan status tagall aktif
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

    obrolan = update.effective_chat
    id_obrolan = obrolan.id

    if obrolan.type not in ['group', 'supergroup']:
        pesan = await update.message.reply_text("Perintah ini hanya bisa digunakan di grup.")
        await delete_pesan_nanti(context, pesan.message_id, id_obrolan, 5)
        return

    if not await adalah_admin(update, context):
        pesan = await update.message.reply_text("Hanya admin yang bisa menggunakan perintah ini.")
        await delete_pesan_nanti(context, pesan.message_id, id_obrolan, 5)
        return

    try:
        anggota = await context.bot.get_chat_members(id_obrolan)
    except Exception as e:
        await update.message.reply_text(f"Gagal mengambil daftar anggota: {str(e)}")
        return

    ukuran_batch = 5
    mention = []
    
    await update.message.reply_text(f"Memulai tag semua di grup: {obrolan.title} (Total anggota: {len(anggota)})")

    for member in anggota:
        if not tagall_active:
            await update.message.reply_text("Tag semua dibatalkan.")
            return

        pengguna = member.user
        if pengguna.username:
            mention.append(f"@{pengguna.username}")
        else:
            mention.append(f"[{pengguna.first_name}](tg://user?id={pengguna.id})")

        if len(mention) == ukuran_batch:
            pesan = " ".join(mention)
            try:
                await update.message.reply_text(f"📢 {pesan}", parse_mode=ParseMode.MARKDOWN)
            except Exception:
                await update.message.reply_text("Gagal mengirim pesan mention.")
            mention = []
            await asyncio.sleep(1)  # Jeda untuk menghindari flood

    if mention:
        pesan = " ".join(mention)
        try:
            await update.message.reply_text(f"📢 {pesan}", parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await update.message.reply_text("Gagal mengirim pesan mention terakhir.")

    await update.message.reply_text("Tag semua selesai.")

async def batal_tag_semua(update: Update, context: CallbackContext):
    global tagall_active
    tagall_active = False
    pesan = await update.message.reply_text("Tag semua dibatalkan.")
    await delete_pesan_nanti(context, pesan.message_id, update.effective_chat.id, 5)

async def adalah_admin(update: Update, context: CallbackContext):
    try:
        id_pengguna = update.effective_user.id
        anggota_obrolan = await context.bot.get_chat_member(update.effective_chat.id, id_pengguna)
        return anggota_obrolan.status in ['administrator', 'creator']
    except Exception:
        return False

def setup(dp):
    dp.add_handler(CommandHandler("tagsemua", tag_semua, Filters.chat_type.groups))
    dp.add_handler(CommandHandler("bataltag", batal_tag_semua, Filters.chat_type.groups))
