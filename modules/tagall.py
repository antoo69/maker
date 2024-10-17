from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, Filters
from database import is_subscription_active
import asyncio

async def delete_message_later(context: CallbackContext, message_id: int, chat_id: int, delay: int):
    await asyncio.sleep(delay)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass

async def is_admin(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id
        chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return chat_member.status in ['administrator', 'creator']
    except Exception:
        return False

async def tag_all(update: Update, context: CallbackContext):
    chat = update.effective_chat
    chat_id = chat.id

    if chat.type not in ['group', 'supergroup']:
        msg = await update.message.reply_text("Perintah ini hanya dapat digunakan di grup.")
        await delete_message_later(context, msg.message_id, chat_id, 5)
        return

    if not await is_admin(update, context):
        msg = await update.message.reply_text("Perintah ini hanya dapat digunakan oleh admin.")
        await delete_message_later(context, msg.message_id, chat_id, 5)
        return

    if not is_subscription_active(chat_id):
        msg = await update.message.reply_text("Subscription tidak aktif. Hubungi owner untuk mengaktifkan bot.")
        await delete_message_later(context, msg.message_id, chat_id, 5)
        return

    try:
        members = await context.bot.get_chat_members(chat_id)
    except Exception as e:
        await update.message.reply_text(f"Gagal mendapatkan daftar anggota: {str(e)}")
        return

    batch_size = 5
    mentions = []
    
    await update.message.reply_text(f"Memulai tagall di grup: {chat.title} (Total anggota: {len(members)})")

    for member in members:
        if context.user_data.get('tagall_active') is False:
            await update.message.reply_text("Tagall dibatalkan.")
            return

        user = member.user
        if user.username:
            mentions.append(f"@{user.username}")
        else:
            mentions.append(f"[{user.first_name}](tg://user?id={user.id})")

        if len(mentions) == batch_size:
            message = " ".join(mentions)
            try:
                await update.message.reply_text(f"📣 {message}", parse_mode=ParseMode.MARKDOWN)
            except Exception:
                await update.message.reply_text("Gagal mengirim pesan mention.")
            mentions = []
            await asyncio.sleep(1)  # Delay untuk menghindari flood

    if mentions:
        message = " ".join(mentions)
        try:
            await update.message.reply_text(f"📣 {message}", parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await update.message.reply_text("Gagal mengirim pesan mention terakhir.")

    await update.message.reply_text("Tagall selesai.")

async def cancel_tagall(update: Update, context: CallbackContext):
    context.user_data['tagall_active'] = False
    msg = await update.message.reply_text("Tagall dibatalkan.")
    await delete_message_later(context, msg.message_id, update.effective_chat.id, 5)

def setup(dp):
    dp.add_handler(CommandHandler("tagall", tag_all, Filters.chat_type.groups))
    dp.add_handler(CommandHandler("cancel", cancel_tagall, Filters.chat_type.groups))
