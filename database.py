import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_user_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_user(username, password):
    hashed_password = generate_password_hash(password, method='sha256')
    conn = get_db_connection()
    conn.execute('INSERT INTO user (username, password) VALUES (?, ?)', 
                 (username, hashed_password))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user WHERE username = ?', 
                        (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        return user
    return None
