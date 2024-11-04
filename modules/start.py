from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
import config

# Fungsi untuk menangani perintah /start dan menampilkan menu utama
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("👤 Owner", callback_data='owner'),
         InlineKeyboardButton("📢 Channel", callback_data='channel')],
        [InlineKeyboardButton("⚙️ Manage", callback_data='manage'),
         InlineKeyboardButton("💳 Langganan", callback_data='subscription')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Tampilkan gambar dengan tombol-tombol
    photo_url = 'https://example.com/your_image.jpg'  # URL gambar yang ingin ditampilkan
    update.message.reply_photo(photo=photo_url, caption="Selamat datang di Bot. Pilih opsi dari menu berikut:", reply_markup=reply_markup)

# Fungsi untuk menangani submenu Manage
def show_manage_menu(query):
    manage_keyboard = [
        [InlineKeyboardButton("🏷️ Tag All", callback_data='tagall_info'),
         InlineKeyboardButton("🚫 Filter User", callback_data='filteruser_info')],
        [InlineKeyboardButton("📝 Blacklist Word", callback_data='blacklistword_info'),
         InlineKeyboardButton("🔇 Mute User", callback_data='mute_info')],
        [InlineKeyboardButton("🚨 Anti Flood", callback_data='antiflood_info')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(manage_keyboard)
    query.edit_message_text(text="Pilih modul yang ingin dijelaskan:", reply_markup=reply_markup)

# Fungsi untuk menangani submenu Langganan
def show_subscription_menu(query):
    subscription_keyboard = [
        [InlineKeyboardButton("🔐 Cara Aktivasi", callback_data='activation'),
         InlineKeyboardButton("💲 Daftar Harga", callback_data='pricing')],
        [InlineKeyboardButton("📝 Cek Status Langganan", callback_data='status')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(subscription_keyboard)
    query.edit_message_text(text="Pilih opsi terkait langganan:", reply_markup=reply_markup)

# Fungsi untuk menangani callback ketika tombol ditekan
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'owner':
        query.edit_message_text(text="Pemilik bot adalah @OwnerUsername", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data='back')]]))
    elif query.data == 'channel':
        query.edit_message_text(text="Ikuti channel kami di: https://t.me/channelname", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data='back')]]))
    elif query.data == 'manage':
        show_manage_menu(query)
    elif query.data == 'subscription':
        show_subscription_menu(query)
    elif query.data == 'back':
        start(update, context)

# Setup function to handle start and button callbacks
def setup(dp):
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))

# Call the setup function
setup(dp)
