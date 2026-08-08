# from database import connect_db
# from Product import Product
# from Order import Order

# def main():
#     # Initialize database and modules
#     db_conn = connect_db()
#     inventory = Product(db_conn)
#     shop = Order(db_conn)

#     while True:
#         print("\n=== 🛍️ Shopping Management System ===")
#         print("1. Add New Product (Admin)")
#         print("2. View Available Products")
#         print("3. Buy a Product")
#         print("4. Exit")
        
#         choice = input("Enter your choice (1-4): ")
        
#         if choice == '1':
#             name = input("Enter product name: ")
#             price = float(input("Enter price: $"))
#             stock = int(input("Enter stock quantity: "))
#             inventory.add_product(name, price, stock)
            
#         elif choice == '2':
#             inventory.view_products()
            
#         elif choice == '3':
#             inventory.view_products() # Show items before buying
#             prod_id = int(input("\nEnter the ID of the product you want to buy: "))
#             qty = int(input("Enter the quantity: "))
#             shop.place_order(prod_id, qty)
            
#         elif choice == '4':
#             print("\nThank you for using the Shopping System. Goodbye!")
#             db_conn.close()
#             break
            
#         else:
#             print("\nInvalid choice. Please try again.")

# if __name__ == "__main__":
#     main()