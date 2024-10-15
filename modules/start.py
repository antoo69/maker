# modules/start.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from database import is_subscription_active
import config

# Definisikan callback data untuk tombol
OWNER_CALLBACK = 'owner'
MODULES_CALLBACK = 'modules'
CHANNEL_CALLBACK = 'channel'
ABOUT_CALLBACK = 'about'
HARGA_CALLBACK = 'harga'  # Callback data untuk "Harga"

# Definisikan callback data untuk sub-menu daftar modul
FILTER_USER_CALLBACK = 'filter_user'
BLACKLIST_WORD_CALLBACK = 'blacklist_word'
MUTE_CALLBACK = 'mute'
TAG_ALL_CALLBACK = 'tag_all'
START_MODULE_CALLBACK = 'start_module'

def start_command(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Periksa apakah obrolan adalah pribadi
    if update.effective_chat.type == 'private':
        welcome_text = f"Hello {user.first_name}! Saya adalah bot Anti-Gcast."

        # Buat inline keyboard dengan tambahan tombol "Harga"
        keyboard = [
            [
                InlineKeyboardButton("👤 Owner", callback_data=OWNER_CALLBACK),
                InlineKeyboardButton("📦 Daftar Modul", callback_data=MODULES_CALLBACK)
            ],
            [
                InlineKeyboardButton("📢 Channel", callback_data=CHANNEL_CALLBACK),
                InlineKeyboardButton("ℹ️ Tentang Saya", callback_data=ABOUT_CALLBACK)
            ],
            [
                InlineKeyboardButton("💰 Harga", callback_data=HARGA_CALLBACK)  # Tambahkan tombol "Harga"
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # Tambahkan status subscription
        if is_subscription_active(chat_id):
            welcome_text += "\n\n🔔 **Subscription Aktif**"
        else:
            welcome_text += "\n\n⚠️ **Subscription Tidak Aktif**"

        # Kirim pesan dengan inline keyboard
        update.message.reply_text(welcome_text, reply_markup=reply_markup)
    else:
        # Jika digunakan di grup, tampilkan informasi tentang bot
        group_info_text = (
            "ℹ️ **Tentang Bot**\n\n"
            "Saya adalah bot Anti-Gcast yang membantu mengelola dan melindungi grup Anda dari spam dan penyalahgunaan.\n"
            "Gunakan perintah `/start` di obrolan pribadi untuk melihat lebih banyak opsi."
        )
        update.message.reply_text(group_info_text)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()  # Mengakui callback query

    data = query.data

    if data == OWNER_CALLBACK:
        owner_text = "👤 **Owner Bot**\n\nNama: John Doe\nTelegram: [@johndoe](https://t.me/johndoe)"
        query.edit_message_text(text=owner_text, parse_mode='Markdown', disable_web_page_preview=True)

    elif data == MODULES_CALLBACK:
        # Buat sub-menu untuk daftar modul
        keyboard = [
            [InlineKeyboardButton("🔍 Filter User", callback_data=FILTER_USER_CALLBACK)],
            [InlineKeyboardButton("🚫 Blacklist Word", callback_data=BLACKLIST_WORD_CALLBACK)],
            [InlineKeyboardButton("🔇 Mute", callback_data=MUTE_CALLBACK)],
            [InlineKeyboardButton("🏷️ Tag All", callback_data=TAG_ALL_CALLBACK)],
            [InlineKeyboardButton("🔄 Start Module", callback_data=START_MODULE_CALLBACK)],
            [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="📦 **Daftar Modul**:\nPilih modul untuk melihat cara penggunaan.", reply_markup=reply_markup)

    elif data == CHANNEL_CALLBACK:
        channel_text = "📢 **Channel Bot**\n\nBergabunglah dengan channel resmi kami untuk update terbaru:\n[Join Channel](https://t.me/your_channel_link)"
        query.edit_message_text(text=channel_text, parse_mode='Markdown', disable_web_page_preview=True)

    elif data == ABOUT_CALLBACK:
        about_text = "ℹ️ **Tentang Saya**\n\nSaya adalah bot Anti-Gcast yang membantu mengelola dan melindungi grup Anda dari spam dan penyalahgunaan."
        query.edit_message_text(text=about_text, parse_mode='Markdown')

    elif data == HARGA_CALLBACK:
        harga_text = (
            "💰 **Harga Layanan Bot Anti-Gcast**\n\n"
            "Kami menawarkan beberapa paket layanan untuk memenuhi kebutuhan grup Anda:\n\n"
            "1. **Paket Basic** - Gratis\n"
            "   - Fitur dasar anti-gcast\n"
            "   - Pemantauan pesan secara real-time\n\n"
            "2. **Paket Premium** - Rp50.000/bulan\n"
            "   - Semua fitur Basic\n"
            "   - Fitur mute dan ban otomatis\n"
            "   - Laporan aktivitas mingguan\n\n"
            "3. **Paket Enterprise** - Rp150.000/bulan\n"
            "   - Semua fitur Premium\n"
            "   - Dukungan prioritas\n"
            "   - Kustomisasi fitur sesuai kebutuhan grup\n\n"
            "Untuk informasi lebih lanjut atau membeli paket, silakan hubungi [Owner](https://t.me/johndoe)."
        )
        query.edit_message_text(text=harga_text, parse_mode='Markdown', disable_web_page_preview=True)

    elif data == FILTER_USER_CALLBACK:
        filter_user_text = "🔍 **Filter User**\n\nFitur ini memantau dan menghapus pesan dari pengguna yang telah difilter.\n\nCara Penggunaan:\n- Tambahkan pengguna ke dalam filter menggunakan perintah `/addfilter <user_id>`.\n- Hapus pengguna dari filter menggunakan perintah `/removefilter <user_id>`."
        query.edit_message_text(text=filter_user_text, parse_mode='Markdown')

    elif data == BLACKLIST_WORD_CALLBACK:
        blacklist_word_text = "🚫 **Blacklist Word**\n\nFitur ini memfilter dan menghapus pesan yang mengandung kata-kata yang dilarang.\n\nCara Penggunaan:\n- Tambahkan kata yang ingin diblokir di `blacklist_words.json`."
        query.edit_message_text(text=blacklist_word_text, parse_mode='Markdown')

    elif data == MUTE_CALLBACK:
        mute_text = "🔇 **Mute**\n\nFitur ini memungkinkan admin untuk mematikan suara pengguna tertentu selama periode tertentu.\n\nCara Penggunaan:\n- Gunakan perintah `/mute` dengan membalas pesan pengguna.\n- Gunakan perintah `/unmute` untuk membatalkan mute."
        query.edit_message_text(text=mute_text, parse_mode='Markdown')

    elif data == TAG_ALL_CALLBACK:
        tag_all_text = "🏷️ **Tag All**\n\nFitur ini memungkinkan admin untuk menandai semua anggota grup sekaligus. **Catatan:** Telegram memiliki batasan jumlah mention dalam satu pesan.\n\nCara Penggunaan:\n- Gunakan perintah `/tagall` untuk menandai semua anggota."
        query.edit_message_text(text=tag_all_text, parse_mode='Markdown')

    elif data == START_MODULE_CALLBACK:
        start_module_text = "🔄 **Start Module**\n\nFitur ini menangani perintah /start dan memberikan informasi dasar tentang bot.\n\nCara Penggunaan:\n- Gunakan perintah `/start` untuk memulai interaksi dengan bot."
        query.edit_message_text(text=start_module_text, parse_mode='Markdown')

    elif data == 'back_to_main':
        # Kembali ke menu utama
        keyboard = [
            [InlineKeyboardButton("👤 Owner", callback_data=OWNER_CALLBACK)],
            [InlineKeyboardButton("📦 Daftar Modul", callback_data=MODULES_CALLBACK)],
            [InlineKeyboardButton("📢 Channel", callback_data=CHANNEL_CALLBACK)],
            [InlineKeyboardButton("ℹ️ Tentang Saya", callback_data=ABOUT_CALLBACK)],
            [InlineKeyboardButton("💰 Harga", callback_data=HARGA_CALLBACK)]  # Tambahkan kembali tombol "Harga"
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        main_menu_text = "📦 **Daftar Modul**:\nPilih modul untuk melihat cara penggunaan."
        query.edit_message_text(text=main_menu_text, reply_markup=reply_markup)

    else:
        query.edit_message_text(text="❓ **Tidak Dikenal**\nPerintah tidak dikenali.")

def setup(dp):
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CallbackQueryHandler(button_handler))
