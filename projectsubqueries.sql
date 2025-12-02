-- 1. Find Customers Who Have Placed Orders (IN with Subquery)
SELECT * 
FROM Customers 
WHERE customer_id IN (SELECT DISTINCT customer_id FROM Orders);

-- 2. Find Products That Have Never Been Ordered (NOT IN with Subquery)
SELECT * 
FROM Products 
WHERE product_id NOT IN (SELECT DISTINCT product_id FROM OrderDetails);

-- 3. Find Customers Who Have Placed the Maximum Order (ALL with Subquery)
SELECT customer_id 
FROM Orders 
WHERE total_amount >= ALL (SELECT total_amount FROM Orders);

-- 4. Find Orders with Total Amount Greater Than Any Customer's Order (ANY with Subquery)
SELECT order_id, total_amount 
FROM Orders 
WHERE total_amount > ANY (SELECT total_amount FROM Orders WHERE customer_id = 2);

-- 5. Find Customers Who Have Made Payments (EXISTS with Subquery)
SELECT * 
FROM Customers c
WHERE EXISTS (SELECT 1 FROM Orders o WHERE o.customer_id = c.customer_id);

-- 6. Find Orders Without Payment (NOT EXISTS with Subquery)
SELECT * 
FROM Orders o
WHERE NOT EXISTS (SELECT 1 FROM Payment p WHERE p.order_id = o.order_id);

-- 7. Find Products That Appear in Multiple Orders (COUNT in Subquery)
SELECT product_id, name 
FROM Products 
WHERE product_id IN (
    SELECT product_id 
    FROM OrderDetails 
    GROUP BY product_id 
    HAVING COUNT(order_id) > 1
);
