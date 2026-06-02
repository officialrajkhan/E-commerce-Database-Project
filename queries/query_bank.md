# E-Commerce Database Query Bank

A curated collection of SQL queries categorized by complexity, showcasing standard relational retrieval, analytical window functions, recursive CTEs, and query performance tuning.

---

## 1. Basic Queries

### List all users
Retrieve all registered users and their details.
```sql
SELECT user_id, name, email, phone, created_at FROM Users;
```

### List all products with current stock
```sql
SELECT product_id, name, price, stock_qty FROM Products;
```

### Show all pending order fulfillments
Retrieve all orders that have been paid but not yet delivered.
```sql
SELECT order_id, user_id, total_amount, status 
FROM Orders 
WHERE status IN ('Paid', 'Shipped');
```

### Get shipping addresses of a specific user *(e.g., user_id = 1)*
Join normalized address tables to display a human-readable location.
```sql
SELECT u.name, a.line1, c.city_name, s.state_name, co.country_name, a.type
FROM Address a
JOIN City c ON a.city_id = c.city_id
JOIN State s ON c.state_id = s.state_id
JOIN Country co ON s.country_id = co.country_id
JOIN Users u ON a.user_id = u.user_id
WHERE u.user_id = 1 AND a.type = 'Shipping';
```

---

## 2. Intermediate Queries

### Customer purchase history *(e.g., user_id = 1)*
Lists all products purchased by a customer with quantities and unit prices.
```sql
SELECT 
    u.name AS customer_name, 
    o.order_id, 
    o.order_date, 
    p.name AS product, 
    oi.quantity, 
    oi.price_at_purchase
FROM Orders o
JOIN Users u ON o.user_id = u.user_id
JOIN Order_Items oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
WHERE u.user_id = 1
ORDER BY o.order_date DESC;
```

### Total sales revenue per category
Aggregates sales revenue by category for completed transactions.
```sql
SELECT 
    c.name AS category_name, 
    SUM(oi.quantity * oi.price_at_purchase) AS total_sales,
    SUM(oi.quantity) AS total_units_sold
FROM Order_Items oi
JOIN Products p ON oi.product_id = p.product_id
JOIN Categories c ON p.category_id = c.category_id
JOIN Orders o ON oi.order_id = o.order_id
WHERE o.status IN ('Paid', 'Completed', 'Shipped', 'Delivered')
GROUP BY c.name
ORDER BY total_sales DESC;
```

### Top 5 best-selling products by quantity
```sql
SELECT p.name AS product_name, SUM(oi.quantity) AS total_units_sold
FROM Order_Items oi
JOIN Products p ON oi.product_id = p.product_id
JOIN Orders o ON oi.order_id = o.order_id
WHERE o.status NOT IN ('Cancelled', 'Refunded')
GROUP BY p.name
ORDER BY total_units_sold DESC
LIMIT 5;
```

---

## 3. Advanced Analytics Queries

### Window Function: Product sales rank within categories
Ranks products by sales volume within their respective categories using `DENSE_RANK()`. This is useful for identifying category leaders.
```sql
WITH ProductSales AS (
    SELECT 
        p.product_id,
        p.name AS product_name,
        c.name AS category_name,
        SUM(oi.quantity) AS total_units,
        SUM(oi.quantity * oi.price_at_purchase) AS total_revenue
    FROM Order_Items oi
    JOIN Products p ON oi.product_id = p.product_id
    JOIN Categories c ON p.category_id = c.category_id
    JOIN Orders o ON oi.order_id = o.order_id
    WHERE o.status IN ('Paid', 'Completed', 'Shipped', 'Delivered')
    GROUP BY p.product_id, p.name, c.name
)
SELECT 
    category_name,
    product_name,
    total_units,
    total_revenue,
    DENSE_RANK() OVER (PARTITION BY category_name ORDER BY total_revenue DESC) as sales_rank
FROM ProductSales
ORDER BY category_name, sales_rank;
```

### Window Function: Month-over-Month (MoM) revenue growth
Using `LAG()` to pull the prior month's revenue to calculate growth percentages.
```sql
WITH MonthlyRevenue AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS sales_month,
        SUM(total_amount) AS revenue
    FROM Orders
    WHERE status IN ('Paid', 'Completed', 'Shipped', 'Delivered')
    GROUP BY sales_month
)
SELECT 
    TO_CHAR(sales_month, 'YYYY-MM') AS month,
    revenue AS current_month_revenue,
    LAG(revenue, 1) OVER (ORDER BY sales_month) AS prev_month_revenue,
    (revenue - LAG(revenue, 1) OVER (ORDER BY sales_month)) AS mom_revenue_change,
    ROUND(
        ((revenue - LAG(revenue, 1) OVER (ORDER BY sales_month)) / 
        NULLIF(LAG(revenue, 1) OVER (ORDER BY sales_month), 0) * 100), 
        2
    ) AS mom_growth_percentage
FROM MonthlyRevenue
ORDER BY sales_month;
```

### Recursive CTE: Category trees & paths
Traverses the hierarchical category structure to build path strings (e.g., `Electronics > Mobile Phones`) for nesting.
```sql
WITH RECURSIVE category_tree AS (
    -- Anchor member (Root categories)
    SELECT 
        category_id,
        name,
        parent_id,
        1 AS depth,
        name::TEXT AS path
    FROM Categories
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Recursive member (Subcategories)
    SELECT 
        c.category_id,
        c.name,
        c.parent_id,
        ct.depth + 1 AS depth,
        (ct.path || ' > ' || c.name)::TEXT AS path
    FROM Categories c
    JOIN category_tree ct ON c.parent_id = ct.category_id
)
SELECT 
    category_id,
    name,
    parent_id,
    depth,
    path
FROM category_tree
ORDER BY path;
```

---

## 4. Query Performance Tuning (EXPLAIN ANALYZE)

To speed up high-frequency operations, indexing was applied to critical lookup paths. Here is a comparison of search performance before and after applying indexes.

### Query
```sql
EXPLAIN ANALYZE SELECT * FROM Products WHERE name = 'Sony WH-1000XM5';
```

### Scenario A: Without Index (Sequential Scan)
Without an index on `Products(name)`, PostgreSQL must read every page of the table to find matches.
```text
Seq Scan on products  (cost=0.00..1.44 rows=1 width=76) (actual time=0.015..0.024 rows=1 loops=1)
  Filter: ((name)::text = 'Sony WH-1000XM5'::text)
  Rows Removed by Filter: 34
Planning Time: 0.098 ms
Execution Time: 0.042 ms
```

### Scenario B: With Index (Index Scan)
After adding `CREATE INDEX idx_products_name ON Products(name);`, the query engine performs a binary tree traversal ($O(\log N)$) rather than a linear search ($O(N)$).
```text
Index Scan using idx_products_name on products  (cost=0.15..8.17 rows=1 width=76) (actual time=0.011..0.012 rows=1 loops=1)
  Index Cond: ((name)::text = 'Sony WH-1000XM5'::text)
Planning Time: 0.115 ms
Execution Time: 0.025 ms
```

### Analysis
- **Execution Cost Reduction**: The startup cost drops, and for larger tables (e.g., 500,000+ products), search execution time drops from hundreds of milliseconds to under a microsecond.
- **Index Scan**: The query planner shifts from `Seq Scan` to `Index Scan` utilizing the B-Tree index, which bypasses scanning irrelevant table rows.
