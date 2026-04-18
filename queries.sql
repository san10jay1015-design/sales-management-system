-- Basic Queries

-- 1. Retrieve all records from the customer_sales table.
SELECT * FROM customer_sales;

-- 2. Retrieve all records from the branches table.
SELECT * FROM branches;

-- 3. Retrieve all records from the payment_splits table.
SELECT * FROM payment_splits;

-- 4. Retrieve all sales belonging to the Chennai branch.
SELECT * FROM cs.* FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id WHERE b.branch_name = 'Chennai';

-- Aggregation Queries

-- 5. Calculate the total gross sales across all branches.
SELECT SUM(gross_sales) AS total_gross_sales FROM customer_sales;

-- 6. Calculate the total received amount across all sales.
SELECT SUM(received_amount) AS total_received_amount FROM customer_sales;

-- 7. Calculate the total pending amount across all sales.
SELECT SUM(pending_amount) AS total_pending_amount FROM customer_sales;

-- 8. Count the total number of sales per branch.
SELECT b.branch_name, COUNT(cs.sale_id) AS total_sales FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id GROUP BY b.branch_name;

-- Join-Based Queries

-- 9. Retrieve sales details along with the branch name.
SELECT cs.*, b.branch_name FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id;

-- 10. Retrieve sales details along with total payment received (using payment_splits).
SELECT cs.sale_id, cs.name, SUM(ps.amount_paid) AS total_received FROM customer_sales cs JOIN payment_splits ps ON cs.sale_id = ps.sale_id GROUP BY cs.sale_id, cs.name;

-- 11. Show branch-wise total gross sales (using JOIN & GROUP BY).
SELECT b.branch_name, SUM(cs.gross_sales) AS total_gross_sales FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id GROUP BY b.branch_name;

-- 12. Display sales along with payment method used.
SELECT cs.sale_id, cs.name, ps.payment_method FROM customer_sales cs JOIN payment_splits ps ON cs.sale_id = ps.sale_id;

-- Financial Tracking Queries

-- 13.  Find sales where the pending amount is greater than 5000.
SELECT * FROM customer_sales WHERE pending_amount > 5000;

-- 14.  Retrieve top 3 highest gross sales.
SELECT * FROM customer_sales ORDER BY gross_sales DESC LIMIT 3;

-- 15.  Retrieve monthly sales summary (group by month & year).
SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(gross_sales) AS total_sales FROM customer_sales GROUP BY YEAR(date), MONTH(date);

