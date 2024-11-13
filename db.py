import sqlite3


def get_db_connection():
    return sqlite3.connect("friends.db")


def init_db():
    conn = sqlite3.connect("friends.db")
    cursor = conn.cursor()

    cursor.executescript("""
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
    """)
    conn.commit()
    conn.close()


def get_friends_user_ids(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Step 1: Fetch friends' usernames
    cursor.execute("SELECT username FROM friends WHERE user_id = ?", (user_id,))
    friends = cursor.fetchall()

    # Step 2: Find corresponding user_id for each friend (by joining the users table)
    friends_user_ids = []
    for friend in friends:
        username = friend[0]
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user:
            friends_user_ids.append(user[0])

    conn.close()
    return friends_user_ids
