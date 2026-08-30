from flask import Flask, render_template, request, redirect, session, flash, jsonify
import sqlite3
import database
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "atomic_super_secret_key"
app.config['UPLOAD_FOLDER'] = 'static/images'

def is_valid_credit_card(card_number):
    card_number = card_number.replace(" ", "").replace("-", "")
    if not card_number.isdigit(): return False
    return sum([x * 2 if i % 2 != 0 else x for i, x in enumerate([int(x) for x in card_number][::-1])]) % 10 == 0

@app.route('/')
def home():
    conn = database.connect_db()
    cursor = conn.cursor()
    # ပစ္စည်းတစ်ခုစီအတွက် ပျမ်းမျှ Rating ကိုပါ တွက်ချက်ယူမည်
    cursor.execute("""
        SELECT p.id, p.name, p.price, p.stock, p.image, p.discount, 
               IFNULL(AVG(NULLIF(o.rating, 0)), 0) as avg_rating 
        FROM products p 
        LEFT JOIN orders o ON p.id = o.product_id 
        GROUP BY p.id
    """)
    db_products = cursor.fetchall()

    products = []
    for row in db_products:
        original_price = row[2]
        discount = row[5]
        final_price = original_price - (original_price * discount / 100)
        
        products.append({
            "id": row[0], "name": row[1], "price": original_price, "final_price": final_price,
            "stock": row[3], "brand": "Atomic Apparels", "image": f"images/{row[4]}", 
            "discount": discount, "rating": row[6]
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
            flash("Account created successfully! 🎉", "success")
            return redirect('/')
        except sqlite3.IntegrityError:
            flash("Username already taken ❌", "error")
            return redirect('/register')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            session['user'] = user[1]  
            session['role'] = user[3]
            flash(f"Welcome back, {session['user']}! 👋", "success")
            if session['role'] == 'owner': return redirect('/admin')
            return redirect('/') 
        else:
            flash("Invalid Credentials ❌", "error")
            return redirect('/login')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    flash("Logged out successfully.", "success")
    return redirect('/')

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user' not in session or session.get('role') != 'user':
        return jsonify({"status": "error", "message": "Please login first"}), 401
        
    username = session['user']
    quantity = int(request.form.get('quantity', 1))
    size = request.form.get('size', 'M')
    
    conn = database.connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT stock FROM products WHERE id=?", (product_id,))
    stock = cursor.fetchone()[0]
    if stock < quantity:
        return jsonify({"status": "error", "message": "Not enough stock available! ❌"}), 400

    cursor.execute("SELECT id, quantity FROM cart WHERE username=? AND product_id=? AND size=?", (username, product_id, size))
    item = cursor.fetchone()
    
    if item:
        new_quantity = item[1] + quantity
        if new_quantity > stock:
            return jsonify({"status": "error", "message": f"Cannot add more. Only {stock} left in stock! ❌"}), 400
        cursor.execute("UPDATE cart SET quantity = ? WHERE id=?", (new_quantity, item[0]))
    else:
        cursor.execute("INSERT INTO cart (username, product_id, quantity, size) VALUES (?, ?, ?, ?)", (username, product_id, quantity, size))
        
    conn.commit()
    return jsonify({"status": "success", "message": f"{quantity} item(s) added to cart! 🛒"}), 200

@app.route('/cart')
def view_cart():
    if 'user' not in session or session.get('role') != 'user': return redirect('/login')
    username = session['user']
    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT cart.id, products.name, products.price, cart.quantity, products.image, products.id, products.discount, cart.size FROM cart JOIN products ON cart.product_id = products.id WHERE cart.username=?''', (username,))
    
    raw_items = cursor.fetchall()
    cart_items = []
    total_price = 0
    for row in raw_items:
        price = row[2]
        discount = row[6]
        final_price = price - (price * discount / 100)
        subtotal = final_price * row[3]
        total_price += subtotal
        cart_items.append({"cart_id": row[0], "name": row[1], "final_price": final_price, "quantity": row[3], "image": row[4], "size": row[7]})
        
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart/<int:cart_id>', methods=['POST'])
def remove_from_cart(cart_id):
    if 'user' in session and session.get('role') == 'user':
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE id=? AND username=?", (cart_id, session['user']))
        conn.commit()
        flash("Item removed from cart.", "success")
    return redirect('/cart')

@app.route('/checkout_cart')
def checkout_cart_page():
    if 'user' not in session or session.get('role') != 'user': return redirect('/login')
    return render_template('checkout_cart.html')

@app.route('/pay_cart', methods=['POST'])
def pay_cart():
    if 'user' not in session or session.get('role') != 'user': return redirect('/login')

    username = session['user']
    payment_method = request.form.get('payment_method')
    account_info = request.form.get('account_info') 
    order_note = request.form.get('order_note', '')

    payment_successful = False
    display_method = ""

    if payment_method == 'cod':
        payment_successful = True
        display_method = "Cash on Delivery"
    elif payment_method == 'other':
        if is_valid_credit_card(account_info):
            payment_successful = True
            display_method = "Credit Card"
    else:
        clean_number = account_info.replace(" ", "").replace("-", "") if account_info else ""
        if clean_number.isdigit() and len(clean_number) >= 9:
            payment_successful = True
            method_names = {'kbz': 'KBZ Pay', 'wave': 'Wave Money', 'ayeya': 'Ayeya Pay', 'aplus': 'A+ Pay'}
            display_method = method_names.get(payment_method, 'Mobile Wallet')

    if payment_successful:
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, quantity, size FROM cart WHERE username=?", (username,))
        cart_items = cursor.fetchall()

        if not cart_items:
            flash("Your cart is empty.", "error")
            return redirect('/')

        for item in cart_items:
            product_id, quantity, size = item[0], item[1], item[2]
            cursor.execute("SELECT price, stock, discount FROM products WHERE id=?", (product_id,))
            product = cursor.fetchone()
            
            if product and product[1] >= quantity:
                final_price = product[0] - (product[0] * product[2] / 100)
                total_price = final_price * quantity
                cursor.execute("INSERT INTO orders (username, product_id, quantity, size, total_price, status, order_note, rating, review_comment) VALUES (?, ?, ?, ?, ?, ?, ?, 0, '')", 
                               (username, product_id, quantity, size, total_price, "Pending", order_note))
                cursor.execute("UPDATE products SET stock = stock - ? WHERE id=?", (quantity, product_id))
        
        cursor.execute("DELETE FROM cart WHERE username=?", (username,))
        conn.commit()
        flash(f"Order Placed! Paid via {display_method}. 🎉", "success")
        return redirect('/history')
    else:
        flash("Payment Failed ❌ Please check your details.", "error")
        return redirect('/checkout_cart')

@app.route('/history')
def history():
    if 'user' not in session or session.get('role') != 'user': return redirect('/login')
    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT orders.id, products.name, orders.quantity, orders.total_price, orders.status, products.image, orders.size, orders.rating, orders.review_comment
        FROM orders JOIN products ON orders.product_id = products.id
        WHERE orders.username=? ORDER BY orders.id DESC
    """, (session['user'],))
    orders = cursor.fetchall()
    return render_template('history.html', orders=orders)

@app.route('/rate_order/<int:order_id>', methods=['POST'])
def rate_order(order_id):
    if 'user' not in session or session.get('role') != 'user': return redirect('/login')
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('review_comment', '')
    
    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET rating=?, review_comment=? WHERE id=? AND username=?", (rating, comment, order_id, session['user']))
    conn.commit()
    flash("Thank you for your feedback! ⭐", "success")
    return redirect('/history')

@app.route('/admin')
def admin():
    if session.get('role') != 'owner': return redirect('/')
    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(stock) FROM products")
    total_stock = cursor.fetchone()[0] or 0
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = cursor.fetchall()
    
    cursor.execute("""
        SELECT orders.id, products.name, orders.quantity, orders.total_price, orders.status, orders.username, orders.size, orders.order_note 
        FROM orders JOIN products ON orders.product_id = products.id ORDER BY orders.id DESC
    """)
    orders = cursor.fetchall()
    return render_template('admin.html', products=products, orders=orders, total_stock=total_stock)

@app.route('/admin/add_product', methods=['POST'])
def add_product():
    if session.get('role') == 'owner':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        discount = int(request.form.get('discount')) 
        
        image_file = request.files.get('image')
        image_filename = "placeholder.jpg" 
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, stock, image, discount) VALUES (?, ?, ?, ?, ?)", (name, price, stock, image_filename, discount))
        conn.commit()
        flash("Product added successfully!", "success")
    return redirect('/admin')

@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if session.get('role') == 'owner':
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        flash("Product removed.", "success")
    return redirect('/admin')

@app.route('/admin/accept_order/<int:order_id>', methods=['POST'])
def accept_order(order_id):
    if session.get('role') == 'owner':
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status='Accepted' WHERE id=?", (order_id,))
        conn.commit()
        flash("Order accepted.", "success")
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)