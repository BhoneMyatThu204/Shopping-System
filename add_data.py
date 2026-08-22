<<<<<<< HEAD
import sqlite3
import random
import database 

def reset_database():
    conn = database.connect_db()
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('DROP TABLE IF EXISTS users')
    
    conn = database.connect_db()
    cursor = conn.cursor()
    
    print("Adding default Admin account...")
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "admin123", "owner"))
    
    print("Adding clothing products with image links...")
    clothing_items = ["Graphic Tee", "Summer Shorts", "Leather Jacket", "Winter Beanie", "Polo Shirt", "Cargo Pants", "Running Shoes"]
    
    for i in range(1, 101):
        if i == 1: name = "Classic T-Shirt"
        elif i == 2: name = "Urban Sneakers"
        elif i == 3: name = "Denim Jeans"
        elif i == 4: name = "Cozy Hoodie"
        else: name = random.choice(clothing_items)
        
        price = round(random.uniform(15.0, 150.0), 2)
        stock = random.randint(5, 50)
        
        # Determine the correct image name for the default 100 items
        image_name = f"product_{i:03}.jpg"
        
        # Notice we added the image_name to the INSERT query!
        cursor.execute("INSERT INTO products (name, price, stock, image) VALUES (?, ?, ?, ?)", (name, price, stock, image_name))
        
    conn.commit()
    print("✅ Successfully updated! You can now log in as Owner with username: admin / password: admin123")
    conn.close()

if __name__ == "__main__":
    reset_database()
=======
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
>>>>>>> f3caf30c0cb0460d97c3b2172334b1a5f61cfb71
