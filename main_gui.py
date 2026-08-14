import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db

class ShoppingSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛍️ Shopping Management System")
        self.root.geometry("650x550")
        
        # Connect to our database
        self.conn = connect_db()
        
        # --- TITLE ---
        tk.Label(root, text="Store Inventory & Ordering", font=("Arial", 16, "bold")).pack(pady=10)
        
        # --- PRODUCT TABLE ---
        # Using Treeview to create a grid/table layout
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Price", "Stock"), show="headings")
        self.tree.heading("ID", text="Product ID")
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Price", text="Price ($)")
        self.tree.heading("Stock", text="Stock Available")
        
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Name", width=250, anchor="w")
        self.tree.column("Price", width=100, anchor="center")
        self.tree.column("Stock", width=120, anchor="center")
        self.tree.pack(pady=10, fill="x", padx=20)
        
        # Load data into the table
        self.refresh_table()
        
        # --- ADMIN FRAME: ADD PRODUCT ---
        add_frame = tk.LabelFrame(root, text="Admin: Add New Product", padx=10, pady=10)
        add_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(add_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(add_frame, width=15)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="Price:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_price = tk.Entry(add_frame, width=10)
        self.entry_price.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(add_frame, text="Stock:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_stock = tk.Entry(add_frame, width=10)
        self.entry_stock.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Button(add_frame, text="Add Item", bg="lightblue", command=self.add_product).grid(row=0, column=6, padx=15)
        
        # --- CUSTOMER FRAME: BUY PRODUCT ---
        buy_frame = tk.LabelFrame(root, text="Customer: Place Order", padx=10, pady=10)
        buy_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(buy_frame, text="Product ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_buy_id = tk.Entry(buy_frame, width=10)
        self.entry_buy_id.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(buy_frame, text="Quantity:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_buy_qty = tk.Entry(buy_frame, width=10)
        self.entry_buy_qty.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Button(buy_frame, text="Buy Now", bg="lightgreen", command=self.buy_product).grid(row=0, column=4, padx=15)

    # --- FUNCTIONS ---
    
    def refresh_table(self):
        # Clear existing data in the table
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Fetch fresh data from database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE stock > 0")
        for item in cursor.fetchall():
            # Format the price to show 2 decimal places before inserting into the GUI
            formatted_item = (item[0], item[1], f"${item[2]:.2f}", item[3])
            self.tree.insert("", "end", values=formatted_item)

    def add_product(self):
        name = self.entry_name.get()
        price = self.entry_price.get()
        stock = self.entry_stock.get()
        
        if not name or not price or not stock:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
            
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", 
                           (name, float(price), int(stock)))
            self.conn.commit()
            
            # Clear input fields and refresh UI
            self.entry_name.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.entry_stock.delete(0, tk.END)
            self.refresh_table()
            
            messagebox.showinfo("Success", f"'{name}' added to inventory!")
            
        except ValueError:
            messagebox.showerror("Format Error", "Price and Stock must be valid numbers.")

    def buy_product(self):
        p_id = self.entry_buy_id.get()
        qty = self.entry_buy_qty.get()
        
        if not p_id or not qty:
            messagebox.showwarning("Input Error", "Please enter Product ID and Quantity.")
            return
            
        try:
            p_id = int(p_id)
            qty = int(qty)
            
            cursor = self.conn.cursor()
            cursor.execute("SELECT name, price, stock FROM products WHERE id=?", (p_id,))
            product = cursor.fetchone()
            
            if not product:
                messagebox.showerror("Error", "Product ID not found.")
                return
                
            name, price, stock = product
            
            if stock < qty:
                messagebox.showerror("Out of Stock", f"Not enough stock! Only {stock} left.")
                return
                
            # Process the order
            total_price = price * qty
            cursor.execute("INSERT INTO orders (product_id, quantity, total_price) VALUES (?, ?, ?)", 
                           (p_id, qty, total_price))
            cursor.execute("UPDATE products SET stock = stock - ? WHERE id=?", (qty, p_id))
            self.conn.commit()
            
            # Clear input fields and refresh UI
            self.entry_buy_id.delete(0, tk.END)
            self.entry_buy_qty.delete(0, tk.END)
            self.refresh_table()
            
            messagebox.showinfo("Order Placed", f"Successfully bought {qty}x {name}.\nTotal: ${total_price:.2f}")
            
        except ValueError:
            messagebox.showerror("Format Error", "ID and Quantity must be whole numbers.")

if __name__ == "__main__":
    # Create the main window and start the application
    root = tk.Tk()
    app = ShoppingSystemGUI(root)
    root.mainloop()