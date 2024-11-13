import sqlite3

def get_db_connection():
    return sqlite3.connect("friends.db")

def init_db():
    conn = sqlite3.connect("friends.db")
    cursor = conn.cursor()
    
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS friends (
            user_id INTEGER,
            friend_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT
        );
        
        CREATE TABLE IF NOT EXISTS languages (
            user_id INTEGER,
            language TEXT
        );
        
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER,
            username TEXT
        );
    ''')
    conn.commit()
    conn.close()
