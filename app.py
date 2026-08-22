from flask import Flask, render_template, request, redirect, session
import sqlite3
import database
from Order import Order
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "atomic_super_secret_key"

# Configure exactly where uploaded images should be saved
app.config['UPLOAD_FOLDER'] = 'static/images'

def is_valid_credit_card(card_number):
    card_number = card_number.replace(" ", "").replace("-", "")
    if not card_number.isdigit(): return False
    digits = [int(x) for x in card_number][::-1]
    doubled = [x * 2 if i % 2 != 0 else x for i, x in enumerate(digits)]
    subtracted = [x - 9 if x > 9 else x for x in doubled]
    return sum(subtracted) % 10 == 0

@app.route('/')
def home():
    conn = database.connect_db()
    cursor = conn.cursor()
    
    # We now fetch the 'image' column directly from the database!
    cursor.execute("SELECT id, name, price, stock, image FROM products")
    db_products = cursor.fetchall()

    products = []
    for row in db_products:
        products.append({
            "id": row[0], "name": row[1], "price": row[2], "stock": row[3],
            "brand": "Atomic Apparels", "warranty": 1, 
            "image": f"images/{row[4]}" # Uses the actual uploaded image name
        })
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = database.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, 'user'))
            conn.commit()
            session['user'] = username
            session['role'] = 'user'
            return redirect('/')
        except sqlite3.IntegrityError:
            return "<div style='text-align:center; margin-top:100px; font-family:sans-serif;'><h1>Username already taken ❌</h1><br><a href='/register' style='padding: 10px 20px; background: #e33e41; color: white; text-decoration: none; border-radius: 5px;'>Try Again</a></div>"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role') 
        username = request.form.get('username')
        password = request.form.get('password')
        conn = database.connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", (username, password, role))
        user = cursor.fetchone()

        if user:
            session['user'] = username  
            session['role'] = role
            if role == 'owner': return redirect('/admin')
            return redirect('/') 
        else:
            return "<div style='text-align:center; margin-top:100px; font-family:sans-serif;'><h1>Invalid Credentials ❌</h1><br><a href='/login' style='padding: 10px 20px; background: #6b7280; color: white; text-decoration: none; border-radius: 5px;'>Try Again</a></div>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect('/')

@app.route('/admin')
def admin():
    if session.get('role') != 'owner': return redirect('/')
    conn = database.connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(stock) FROM products")
    total_stock = cursor.fetchone()[0]
    if total_stock is None: total_stock = 0
    
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = cursor.fetchall()
    
    cursor.execute("""
        SELECT orders.id, products.name, orders.quantity, orders.total_price, orders.status 
        FROM orders 
        JOIN products ON orders.product_id = products.id
        ORDER BY orders.id DESC
    """)
    orders = cursor.fetchall()
    
    return render_template('admin.html', products=products, orders=orders, total_stock=total_stock)

# --- UPDATED: IMAGE UPLOAD ROUTE ---
@app.route('/admin/add_product', methods=['POST'])
def add_product():
    if session.get('role') == 'owner':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        
        # 1. Grab the image file from the HTML form
        image_file = request.files.get('image')
        image_filename = "placeholder.jpg" # Default fallback
        
        # 2. If an image was uploaded, save it securely to static/images
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            # Make sure the static/images folder exists before saving!
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        # 3. Save everything to the database
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, stock, image) VALUES (?, ?, ?, ?)", (name, price, stock, image_filename))
        conn.commit()
    return redirect('/admin')

@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if session.get('role') == 'owner':
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
    return redirect('/admin')

@app.route('/admin/accept_order/<int:order_id>', methods=['POST'])
def accept_order(order_id):
    if session.get('role') == 'owner':
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status='Accepted' WHERE id=?", (order_id,))
        conn.commit()
    return redirect('/admin')

@app.route('/checkout/<int:product_id>')
def checkout(product_id):
    if 'user' not in session: return redirect('/login')
    return render_template('checkout.html', product_id=product_id)

@app.route('/pay/<int:product_id>', methods=['POST'])
def pay(product_id):
    name = request.form.get('name')
    payment_method = request.form.get('payment_method')
    account_info = request.form.get('account_info') 

    payment_successful = False
    display_method = ""

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

    if payment_successful:
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM products WHERE id=?", (product_id,))
        result = cursor.fetchone()

        if result and result[0] > 0:
            my_order = Order(conn)
            my_order.place_order(product_id, 1) 
            return f"<div style='font-family: sans-serif; text-align: center; margin-top: 100px;'><h1 style='color: #16a34a;'>Payment Successful! 🎉</h1><p style='font-size: 1.2rem;'>Thank you, <strong>{name}</strong>. Your <strong>{display_method}</strong> transaction is complete and inventory has been updated.</p><a href='/' style='padding: 10px 20px; background: #2563eb; color: white; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px;'>Return to Shop</a></div>"
        else:
            return f"<div style='font-family: sans-serif; text-align: center; margin-top: 100px;'><h1 style='color: #e33e41;'>Out of Stock ❌</h1><p style='font-size: 1.2rem;'>Sorry, this item is currently out of stock.</p><a href='/' style='padding: 10px 20px; background: #6b7280; color: white; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px;'>Go Back</a></div>"
    else:
        return f"<div style='font-family: sans-serif; text-align: center; margin-top: 100px;'><h1 style='color: #e33e41;'>Payment Failed ❌</h1><p style='font-size: 1.2rem;'>Please check your payment details and try again.</p><a href='javascript:history.back()' style='padding: 10px 20px; background: #6b7280; color: white; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px;'>Go Back</a></div>"

if __name__ == '__main__':
    app.run(debug=True)