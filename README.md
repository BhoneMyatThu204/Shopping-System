# 🛍️ Shopping System v2.0

A web-based shopping system built with **Python Flask** and **SQLite**.
The system provides separate features for customers and administrators, including product management, shopping cart, checkout, order tracking, and product reviews.

## ✨ Features

### 👤 Customer

* User registration and login
* Browse available products
* View product prices, discounts, stock, and ratings
* Select product size and quantity
* Add products to shopping cart
* Remove products from cart
* Checkout and place orders
* Multiple payment options

  * Cash on Delivery
  * KBZ Pay
  * Wave Money
  * Ayeya Pay
  * A+ Pay
  * Credit Card
* View order history
* Rate purchased products
* Write product reviews

### 👨‍💼 Admin / Owner

* Admin login
* View all products
* Add new products
* Upload product images
* Set product price and stock
* Set product discounts
* View customer orders
* View total available stock
* Manage the shopping system from the admin dashboard

## 🛠️ Technologies

* **Python**
* **Flask**
* **SQLite**
* **HTML5**
* **CSS3**
* **Jinja2**
* **JavaScript**

## 📁 Project Structure

```text
shopping system v2.0/
│
├── app.py                 # Flask application and routes
├── database.py            # SQLite database setup
├── Product.py             # Product management
├── Order.py               # Order management
├── main.py                # Console-based implementation
├── main_gui.py            # GUI implementation
├── add_data.py            # Initial/product data
├── shopping.db            # SQLite database
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── cart.html
│   ├── checkout.html
│   ├── checkout_cart.html
│   ├── history.html
│   ├── admin.html
│   └── add_item.html
│
└── static/
    ├── style.css
    └── images/
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd "shopping system v2.0"
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install Flask

```bash
pip install flask
```

If your project contains a `requirements.txt` file, you can install dependencies with:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

Start the Flask application with:

```bash
python app.py
```

Then open your browser and visit:

```text
http://127.0.0.1:5000/
```

## 🗄️ Database

The project uses **SQLite**.

The database contains the following main tables:

* `users` — stores user accounts and roles
* `products` — stores product information
* `cart` — stores customer cart items
* `orders` — stores customer orders, ratings, and reviews

The database is automatically initialized when the application connects to it.

## 🔐 User Roles

The system supports two roles:

| Role    | Description                                               |
| ------- | --------------------------------------------------------- |
| `user`  | Browse products, manage cart, checkout, and review orders |
| `owner` | Manage products, stock, and customer orders               |

## 💳 Payment

The checkout system supports:

* Cash on Delivery
* Mobile wallet payments
* Credit card payment validation

Payment information is validated before an order is created.

## 📦 Order Process

```text
Register / Login
       ↓
Browse Products
       ↓
Select Product
       ↓
Choose Size & Quantity
       ↓
Add to Cart
       ↓
Checkout
       ↓
Choose Payment Method
       ↓
Place Order
       ↓
Order History
       ↓
Rating & Review
```

## 🌿 Git Workflow

For development, use a separate feature branch:

```bash
git checkout -b Fix-Bug
```

After making changes:

```bash
git add .
git commit -m "Fix shopping system bug"
git push origin Fix-Bug
```

Then create a Pull Request on GitHub.

## ⚠️ Notes

* Do not commit the virtual environment (`venv/`) to Git.
* Do not commit the SQLite database if it contains local/test data.
* Keep sensitive information such as secret keys and payment credentials outside the source code.
* Use environment variables for production configuration.

## 📌 Project Status

**Version:** 2.0
**Type:** Web-based Shopping System
**Backend:** Flask
**Database:** SQLite
