from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
import json
import os
from datetime import datetime, timedelta
from modules.helpers import owner_only

SUBSCRIPTION_FILE = 'data/subscriptions.json'

def load_subscriptions():
    """Memuat daftar langganan dari file."""
    if os.path.exists(SUBSCRIPTION_FILE):
        with open(SUBSCRIPTION_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_subscriptions(subscriptions):
    """Menyimpan daftar langganan ke file."""
    with open(SUBSCRIPTION_FILE, 'w') as f:
        json.dump(subscriptions, f, indent=4)

subscriptions = load_subscriptions()

@owner_only
def add_subscription(update: Update, context: CallbackContext):
    """Menambahkan langganan grup."""
    if len(context.args) != 2:
        update.message.reply_text("Penggunaan: /addgc <chat_id> <durasi_dalam_hari>")
        return

    chat_id = context.args[0]
    try:
        duration = int(context.args[1])
    except ValueError:
        update.message.reply_text("Durasi harus berupa angka (jumlah hari).")
        return

    end_date = (datetime.now() + timedelta(days=duration)).strftime('%Y-%m-%d')
    subscriptions[chat_id] = end_date
    save_subscriptions(subscriptions)
    update.message.reply_text(f"Langganan untuk chat ID {chat_id} berhasil ditambahkan sampai {end_date}.")

@owner_only
def remove_subscription(update: Update, context: CallbackContext):
    """Menghapus langganan grup."""
    if len(context.args) != 1:
        update.message.reply_text("Penggunaan: /rmgc <chat_id>")
        return

    chat_id = context.args[0]
    if chat_id in subscriptions:
        del subscriptions[chat_id]
        save_subscriptions(subscriptions)
        update.message.reply_text(f"Langganan untuk chat ID {chat_id} berhasil dihapus.")
    else:
        update.message.reply_text(f"Tidak ada langganan aktif untuk chat ID {chat_id}.")

@owner_only
def list_subscriptions(update: Update, context: CallbackContext):
    """Menampilkan daftar langganan aktif."""
    if not subscriptions:
        update.message.reply_text("Tidak ada langganan aktif saat ini.")
        return

    message = "Daftar langganan aktif:\n\n"
    for chat_id, end_date in subscriptions.items():
        message += f"Chat ID: {chat_id}, Berakhir pada: {end_date}\n"
    update.message.reply_text(message)

def check_subscription(update: Update, context: CallbackContext):
    """Memeriksa status langganan untuk grup tertentu."""
    chat_id = str(update.effective_chat.id)
    if chat_id in subscriptions:
        end_date = subscriptions[chat_id]
        update.message.reply_text(f"Langganan aktif sampai {end_date}.")
    else:
        update.message.reply_text("Tidak ada langganan aktif untuk grup ini.")

def is_subscription_active(chat_id):
    """Memeriksa apakah langganan masih aktif."""
    chat_id = str(chat_id)
    if chat_id in subscriptions:
        end_date = datetime.strptime(subscriptions[chat_id], '%Y-%m-%d')
        return datetime.now() <= end_date
    return False

def setup(dp):
    """Mendaftarkan handler untuk perintah subscription."""
    dp.add_handler(CommandHandler("addgc", add_subscription))
    dp.add_handler(CommandHandler("rmgc", remove_subscription))
    dp.add_handler(CommandHandler("listgc", list_subscriptions))
    dp.add_handler(CommandHandler("cek", check_subscription))
