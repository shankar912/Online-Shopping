-- Create a new customer
INSERT INTO Customers (name, email, phone, address)
VALUES ('John Doe', 'john.doe@example.com', '9876543210', '123 Main St, NY');

-- Read all customers
SELECT * FROM Customers;

-- Update customer details
UPDATE Customers 
SET phone = '9998887776', address = '456 Park Ave, NY' 
WHERE customer_id = 1;

-- Delete a customer
DELETE FROM Customers WHERE customer_id = 1;

------------------------------------------------------------

-- Create a new product
INSERT INTO Products (name, price, stock_quantity)
VALUES ('Laptop', 999.99, 10);

-- Read all products
SELECT * FROM Products;

-- Update product details
UPDATE Products 
SET price = 899.99, stock_quantity = 5 
WHERE product_id = 1;

-- Delete a product
DELETE FROM Products WHERE product_id = 1;

------------------------------------------------------------

-- Create a new order
INSERT INTO Orders (customer_id, total_amount)
VALUES (1, 1200.50);

-- Read all orders
SELECT * FROM Orders;

-- Update order details
UPDATE Orders 
SET total_amount = 1150.00 
WHERE order_id = 1;

-- Delete an order
DELETE FROM Orders WHERE order_id = 1;

------------------------------------------------------------

-- Create order details
INSERT INTO OrderDetails (order_id, product_id, quantity, price)
VALUES (1, 2, 3, 299.99);

-- Read all order details
SELECT * FROM OrderDetails;

-- Update order details
UPDATE OrderDetails 
SET quantity = 2, price = 249.99 
WHERE order_detail_id = 1;

-- Delete order details
DELETE FROM OrderDetails WHERE order_detail_id = 1;

------------------------------------------------------------

-- Create delivery details
INSERT INTO Delivery (order_id, delivery_date, delivery_status)
VALUES (1, '2025-03-28', 'Shipped');

-- Read all deliveries
SELECT * FROM Delivery;

-- Update delivery status
UPDATE Delivery 
SET delivery_status = 'Delivered', delivery_date = CURDATE() 
WHERE delivery_id = 1;

-- Delete a delivery record
DELETE FROM Delivery WHERE delivery_id = 1;

------------------------------------------------------------

-- Create a payment record
INSERT INTO Payment (order_id, payment_method, payment_status)
VALUES (1, 'Credit Card', 'Completed');

-- Read all payments
SELECT * FROM Payment;

-- Update payment status
UPDATE Payment 
SET payment_status = 'Completed' 
WHERE payment_id = 1;

-- Delete a payment record
DELETE FROM Payment WHERE payment_id = 1;
