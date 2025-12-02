
-- Create new DB
CREATE DATABASE NewOnlineShoppingDB;
USE ProjectOnlineShoppingDB;

-- Customers Table
CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    address VARCHAR(255)
);

-- Products Table
CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) CHECK (price > 0),
    stock_quantity INT DEFAULT 0
);

-- Orders Table
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    order_date DATE DEFAULT CURDATE(),
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- OrderDetails Table
CREATE TABLE OrderDetails (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT DEFAULT 1 CHECK (quantity > 0),
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Delivery Table
CREATE TABLE Delivery (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    delivery_date DATE,
    delivery_status VARCHAR(50) CHECK (delivery_status IN ('Pending', 'Shipped', 'Delivered', 'Cancelled')),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Payment Table
CREATE TABLE Payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    payment_date DATE DEFAULT CURDATE(),
    payment_method VARCHAR(50) CHECK (payment_method IN ('Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'COD')),
    payment_status VARCHAR(50) CHECK (payment_status IN ('Pending', 'Completed', 'Failed')),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);
