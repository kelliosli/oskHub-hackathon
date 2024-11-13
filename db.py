import sqlite3

def get_db_connection():
    return sqlite3.connect("friends.db")

def init_db():
    conn = sqlite3.connect("friends.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            user_id INTEGER,
            friend_id INTEGER PRIMARY KEY,
            username TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            user_id INTEGER,
            language TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
