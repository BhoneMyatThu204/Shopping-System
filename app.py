from flask import Flask, render_template, request, redirect
import database
from Order import Order

app = Flask(__name__)

# --- MATH LOGIC FOR "OTHER" (CREDIT CARDS) ---
def is_valid_credit_card(card_number):
    card_number = card_number.replace(" ", "").replace("-", "")
    if not card_number.isdigit(): return False
    digits = [int(x) for x in card_number][::-1]
    doubled = [x * 2 if i % 2 != 0 else x for i, x in enumerate(digits)]
    subtracted = [x - 9 if x > 9 else x for x in doubled]
    return sum(subtracted) % 10 == 0

# --- ROUTES ---
@app.route('/')
def home():
    # 1. Connect to your SQLite Database
    conn = database.connect_db()
    cursor = conn.cursor()
    
    # 2. Fetch all real products from shopping.db
    cursor.execute("SELECT id, name, price, stock FROM products")
    db_products = cursor.fetchall()
    
    # 3. Format the database rows into dictionaries so your HTML UI can read them
    products = []
    for row in db_products:
        products.append({
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "stock": row[3],
            "brand": "TechCorp", # UI filler
            "warranty": 1,       # UI filler
            "image": f"images/product_{row[0]:03}.jpg" # Dynamically loads product_001.jpg based on DB id!
        })
        
    return render_template('index.html', products=products)

@app.route('/checkout/<int:product_id>')
def checkout(product_id):
    # We pass the product_id to the checkout page so it knows what the user is buying
    return render_template('checkout.html', product_id=product_id)

# Notice we added <int:product_id> here so the payment route knows which product to deduct from inventory
@app.route('/pay/<int:product_id>', methods=['POST'])
def pay(product_id):
    name = request.form.get('name')
    payment_method = request.form.get('payment_method')
    account_info = request.form.get('account_info') 
    
    payment_successful = False
    display_method = ""
    
    # Validate Payment Details
    if payment_method == 'other':
        if is_valid_credit_card(account_info):
            payment_successful = True
            display_method = "Credit Card"
    else:
        clean_number = account_info.replace(" ", "").replace("-", "")
        if clean_number.isdigit() and len(clean_number) >= 9:
            payment_successful = True
            method_names = {'kbz': 'KBZ Pay', 'wave': 'Wave Money', 'ayeya': 'Ayeya Pay', 'aplus': 'A+ Pay'}
            display_method = method_names.get(payment_method, 'Mobile Wallet')
            
    # Process the Order if Payment is Valid
    if payment_successful:
        conn = database.connect_db()
        cursor = conn.cursor()
        
        # Security Check: Ensure the item isn't out of stock before processing
        cursor.execute("SELECT stock FROM products WHERE id=?", (product_id,))
        result = cursor.fetchone()
        
        if result and result[0] > 0:
            # Connect to your Order.py logic!
            my_order = Order(conn)
            my_order.place_order(product_id, 1) # Assuming user buys a quantity of 1
            
            return f"<div style='font-family: sans-serif; text-align: center; margin-top: 100px;'><h1 style='color: #198754;'>Payment Successful! 🎉</h1><p style='font-size: 1.2rem;'>Thank you, <strong>{name}</strong>. Your <strong>{display_method}</strong> transaction is complete and inventory has been updated.</p><a href='/' style='padding: 10px 20px; background: #0d6efd; color: white; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px;'>Return to Shop</a></div>"
        else:
            return f"<div style='font-family: sans-serif; text-align: center; margin-top: 100px;'><h1 style='color: #dc3545;'>Out of Stock ❌</h1><p style='font-size: 1.2rem;'>Sorry, this item is currently out of stock.</p><a href='/' style='padding: 10px 20px; background: #6c757d; color: white; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px;'>Go Back</a></div>"
    
    else:
        return f"<div style='font-family: sans-serif; text-align: center; margin-top: 100px;'><h1 style='color: #dc3545;'>Payment Failed ❌</h1><p style='font-size: 1.2rem;'>Please check your payment details and try again.</p><a href='javascript:history.back()' style='padding: 10px 20px; background: #6c757d; color: white; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px;'>Go Back</a></div>"

if __name__ == '__main__':
from flask import Flask, render_template, request
import random # Added this import for the generator

app = Flask(__name__)

def is_valid_credit_card(card_number):
    card_number = card_number.replace(" ", "").replace("-", "")
    if not card_number.isdigit(): return False
    digits = [int(x) for x in card_number][::-1]
    doubled = [x * 2 if i % 2 != 0 else x for i, x in enumerate(digits)]
    subtracted = [x - 9 if x > 9 else x for x in doubled]
    return sum(subtracted) % 10 == 0

# --- NEW GENERATOR PLACED HERE ---
def generate_mock_products():
    products = []
    base_names = ["Mechanical Keyboard", "Wireless Mouse", "4K Ultra HD Monitor", "Gaming Headset", "HD Webcam", "USB-C Hub", "Laptop Stand", "Ergonomic Desk Mat"]
    base_brands = ["TechCorp, CA", "ErgoLogi, TX", "VisionX, NY", "AudioPro, WA", "GearUp, FL"]
    
    for i in range(1, 101):
        name = random.choice(base_names)
        products.append({
            "id": i, 
            "name": f"{name} Gen-{random.randint(1, 9)}", 
            "price": round(random.uniform(25.0, 499.0), 2), 
            "brand": random.choice(base_brands), 
            "stock": random.randint(0, 15), 
            "warranty": random.randint(1, 5), 
            "image": f"images/product_{i:03}.jpg" # Pulls from your static/images folder
        })
    return products

# Generate the items once when the server starts
MOCK_PRODUCTS = generate_mock_products()

@app.route('/')
def home():
    # We replaced the hardcoded list with the MOCK_PRODUCTS variable
    return render_template('index.html', products=MOCK_PRODUCTS)

@app.route('/checkout/<int:product_id>')
def checkout(product_id):
    return render_template('checkout.html', product_id=product_id)

@app.route('/pay', methods=['POST'])
def pay():
    name = request.form.get('name')
    card_number = request.form.get('card_number')
    if is_valid_credit_card(card_number):
        return f"<div style='text-align: center; margin-top: 100px;'><h1 style='color: #198754;'>Payment Successful! 🎉</h1><a href='/'>Return</a></div>"
    else:
        return f"<div style='text-align: center; margin-top: 100px;'><h1 style='color: #dc3545;'>Payment Failed ❌</h1><a href='javascript:history.back()'>Go Back</a></div>"

if __name__ == '__main__':
    app.run(debug=True)