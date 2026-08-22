class Product:
    def __init__(self, db_connection):
        self.conn = db_connection

    def add_product(self, name, price, stock):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
            (name, price, stock)
        )
        self.conn.commit()
        print(f"\n✅ Success: '{name}' added to inventory!")

    def view_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE stock > 0")
        items = cursor.fetchall()
        
        print("\n--- Available Products ---")
        print(f"{'ID':<5} | {'Name':<15} | {'Price':<10} | {'Stock'}")
        print("-" * 45)
        for item in items:
            print(f"{item[0]:<5} | {item[1]:<15} | ${item[2]:<9} | {item[3]}")