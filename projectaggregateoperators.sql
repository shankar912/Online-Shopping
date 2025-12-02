-- 1. Total Orders Per Customer
SELECT customer_id, COUNT(order_id) AS total_orders
FROM Orders
GROUP BY customer_id;

-- 2. Total Revenue Per Product
SELECT p.name AS product_name, SUM(od.quantity * od.price) AS total_revenue
FROM OrderDetails od
JOIN Products p ON od.product_id = p.product_id
GROUP BY p.name;

-- 3. Customers Who Spent More Than $500
SELECT o.customer_id, SUM(o.total_amount) AS total_spent
FROM Orders o
GROUP BY o.customer_id
HAVING SUM(o.total_amount) > 500;

-- 4. Average Order Value
SELECT AVG(total_amount) AS avg_order_value
FROM Orders;

-- 5. Total Orders Per Month
SELECT DATE_FORMAT(order_date, '%Y-%m') AS order_month, COUNT(order_id) AS total_orders
FROM Orders
GROUP BY order_month;

-- 6. Most Sold Product
SELECT p.name AS product_name, SUM(od.quantity) AS total_sold
FROM OrderDetails od
JOIN Products p ON od.product_id = p.product_id
GROUP BY p.name
ORDER BY total_sold DESC
LIMIT 1;

-- 7. Number of Orders Per Payment Method
SELECT payment_method, COUNT(payment_id) AS total_payments
FROM Payment
GROUP BY payment_method;

-- 8. Total Orders Delivered Successfully
SELECT delivery_status, COUNT(delivery_id) AS total_delivered
FROM Delivery
GROUP BY delivery_status
HAVING delivery_status = 'Delivered';

-- 9. Minimum, Maximum, and Average Product Price
SELECT MIN(price) AS min_price, MAX(price) AS max_price, AVG(price) AS avg_price
FROM Products;

-- 10. Customers with More Than 2 Orders
SELECT customer_id, COUNT(order_id) AS order_count
FROM Orders
GROUP BY customer_id
HAVING COUNT(order_id) > 2;
