import os
from dotenv import load_dotenv

# Memuat variabel lingkungan dari file .env
load_dotenv(".env")

# Mengambil nilai TOKEN dari variabel lingkungan
TOKEN = os.getenv('TOKEN')

# Mengambil nilai OWNER_ID dari variabel lingkungan dan mengonversinya ke integer
OWNER_ID = int(os.getenv('OWNER_ID'))

# Menambahkan variabel konfigurasi baru
DATABASE_FILE = 'data/subscriptions.db'
BLACKLIST_USERS_FILE = 'data/blacklist_users.json'
BLACKLIST_WORDS_FILE = 'data/blacklist_words.json'
MUTED_USERS_FILE = 'data/muted_users.json'


# Menambahkan konfigurasi untuk zona waktu
TIMEZONE = 'Asia/Jakarta'

# Menambahkan konfigurasi untuk durasi subscription default (dalam hari)
DEFAULT_SUBSCRIPTION_DURATION = 30
