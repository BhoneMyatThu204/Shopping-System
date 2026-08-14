# Shopping System

A Python-based desktop application designed to manage products and track orders. This system utilizes a graphical user interface (GUI) and a local SQLite database to provide a seamless user experience for basic inventory and shopping cart management.

## Features

* **Product Management:** View and manage available items through the system's catalog.
* **Order Tracking:** Process and track user orders from start to finish.
* **Graphical User Interface (GUI):** An intuitive, easy-to-use desktop interface built directly in Python.
* **Database Integration:** Persistent data storage using a local database (`shopping.db`) to ensure products and orders are saved between sessions.

## Project Structure

* `main_gui.py`: The entry point for the application. Run this file to launch the graphical user interface.
* `database.py`: Handles all connections and queries to the local SQLite database.
* `Order.py`: Contains the core logic and object models for managing customer orders.
* `Product.py`: Contains the core logic and object models for the shopping catalog and inventory.
* `shopping.db`: The local SQLite database file (automatically generated/managed by the system).

## Prerequisites

To run this project locally, you will need:
* Python 3.x installed on your machine.

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/shopping-system.git](https://github.com/YOUR-USERNAME/shopping-system.git)
   cd "shopping system"

# 🛍️ UrbanTech E-Commerce Prototype

A modern, responsive e-commerce storefront prototype built with Python and Flask. This project features dynamic backend product generation, a clean UI inspired by real estate filtering systems, and a mock checkout gateway that uses mathematical algorithms for credit card validation.

## ✨ Features

* **Dynamic Product Generation:** The Flask backend automatically generates 100 unique mock products (keyboards, mice, monitors) with randomized prices, stock levels, and warranties upon server startup.
* **Modern UI/UX:** Built with Bootstrap 5, featuring a responsive grid system, floating image overlays, pill-navigation, and a sticky sidebar.
* **Local Asset Management:** Safely serves 100+ local product images using Flask's `url_for` static routing.
* **Algorithmic Payment Validation:** The checkout form implements the **Luhn Algorithm** in Python to mathematically verify if a submitted credit card number matches a valid, real-world format before processing.

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3, Bootstrap 5 (CDN), Bootstrap Icons
* **Template Engine:** Jinja2

## 📁 Project Structure

```text
shopping-system-v1.1/
│
├── app.py                  # Main Flask application and backend logic
├── README.md               # Project documentation
│
├── static/
│   └── images/             # Local product image assets (product_001.jpg, etc.)
│
└── templates/
    ├── index.html          # Main storefront UI and product grid
    └── checkout.html       # Payment form and checkout UI
