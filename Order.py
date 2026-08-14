class Order:
    def __init__(self, db_connection):
        self.conn = db_connection

    def place_order(self, product_id, quantity):
        cursor = self.conn.cursor()
        
        # Check if the product exists and has enough stock
        cursor.execute("SELECT name, price, stock FROM products WHERE id=?", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            print("\n❌ Error: Product not found.")
            return
            
        name, price, stock = product
        
        if stock < quantity:
            print(f"\n❌ Error: Not enough stock. Only {stock} left.")
            return
            
        # Calculate total and process order
        total_price = price * quantity
        cursor.execute(
            "INSERT INTO orders (product_id, quantity, total_price) VALUES (?, ?, ?)",
            (product_id, quantity, total_price)
        )
        
        # Deduct the bought quantity from inventory stock
        cursor.execute("UPDATE products SET stock = stock - ? WHERE id=?", (quantity, product_id))
        
        self.conn.commit()
        print(f"\n🛒 Order Placed: {quantity}x {name} for ${total_price:.2f} total.")