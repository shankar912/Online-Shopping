-- Creating Indexes for NewOnlineShoppingDB

-- 1. Customers Table: Index on email for faster search and uniqueness
CREATE INDEX idx_customers_email ON Customers(email);

-- 2. Products Table: Index on product name for faster search
CREATE INDEX idx_products_name ON Products(name);

-- 3. Orders Table: Index on customer_id to speed up JOIN with Customers
CREATE INDEX idx_orders_customer_id ON Orders(customer_id);

-- 4. OrderDetails Table: Index on order_id to speed up JOIN with Orders
CREATE INDEX idx_orderdetails_order_id ON OrderDetails(order_id);

-- 5. OrderDetails Table: Index on product_id to speed up JOIN with Products
CREATE INDEX idx_orderdetails_product_id ON OrderDetails(product_id);

-- 6. Delivery Table: Index on order_id to speed up JOIN with Orders
CREATE INDEX idx_delivery_order_id ON Delivery(order_id);

-- 7. Payment Table: Index on order_id to speed up JOIN with Orders
CREATE INDEX idx_payment_order_id ON Payment(order_id);
