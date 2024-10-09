import sqlite3
from datetime import datetime, timedelta

DATABASE_FILE = 'data/subscriptions.db'

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            chat_id INTEGER PRIMARY KEY,
            buyer_username TEXT,
            expiry_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_subscription(chat_id, buyer_username, duration_days):
    expiry_date = datetime.now() + timedelta(days=duration_days)
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO subscriptions (chat_id, buyer_username, expiry_date)
        VALUES (?, ?, ?)
    ''', (chat_id, buyer_username, expiry_date.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def remove_subscription(chat_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM subscriptions WHERE chat_id = ?', (chat_id,))
    conn.commit()
    conn.close()

def get_subscription(chat_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM subscriptions WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def is_subscription_active(chat_id):
    subscription = get_subscription(chat_id)
    if subscription:
        expiry_date = datetime.strptime(subscription[2], '%Y-%m-%d %H:%M:%S')
        return datetime.now() < expiry_date
    return False

def get_all_subscriptions():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM subscriptions')
    results = cursor.fetchall()
    conn.close()
    return results
