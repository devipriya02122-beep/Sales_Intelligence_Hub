-- =========================================================
-- 📌 Basic Queries
-- =========================================================
-- Retrieve all records from customer_sales
SELECT * FROM customer_sales;

-- Retrieve all records from branches
SELECT * FROM branches;

-- Retrieve all records from payment_splits
SELECT * FROM payment_splits;

-- Display all sales with status = 'Open'
SELECT * FROM customer_sales WHERE status = 'Open';

-- Retrieve all sales belonging to the Chennai branch
SELECT * FROM customer_sales
WHERE branch_id = (SELECT branch_id FROM branches WHERE branch_name = 'Chennai');

-- =========================================================
-- 📊 Aggregation Queries
-- =========================================================
-- Calculate total gross sales across all branches
SELECT SUM(gross_sales) AS total_gross_sales FROM customer_sales;

-- Calculate total received amount across all sales
SELECT SUM(received_amount) AS total_received FROM customer_sales;

-- Calculate total pending amount across all sales
SELECT SUM(pending_amount) AS total_pending FROM customer_sales;

-- Count total number of sales per branch
SELECT branch_id, COUNT(*) AS total_sales
FROM customer_sales
GROUP BY branch_id;

-- Find average gross sales amount
SELECT AVG(gross_sales) AS avg_gross_sales FROM customer_sales;

-- =========================================================
-- 🔗 Join-Based Queries
-- =========================================================
-- Retrieve sales details along with branch name
SELECT cs.sale_id, cs.name, cs.product_name, cs.gross_sales, b.branch_name
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id;

-- Retrieve sales details along with total payment received
SELECT cs.sale_id, cs.name, cs.gross_sales, SUM(ps.amount_paid) AS total_payment
FROM customer_sales cs
JOIN payment_splits ps ON cs.sale_id = ps.sale_id
GROUP BY cs.sale_id, cs.name, cs.gross_sales;

-- Show branch-wise total gross sales
SELECT b.branch_name, SUM(cs.gross_sales) AS total_gross_sales
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
GROUP BY b.branch_name;

-- Display sales along with payment method used
SELECT cs.sale_id, cs.name, cs.gross_sales, ps.payment_method, ps.amount_paid
FROM customer_sales cs
JOIN payment_splits ps ON cs.sale_id = ps.sale_id;

-- Retrieve sales along with branch admin name
SELECT cs.sale_id, cs.name, cs.gross_sales, b.branch_admin_name
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id;

-- =========================================================
-- 💰 Financial Tracking Queries
-- =========================================================
-- Find sales where pending amount > 5000
SELECT * FROM customer_sales WHERE pending_amount > 5000;

-- Retrieve top 3 highest gross sales
SELECT sale_id, name, gross_sales
FROM customer_sales
ORDER BY gross_sales DESC
LIMIT 3;

-- Find branch with highest total gross sales
SELECT b.branch_name, SUM(cs.gross_sales) AS total_gross_sales
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
GROUP BY b.branch_name
ORDER BY total_gross_sales DESC
LIMIT 1;

-- Retrieve monthly sales summary
SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(gross_sales) AS monthly_sales
FROM customer_sales
GROUP BY YEAR(date), MONTH(date)
ORDER BY year, month;

-- Calculate payment method-wise total collection
SELECT payment_method, SUM(amount_paid) AS total_collection
FROM payment_splits
GROUP BY payment_method;
