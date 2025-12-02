import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector

class OnlineShoppingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Shopping Management System")
        self.root.geometry("1500x800")

        # Custom Colors
        self.colors = {
            'bg_primary': '#4A90E2',  # Bright Blue
            'bg_secondary': '#50E3C2',  # Vibrant Teal
            'text_primary': '#FFFFFF',  # White
            'accent_color': '#FF6B6B',  # Coral Red
            'hover_color': '#4ECDC4'  # Bright Mint
        }

        # Configure root window style
        self.root.configure(bg=self.colors['bg_primary'])

        # Custom Style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # More customizable theme
        
        # Notebook (Tab) Style
        self.style.configure('TNotebook', background=self.colors['bg_primary'])
        self.style.configure('TNotebook.Tab', 
            background=self.colors['bg_secondary'], 
            foreground=self.colors['text_primary'],
            padding=[10, 5]
        )
        self.style.map('TNotebook.Tab', 
            background=[('selected', self.colors['accent_color'])],
            expand=[('selected', [1, 1, 1])]
        )

        # Treeview Style
        self.style.configure('Treeview', 
            background=self.colors['text_primary'], 
            foreground='black',
            rowheight=25,
            fieldbackground=self.colors['text_primary']
        )
        self.style.map('Treeview', 
            background=[('selected', self.colors['hover_color'])]
        )

        # Create Notebook with vibrant tabs
        self.notebook = ttk.Notebook(root, style='TNotebook')
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Setup tabs
        self.setup_customers_tab()
        self.setup_products_tab()
        self.setup_orders_tab()
        self.setup_delivery_tab()
        self.setup_payment_tab()

    def connect_db(self):
        return mysql.connector.connect(
            host="localhost", 
            user="root",  
            password="amruthadb",  
            database="NewOnlineShoppingDB",
        )

    def execute_query(self, query, params=(), fetch=False):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
                conn.close()
                return result
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False

    def setup_customers_tab(self):
        customers_frame = ttk.Frame(self.notebook)
        self.notebook.add(customers_frame, text="Customers")

        # Customers Tree
        self.customers_tree = ttk.Treeview(customers_frame, height=15, columns=("ID", "Name", "Email", "Phone", "Address"))
        for col in ["ID", "Name", "Email", "Phone", "Address"]:
            self.customers_tree.heading(col, text=col)
        self.customers_tree.grid(row=2, column=0, columnspan=6, sticky="nsew")

        # Customers Entries
        entries_config = [
            ("Name:", 0, 0, 'customer_name'),
            ("Email:", 0, 2, 'customer_email'),
            ("Phone:", 0, 4, 'customer_phone'),
            ("Address:", 1, 0, 'customer_address')
        ]

        for label_text, row, col, attr_name in entries_config:
            tk.Label(customers_frame, text=label_text, 
                     fg=self.colors['text_primary'], 
                     bg=self.colors['bg_primary']).grid(row=row, column=col)
            
            setattr(self, attr_name, tk.Entry(customers_frame, bg='white', fg='black', width=30))
            getattr(self, attr_name).grid(row=row, column=col+1)

        # Customers Buttons
        button_config = [
            ("Add Customer", self.add_customer, 1, 4, self.colors['accent_color']),
            ("Update Customer", self.update_customer, 1, 5, self.colors['bg_secondary']),
            ("Delete Customer", self.delete_customer, 2, 6, self.colors['hover_color']),
            ("Refresh", self.fetch_customers, 0, 6, self.colors['accent_color'])
        ]

        for text, command, row, col, color in button_config:
            tk.Button(customers_frame, text=text, command=command, 
                      bg=color, fg=self.colors['text_primary']).grid(row=row, column=col)

        # Bind treeview selection
        self.customers_tree.bind('<<TreeviewSelect>>', self.load_customer_data)

        self.fetch_customers()

    def fetch_customers(self):
        for i in self.customers_tree.get_children():
            self.customers_tree.delete(i)
        customers = self.execute_query("SELECT * FROM Customers", fetch=True)
        for customer in customers:
            self.customers_tree.insert("", "end", values=customer)

    def add_customer(self):
        name = self.customer_name.get()
        email = self.customer_email.get()
        phone = self.customer_phone.get()
        address = self.customer_address.get()

        if self.execute_query(
            "INSERT INTO Customers (name, email, phone, address) VALUES (%s, %s, %s, %s)",
            (name, email, phone, address)
        ):
            self.fetch_customers()
            messagebox.showinfo("Success", "Customer added successfully!")

    def load_customer_data(self, event):
        selected = self.customers_tree.selection()
        if selected:
            values = self.customers_tree.item(selected[0])['values']
            self.customer_name.delete(0, tk.END)
            self.customer_name.insert(0, values[1])
            self.customer_email.delete(0, tk.END)
            self.customer_email.insert(0, values[2])
            self.customer_phone.delete(0, tk.END)
            self.customer_phone.insert(0, values[3])
            self.customer_address.delete(0, tk.END)
            self.customer_address.insert(0, values[4])

    def update_customer(self):
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a customer to update")
            return

        customer_id = self.customers_tree.item(selected[0])['values'][0]
        name = self.customer_name.get()
        email = self.customer_email.get()
        phone = self.customer_phone.get()
        address = self.customer_address.get()

        if self.execute_query(
            "UPDATE Customers SET name=%s, email=%s, phone=%s, address=%s WHERE customer_id=%s",
            (name, email, phone, address, customer_id)
        ):
            self.fetch_customers()
            messagebox.showinfo("Success", "Customer updated successfully!")

    def delete_customer(self):
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a customer to delete")
            return

        customer_id = self.customers_tree.item(selected[0])['values'][0]
        if self.execute_query("DELETE FROM Customers WHERE customer_id=%s", (customer_id,)):
            self.fetch_customers()
            messagebox.showinfo("Success", "Customer deleted successfully!")

    def setup_products_tab(self):
        products_frame = ttk.Frame(self.notebook)
        self.notebook.add(products_frame, text="Products")

        # Products Tree
        self.products_tree = ttk.Treeview(products_frame, height=15, columns=("ID", "Name", "Price", "Stock Quantity"))
        for col in ["ID", "Name", "Price", "Stock Quantity"]:
            self.products_tree.heading(col, text=col)
        self.products_tree.grid(row=2, column=0, columnspan=6, sticky="nsew")

        # Products Entries
        entries_config = [
            ("Name:", 0, 0, 'product_name'),
            ("Price:", 0, 2, 'product_price'),
            ("Stock Quantity:", 0, 4, 'product_stock')
        ]

        for label_text, row, col, attr_name in entries_config:
            tk.Label(products_frame, text=label_text, 
                     fg=self.colors['text_primary'], 
                     bg=self.colors['bg_primary']).grid(row=row, column=col)
            
            setattr(self, attr_name, tk.Entry(products_frame, bg='white', fg='black', width=30))
            getattr(self, attr_name).grid(row=row, column=col+1)

        # Products Buttons
        button_config = [
            ("Add Product", self.add_product, 1, 4, self.colors['accent_color']),
            ("Update Product", self.update_product, 1, 5, self.colors['bg_secondary']),
            ("Delete Product", self.delete_product, 2, 6, self.colors['hover_color']),
            ("Refresh", self.fetch_products, 0, 6, self.colors['accent_color'])
        ]

        for text, command, row, col, color in button_config:
            tk.Button(products_frame, text=text, command=command, 
                      bg=color, fg=self.colors['text_primary']).grid(row=row, column=col)

        # Bind treeview selection
        self.products_tree.bind('<<TreeviewSelect>>', self.load_product_data)

        self.fetch_products()

    def fetch_products(self):
        for i in self.products_tree.get_children():
            self.products_tree.delete(i)
        products = self.execute_query("SELECT * FROM Products", fetch=True)
        for product in products:
            self.products_tree.insert("", "end", values=product)

    def add_product(self):
        name = self.product_name.get()
        price = self.product_price.get()
        stock = self.product_stock.get()

        if self.execute_query(
            "INSERT INTO Products (name, price, stock_quantity) VALUES (%s, %s, %s)",
            (name, price, stock)
        ):
            self.fetch_products()
            messagebox.showinfo("Success", "Product added successfully!")

    def load_product_data(self, event):
        selected = self.products_tree.selection()
        if selected:
            values = self.products_tree.item(selected[0])['values']
            self.product_name.delete(0, tk.END)
            self.product_name.insert(0, values[1])
            self.product_price.delete(0, tk.END)
            self.product_price.insert(0, values[2])
            self.product_stock.delete(0, tk.END)
            self.product_stock.insert(0, values[3])

    def update_product(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a product to update")
            return

        product_id = self.products_tree.item(selected[0])['values'][0]
        name = self.product_name.get()
        price = self.product_price.get()
        stock = self.product_stock.get()

        if self.execute_query(
            "UPDATE Products SET name=%s, price=%s, stock_quantity=%s WHERE product_id=%s",
            (name, price, stock, product_id)
        ):
            self.fetch_products()
            messagebox.showinfo("Success", "Product updated successfully!")

    def delete_product(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a product to delete")
            return

        product_id = self.products_tree.item(selected[0])['values'][0]
        if self.execute_query("DELETE FROM Products WHERE product_id=%s", (product_id,)):
            self.fetch_products()
            messagebox.showinfo("Success", "Product deleted successfully!")

    def setup_orders_tab(self):
        orders_frame = ttk.Frame(self.notebook)
        self.notebook.add(orders_frame, text="Orders")

        # Orders Tree
        self.orders_tree = ttk.Treeview(orders_frame, height=15, columns=("ID", "Customer ID", "Order Date", "Total Amount"))
        for col in ["ID", "Customer ID", "Order Date", "Total Amount"]:
            self.orders_tree.heading(col, text=col)
        self.orders_tree.grid(row=2, column=0, columnspan=6, sticky="nsew")

        # Orders Entries
        entries_config = [
            ("Customer ID:", 0, 0, 'order_customer_id'),
            ("Total Amount:", 0, 2, 'order_total_amount')
        ]

        for label_text, row, col, attr_name in entries_config:
            tk.Label(orders_frame, text=label_text, 
                     fg=self.colors['text_primary'], 
                     bg=self.colors['bg_primary']).grid(row=row, column=col)
            
            setattr(self, attr_name, tk.Entry(orders_frame, bg='white', fg='black', width=30))
            getattr(self, attr_name).grid(row=row, column=col+1)

        # Orders Buttons
        button_config = [
            ("Add Order", self.add_order, 1, 4, self.colors['accent_color']),
            ("Update Order", self.update_order, 1, 5, self.colors['bg_secondary']),
            ("Delete Order", self.delete_order, 2, 6, self.colors['hover_color']),
            ("Refresh", self.fetch_orders, 0, 6, self.colors['accent_color'])
        ]

        for text, command, row, col, color in button_config:
            tk.Button(orders_frame, text=text, command=command, 
                      bg=color, fg=self.colors['text_primary']).grid(row=row, column=col)

        # Bind treeview selection
        self.orders_tree.bind('<<TreeviewSelect>>', self.load_order_data)

        self.fetch_orders()

    def fetch_orders(self):
        for i in self.orders_tree.get_children():
            self.orders_tree.delete(i)
        orders = self.execute_query("SELECT * FROM Orders", fetch=True)
        for order in orders:
            self.orders_tree.insert("", "end", values=order)

    def add_order(self):
        customer_id = self.order_customer_id.get()
        total_amount = self.order_total_amount.get()

        if self.execute_query(
            "INSERT INTO Orders (customer_id, total_amount) VALUES (%s, %s)",
            (customer_id, total_amount)
        ):
            self.fetch_orders()
            messagebox.showinfo("Success", "Order added successfully!")

    def load_order_data(self, event):
        selected = self.orders_tree.selection()
        if selected:
            values = self.orders_tree.item(selected[0])['values']
            self.order_customer_id.delete(0, tk.END)
            self.order_customer_id.insert(0, values[1])
            self.order_total_amount.delete(0, tk.END)
            self.order_total_amount.insert(0, values[3])

    def update_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an order to update")
            return

        order_id = self.orders_tree.item(selected[0])['values'][0]
        customer_id = self.order_customer_id.get()
        total_amount = self.order_total_amount.get()

        if self.execute_query(
            "UPDATE Orders SET customer_id=%s, total_amount=%s WHERE order_id=%s",
            (customer_id, total_amount, order_id)
        ):
            self.fetch_orders()
            messagebox.showinfo("Success", "Order updated successfully!")

    def delete_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an order to delete")
            return

        order_id = self.orders_tree.item(selected[0])['values'][0]
        if self.execute_query("DELETE FROM Orders WHERE order_id=%s", (order_id,)):
            self.fetch_orders()
            messagebox.showinfo("Success", "Order deleted successfully!")

    def setup_delivery_tab(self):
        delivery_frame = ttk.Frame(self.notebook)
        self.notebook.add(delivery_frame, text="Delivery")

        # Delivery Tree
        self.delivery_tree = ttk.Treeview(delivery_frame, height=15, columns=("ID", "Order ID", "Delivery Date", "Delivery Status"))
        for col in ["ID", "Order ID", "Delivery Date", "Delivery Status"]:
            self.delivery_tree.heading(col, text=col)
        self.delivery_tree.grid(row=2, column=0, columnspan=6, sticky="nsew")

        # Delivery Entries
        entries_config = [
            ("Order ID:", 0, 0, 'delivery_order_id'),
            ("Delivery Date (YYYY-MM-DD):", 0, 2, 'delivery_date')
        ]

        for label_text, row, col, attr_name in entries_config:
            tk.Label(delivery_frame, text=label_text, 
                     fg=self.colors['text_primary'], 
                     bg=self.colors['bg_primary']).grid(row=row, column=col)
            
            setattr(self, attr_name, tk.Entry(delivery_frame, bg='white', fg='black', width=30))
            getattr(self, attr_name).grid(row=row, column=col+1)

        # Delivery Status
        tk.Label(delivery_frame, text="Delivery Status:", 
                 fg=self.colors['text_primary'], 
                 bg=self.colors['bg_primary']).grid(row=1, column=0)
        self.delivery_status = ttk.Combobox(delivery_frame, 
                                            values=["Pending", "Shipped", "Delivered", "Cancelled"])
        self.delivery_status.grid(row=1, column=1)

        # Delivery Buttons
        button_config = [
            ("Add Delivery", self.add_delivery, 1, 4, self.colors['accent_color']),
            ("Update Delivery", self.update_delivery, 1, 5, self.colors['bg_secondary']),
            ("Delete Delivery", self.delete_delivery, 2, 6, self.colors['hover_color']),
            ("Refresh", self.fetch_deliveries, 0, 6, self.colors['accent_color'])
        ]

        for text, command, row, col, color in button_config:
            tk.Button(delivery_frame, text=text, command=command, 
                      bg=color, fg=self.colors['text_primary']).grid(row=row, column=col)

        # Bind treeview selection
        self.delivery_tree.bind('<<TreeviewSelect>>', self.load_delivery_data)

        self.fetch_deliveries()

    def fetch_deliveries(self):
        for i in self.delivery_tree.get_children():
            self.delivery_tree.delete(i)
        deliveries = self.execute_query("SELECT * FROM Delivery", fetch=True)
        for delivery in deliveries:
            self.delivery_tree.insert("", "end", values=delivery)

    def add_delivery(self):
        order_id = self.delivery_order_id.get()
        delivery_date = self.delivery_date.get()
        delivery_status = self.delivery_status.get()

        if self.execute_query(
            "INSERT INTO Delivery (order_id, delivery_date, delivery_status) VALUES (%s, %s, %s)",
            (order_id, delivery_date, delivery_status)
        ):
            self.fetch_deliveries()
            messagebox.showinfo("Success", "Delivery added successfully!")

    def load_delivery_data(self, event):
        selected = self.delivery_tree.selection()
        if selected:
            values = self.delivery_tree.item(selected[0])['values']
            self.delivery_order_id.delete(0, tk.END)
            self.delivery_order_id.insert(0, values[1])
            self.delivery_date.delete(0, tk.END)
            self.delivery_date.insert(0, values[2])
            self.delivery_status.set(values[3])

    def update_delivery(self):
        selected = self.delivery_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a delivery to update")
            return

        delivery_id = self.delivery_tree.item(selected[0])['values'][0]
        order_id = self.delivery_order_id.get()
        delivery_date = self.delivery_date.get()
        delivery_status = self.delivery_status.get()

        if self.execute_query(
            "UPDATE Delivery SET order_id=%s, delivery_date=%s, delivery_status=%s WHERE delivery_id=%s",
            (order_id, delivery_date, delivery_status, delivery_id)
        ):
            self.fetch_deliveries()
            messagebox.showinfo("Success", "Delivery updated successfully!")

    def delete_delivery(self):
        selected = self.delivery_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a delivery to delete")
            return

        delivery_id = self.delivery_tree.item(selected[0])['values'][0]
        if self.execute_query("DELETE FROM Delivery WHERE delivery_id=%s", (delivery_id,)):
            self.fetch_deliveries()
            messagebox.showinfo("Success", "Delivery deleted successfully!")

    def setup_payment_tab(self):
        payment_frame = ttk.Frame(self.notebook)
        self.notebook.add(payment_frame, text="Payment")

        # Payment Tree
        self.payment_tree = ttk.Treeview(payment_frame, height=15, columns=("ID", "Order ID", "Payment Date", "Payment Method", "Payment Status"))
        for col in ["ID", "Order ID", "Payment Date", "Payment Method", "Payment Status"]:
            self.payment_tree.heading(col, text=col)
        self.payment_tree.grid(row=2, column=0, columnspan=6, sticky="nsew")

        # Payment Entries
        entries_config = [
            ("Order ID:", 0, 0, 'payment_order_id'),
            ("Payment Date (YYYY-MM-DD):", 0, 2, 'payment_date')
        ]

        for label_text, row, col, attr_name in entries_config:
            tk.Label(payment_frame, text=label_text, 
                     fg=self.colors['text_primary'], 
                     bg=self.colors['bg_primary']).grid(row=row, column=col)
            
            setattr(self, attr_name, tk.Entry(payment_frame, bg='white', fg='black', width=30))
            getattr(self, attr_name).grid(row=row, column=col+1)

        # Payment Method and Status Dropdowns
        tk.Label(payment_frame, text="Payment Method:", 
                 fg=self.colors['text_primary'], 
                 bg=self.colors['bg_primary']).grid(row=1, column=0)
        self.payment_method = ttk.Combobox(payment_frame, 
                                            values=["Credit Card", "Debit Card", "UPI", "Net Banking", "COD"])
        self.payment_method.grid(row=1, column=1)

        tk.Label(payment_frame, text="Payment Status:", 
                 fg=self.colors['text_primary'], 
                 bg=self.colors['bg_primary']).grid(row=1, column=2)
        self.payment_status = ttk.Combobox(payment_frame, 
                                            values=["Pending", "Completed", "Failed"])
        self.payment_status.grid(row=1, column=3)

        # Payment Buttons
        button_config = [
            ("Add Payment", self.add_payment, 1, 4, self.colors['accent_color']),
            ("Update Payment", self.update_payment, 1, 5, self.colors['bg_secondary']),
            ("Delete Payment", self.delete_payment, 2, 6, self.colors['hover_color']),
            ("Refresh", self.fetch_payments, 0, 6, self.colors['accent_color'])
        ]

        for text, command, row, col, color in button_config:
            tk.Button(payment_frame, text=text, command=command, 
                      bg=color, fg=self.colors['text_primary']).grid(row=row, column=col)

        # Bind treeview selection
        self.payment_tree.bind('<<TreeviewSelect>>', self.load_payment_data)

        self.fetch_payments()

    def fetch_payments(self):
        for i in self.payment_tree.get_children():
            self.payment_tree.delete(i)
        payments = self.execute_query("SELECT * FROM Payment", fetch=True)
        for payment in payments:
            self.payment_tree.insert("", "end", values=payment)

    def add_payment(self):
        order_id = self.payment_order_id.get()
        payment_method = self.payment_method.get()
        payment_status = self.payment_status.get()

        if self.execute_query(
            "INSERT INTO Payment (order_id, payment_method, payment_status) VALUES (%s, %s, %s)",
            (order_id, payment_method, payment_status)
        ):
            self.fetch_payments()
            messagebox.showinfo("Success", "Payment added successfully!")

    def load_payment_data(self, event):
        selected = self.payment_tree.selection()
        if selected:
            values = self.payment_tree.item(selected[0])['values']
            self.payment_order_id.delete(0, tk.END)
            self.payment_order_id.insert(0, values[1])
            self.payment_method.set(values[3])
            self.payment_status.set(values[4])

    def update_payment(self):
        selected = self.payment_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a payment to update")
            return

        payment_id = self.payment_tree.item(selected[0])['values'][0]
        order_id = self.payment_order_id.get()
        payment_method = self.payment_method.get()
        payment_status = self.payment_status.get()

        if self.execute_query(
            "UPDATE Payment SET order_id=%s, payment_method=%s, payment_status=%s WHERE payment_id=%s",
            (order_id, payment_method, payment_status, payment_id)
        ):
            self.fetch_payments()
            messagebox.showinfo("Success", "Payment updated successfully!")

    def delete_payment(self):
        selected = self.payment_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a payment to delete")
            return

        payment_id = self.payment_tree.item(selected[0])['values'][0]
        if self.execute_query("DELETE FROM Payment WHERE payment_id=%s", (payment_id,)):
            self.fetch_payments()
            messagebox.showinfo("Success", "Payment deleted successfully!")

def main():
    root = tk.Tk()
    app = OnlineShoppingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
