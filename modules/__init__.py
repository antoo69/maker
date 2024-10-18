
# modules/__init__.py

from .filterUser import setup as setup_filterUser
from .blacklistWord import setup as setup_blacklistWord
from .mute import setup as setup_mute
from .antiflood import setup as setup_antiflood
from .tagall import setup as setup_tagall
from .subscription import setup as setup_subscription

def setup_all_handlers(dp):
    """
    Fungsi ini digunakan untuk menginisialisasi semua handler dari modul-modul yang ada.
    """
    setup_filterUser(dp)
    setup_blacklistWord(dp)
    setup_mute(dp)
    setup_antiflood(dp)
    setup_tagall(dp)
    setup_subscription(dp)
