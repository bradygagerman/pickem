import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    
    # Create User table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create League table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS league (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            league_name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            headuser INTEGER NOT NULL,
            FOREIGN KEY (headuser) REFERENCES user(id)
        )
    ''')
    
    # Create Pick table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pick (
            pick_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_win TEXT NOT NULL,
            spread REAL NOT NULL,
            team_loss TEXT NOT NULL
        )
    ''')

    # Create Basket table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS basket (
            basket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            p1 INTEGER,
            p2 INTEGER,
            p3 INTEGER,
            p4 INTEGER,
            p5 INTEGER,
            FOREIGN KEY (p1) REFERENCES pick(pick_id),
            FOREIGN KEY (p2) REFERENCES pick(pick_id),
            FOREIGN KEY (p3) REFERENCES pick(pick_id),
            FOREIGN KEY (p4) REFERENCES pick(pick_id),
            FOREIGN KEY (p5) REFERENCES pick(pick_id)
        )
    ''')

    # Create LeaguePlayer table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS leagueplayer (
            lp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user INTEGER NOT NULL,
            league INTEGER NOT NULL,
            basket INTEGER,
            FOREIGN KEY (user) REFERENCES user(id),
            FOREIGN KEY (league) REFERENCES league(id),
            FOREIGN KEY (basket) REFERENCES basket(basket_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(email, username, password):
    hashed_password = generate_password_hash(password, method='sha256')
    conn = get_db_connection()
    conn.execute('INSERT INTO user (email, username, password) VALUES (?, ?, ?)', 
                 (email, username, hashed_password))
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
