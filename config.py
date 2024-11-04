# config.py

# Token bot Telegram
TOKEN = 'YOUR_BOT_TOKEN_HERE'

# ID pemilik bot
OWNER_ID = 123456789  # Replace with your Telegram ID

# ID pengembang
DEV_ID = 987654321  # Replace with the Telegram ID of the developer

# Pengaturan database (opsional)
DATABASE_URL = 'sqlite:///bot_database.db'

# Daftar admin (opsional)
ADMIN_IDS = [
    123456789,
    987654321,
]

# Pengaturan lainnya
DEBUG_MODE = False
MAX_MESSAGES_PER_MINUTE = 60

# Additional settings
LOGGING_LEVEL = 'INFO'
LOG_FILE = 'bot.log'

# Telegram API endpoint
API_ENDPOINT = 'https://api.telegram.org'

# Bot's language
LANGUAGE = 'en'

# Bot's timezone
TIMEZONE = 'UTC'
