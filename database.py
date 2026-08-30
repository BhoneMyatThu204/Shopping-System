<<<<<<< HEAD
import sqlite3

def connect_db():
    conn = sqlite3.connect("shopping.db")
    cursor = conn.cursor()
    
    # Products Table (UPDATED: Added 'image' column)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            image TEXT NOT NULL
        )
    ''')
    
    # Orders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    conn.commit()
=======
import sqlite3

def connect_db():
    # Database locked မဖြစ်စေရန် timeout=15.0 ထည့်သွင်းထားပါသည်
    conn = sqlite3.connect("shopping.db", timeout=15.0)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            image TEXT NOT NULL,
            discount INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            product_id INTEGER,
            quantity INTEGER,
            size TEXT,
            total_price REAL,
            status TEXT DEFAULT 'Pending',
            order_note TEXT,
            rating INTEGER DEFAULT 0,
            review_comment TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            product_id INTEGER,
            quantity INTEGER DEFAULT 1,
            size TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')
    
    conn.commit()
>>>>>>> f3caf30c0cb0460d97c3b2172334b1a5f61cfb71
    return conn