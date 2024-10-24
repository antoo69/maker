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
    elif query.data == 'activation':
        show_activation_info(query)
    elif query.data == 'pricing':
        show_pricing_info(query)
    elif query.data == 'status':
        show_status_info(query)
    elif query.data == 'tagall_info':
        show_tagall_info(query)
    elif query.data == 'filteruser_info':
        show_filteruser_info(query)
    elif query.data == 'blacklistword_info':
        show_blacklistword_info(query)
    elif query.data == 'mute_info':
        show_mute_info(query)
    elif query.data == 'antiflood_info':
        show_antiflood_info(query)
    elif query.data == 'back':
        start(update, context)

# Setup function to handle start and button callbacks
def setup(dp):
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))

# Fungsi untuk menampilkan informasi modul
def show_activation_info(query):
    query.edit_message_text(
        text="🔐 Aktivasi Langganan\n\n"
             "Perintah:\n/addgc <chat_id> <durasi_hari>\n\nPenjelasan: Owner menambahkan grup ke dalam sistem langganan selama durasi tertentu.\n\n"
             "Perintah:\n/removegc <chat_id>\n\nPenjelasan: Owner menghapus grup dari sistem langganan.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data='subscription')]])
    )

def show_pricing_info(query):
    query.edit_message_text(
        text="💲 Daftar Harga Langganan\n\n"
             "1. 30 Hari: Rp50.000\n"
             "2. 60 Hari: Rp90.000\n"
             "3. 90 Hari: Rp120.000\n\n"
             "Untuk mengaktifkan langganan, hubungi pemilik bot.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data='subscription')]])
    )

def show_status_info(query):
    query.edit_message_text(
        text="📝 Cek Status Langganan\n\n"
             "Perintah:\n/listgc\n\nPenjelasan: Melihat daftar grup yang aktif berlangganan beserta durasinya.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data='subscription')]])
    )

def show_tagall_info(query):
    query.edit_message_text(
        text="🏷️ Tag All\n\n"
             "Perintah:\n/tagall\n\nPenjelasan: Untuk menandai semua anggota grup.\n\n"
             "Perintah:\n/cancel\n\nPenjelasan: Untuk membatalkan proses tagall.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data='manage')]])
    )

def show_filteruser_info(query):
    query.edit_message_text(
        text="🚫 Filter User\n\n"
             "Perintah:\n/addblacklist <user_id/username>\n\nPenjelasan: Menambahkan pengguna ke daftar blacklist.\n\n"
             "Perintah:\n/removeblacklist <user_id/username>\n\nPenjelasan: Menghapus pengguna dari daftar blacklist.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data='manage')]])
    )

def show_blacklistword_info(query):
    query.edit_message_text(
        text="📝 Blacklist Word\n\n"
             "Perintah:\n/addword <kata>\n\nPenjelasan: Menambahkan kata ke daftar blacklist.\n\n"
             "Perintah:\n/removeword <kata>\n\nPenjelasan: Menghapus kata dari daftar blacklist.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data='manage')]])
    )

def show_mute_info(query):
    query.edit_message_text(
        text="🔇 Mute User\n\n"
             "Perintah:\n/mute <user_id/username>\n\nPenjelasan: Membisukan pengguna tertentu di grup.\n\n"
             "Perintah:\n/unmute <user_id/username>\n\nPenjelasan: Mengembalikan hak bicara pengguna.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data='manage')]])
    )

def show_antiflood_info(query):
    query.edit_message_text(
        text="🚨 Anti Flood\n\n"
             "Perintah:\n/setflood <jumlah_pesan>\n\nPenjelasan: Mengatur batas maksimal jumlah pesan yang diizinkan dalam waktu singkat.\n\n"
             "Perintah:\n/unsetflood\n\nPenjelasan: Menonaktifkan pengaturan anti-flood.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data='manage')]])
    )
