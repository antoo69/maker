
# modules/__init__.py

# modules/__init__.py

from . import filterUser, blacklistWord, mute, antiflood, tagall, subscription

def setup_all_handlers(dp):
    """
    Fungsi ini digunakan untuk menginisialisasi semua handler dari modul-modul yang ada.
    """
    for module in [filterUser, blacklistWord, mute, antiflood, tagall, subscription]:
        module.setup(dp)
