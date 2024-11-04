import sqlite3
from datetime import datetime, timedelta
import pytz
from config import DATABASE_FILE, TIMEZONE

class SubscriptionManager:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                chat_id INTEGER PRIMARY KEY,
                buyer_username TEXT,
                expiry_date TEXT
            )
        ''')
        self.conn.commit()

    def add_subscription(self, chat_id, buyer_username, duration_days):
        expiry_date = datetime.now(pytz.timezone(TIMEZONE)) + timedelta(days=duration_days)
        self.cursor.execute('''
            INSERT OR REPLACE INTO subscriptions (chat_id, buyer_username, expiry_date)
            VALUES (?, ?, ?)
        ''', (chat_id, buyer_username, expiry_date.strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    def remove_subscription(self, chat_id):
        self.cursor.execute('DELETE FROM subscriptions WHERE chat_id = ?', (chat_id,))
        self.conn.commit()

    def get_subscription(self, chat_id):
        self.cursor.execute('SELECT * FROM subscriptions WHERE chat_id = ?', (chat_id,))
        result = self.cursor.fetchone()
        return result

    def is_subscription_active(self, chat_id):
        subscription = self.get_subscription(chat_id)
        if subscription:
            expiry_date = datetime.strptime(subscription[2], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone(TIMEZONE))
            return datetime.now(pytz.timezone(TIMEZONE)) < expiry_date
        return False

    def get_all_subscriptions(self):
        self.cursor.execute('SELECT * FROM subscriptions')
        results = self.cursor.fetchall()
        return results

    def __del__(self):
        self.conn.close()
