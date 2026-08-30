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
    
    print("Adding clothing products...")
    clothing_items = ["Graphic Tee", "Summer Shorts", "Leather Jacket", "Winter Beanie", "Polo Shirt", "Cargo Pants", "Running Shoes"]
    
    for i in range(1, 101):
        if i == 1: name = "Classic T-Shirt"
        elif i == 2: name = "Urban Sneakers"
        elif i == 3: name = "Denim Jeans"
        elif i == 4: name = "Cozy Hoodie"
        else: name = random.choice(clothing_items)
        
        price = round(random.uniform(15.0, 150.0), 2)
        
        # Make some items Out of Stock (0) and give some a Discount
        stock = 0 if i in [3, 7, 12] else random.randint(5, 50)
        discount = random.choice([0, 0, 0, 10, 20, 50]) # Random discounts
        
        image_name = f"product_{i:03}.jpg" if i <= 100 else "placeholder.jpg"
        
        cursor.execute("INSERT INTO products (name, price, stock, image, discount) VALUES (?, ?, ?, ?, ?)", 
                       (name, price, stock, image_name, discount))
        
    conn.commit()
    print("✅ Successfully updated! You can now log in as Owner with username: admin / password: admin123")
    conn.close()

if __name__ == "__main__":
    reset_database()