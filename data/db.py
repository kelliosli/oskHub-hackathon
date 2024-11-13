import sqlite3
from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        language TEXT DEFAULT 'en'
                    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS contacts (
                        user_id INTEGER,
                        contact_id INTEGER,
                        name TEXT
                    )""")
    conn.commit()
    conn.close()


def add_contact(user_id, contact_id, name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (user_id, contact_id, name) VALUES (?, ?, ?)",
        (user_id, contact_id, name),
    )
    conn.commit()
    conn.close()


def get_contacts(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT contact_id, name FROM contacts WHERE user_id = ?", (user_id,)
    )
    contacts = cursor.fetchall()  # Get all contacts for the user
    conn.close()
    return contacts
