import sqlite3
import random

def seed_database():
    conn = sqlite3.connect("shopping.db")
    cursor = conn.cursor()
    
    # Table မရှိသေးရင် အလိုအလျောက် တည်ဆောက်ပေးရန်
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    
    # Database ထဲမှာ Data ရှိ/မရှိ စစ်ဆေးရန်
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("Adding 100 products to database...")
        base_names = ["Mechanical Keyboard", "Wireless Mouse", "4K Ultra HD Monitor", "Gaming Headset", "HD Webcam", "USB-C Hub", "Laptop Stand", "Ergonomic Desk Mat"]
        
        # Product အခု ၁၀၀ ကို Database ထဲသို့ ထည့်ရန်
        for i in range(1, 101):
            name = f"{random.choice(base_names)} Gen-{random.randint(1, 9)}"
            price = round(random.uniform(25.0, 499.0), 2)
            stock = random.randint(5, 50)
            
            cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
            
        conn.commit()
        print("✅ Successfully added 100 products! Refresh your browser.")
    else:
        print(f"Database already has {count} products.")
        
    conn.close()

if __name__ == "__main__":
    seed_database()