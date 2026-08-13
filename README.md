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
