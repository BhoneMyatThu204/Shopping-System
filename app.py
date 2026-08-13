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