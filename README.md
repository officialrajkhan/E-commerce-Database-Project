# E-Commerce Database Project (Production Grade)

A robust, production-grade **relational database system** built using **PostgreSQL** simulating a multi-vendor e-commerce platform.

This database architecture is fully normalized to **3NF**, populated with a realistic chronological dataset, optimized with high-performance indexes, and features advanced database objects such as **Stored Procedures**, **Triggers**, and **Recursive CTE Views**.

---

## 🌟 Key Features

- **Docker-Compose Ready**: Spin up the entire database with tables, indexes, triggers, views, stored procedures, and sample seed data loaded automatically in 30 seconds.
- **Normalized Address Hierarchy (3NF)**: Separate, clean mappings for `Country` → `State` → `City` → `Address` to prevent data redundancy.
- **Multi-Vendor Support**: Product listings are associated with multiple `Sellers`.
- **Hierarchical Categories**: Parent-child relationship mappings (e.g. `Electronics` > `Computers` > `Laptops`) for flexible catalog structures.
- **Customer Session State**: Built-in support for live persistent `Carts` and `Wishlists`.
- **Advanced Stored Procedures**:
  - `place_order()`: Handles cart checkout, applies coupon discount checking, logs shipping details, and clears the cart atomically.
  - `process_refund()`: Updates order/payment state and returns items to stock with ledger logging.
- **Automated Triggers**:
  - `trigger_decrement_stock`: Automatically decreases product inventory on checkout and writes to stock ledgers.
  - `trigger_flag_order_paid`: Dynamically updates order states and shipping logs upon receipt of payment.
- **Database Indexing**: Speeds up foreign key lookups and name/price search columns.
- **Rich Sample Dataset**: 60 realistic users, 10 sellers, 35 products, 10 coupons, and **115 chronological orders** spanning 6 months with real payments, reviews, and tracking information.

---

## 📂 Repository Structure

```text
ecommerce-database-project/
├── docker-compose.yml       # Spin up database and load schema + seeds in one command
├── README.md                # Documentation and setup instructions
├── CHANGELOG.md             # Record of updates using Conventional Commits
├── schema/
│   ├── create_tables.sql    # PostgreSQL schema, indexes, triggers, procedures, views
│   └── sample_data.sql      # Seed inserts (60 users, 10 sellers, 115 orders, etc.)
├── queries/
│   └── query_bank.md        # Basic, intermediate, and advanced queries (CTEs, Windows)
├── diagrams/
│   ├── er_diagram.md        # ER diagram details
│   └── er_diagram.png       # Visual ER diagram image
└── scripts/
    └── generate_sample_data.py # Python script for seeding sample data
```

---

## 🚀 Quick Start (Run in 30 seconds)

### Method A: Docker Compose (Recommended)
Make sure you have [Docker](https://www.docker.com/) installed, then run:

```bash
docker compose up -d
```

Docker will download PostgreSQL 15, initialize the container, create the schema, and load the 110+ sample records.

To connect to your database using `psql` or any database viewer (like pgAdmin or DBeaver):
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `ecommerce_db`
- **User**: `postgres`
- **Password**: `postgres`

### Method B: Manual Execution
If you do not use Docker, execute the scripts in the following order using psql or pgAdmin:
1. Run `schema/create_tables.sql` to initialize tables and objects.
2. Run `schema/sample_data.sql` to seed the database.

---

## 📊 Analytical Query Bank

Inside [queries/query_bank.md](queries/query_bank.md), you will find pre-built queries demonstrating:
- Sales ranking within categories using `DENSE_RANK()`.
- Month-over-Month (MoM) revenue trends using `LAG()`.
- Category paths using recursive CTEs.
- `EXPLAIN ANALYZE` benchmarks validating indexing gains.

---

## 🛠️ Testing Stored Procedures & Triggers

Connect to your database client and run the following commands to test the automated workflows.

### 1. Test Stored Procedure: `place_order()`
Add a product to user 5's cart, and call the checkout procedure:

```sql
-- Step 1: Add a product to User 5's cart
INSERT INTO Cart_Items (cart_id, product_id, quantity) 
VALUES (5, 1, 1); -- iPhone 15 Pro (ID: 1)

-- Step 2: Run the checkout stored procedure
CALL place_order(
    p_user_id := 5,
    p_shipping_address_id := 9,
    p_shipping_method := 'Express',
    p_coupon_code := 'WELCOME10'
);

-- Step 3: Check that the order was created and the cart cleared
SELECT * FROM Orders WHERE user_id = 5 ORDER BY order_id DESC LIMIT 1;
SELECT * FROM Cart_Items WHERE cart_id = 5;
```

### 2. Test Trigger: Stock Decrementor
Check product stock level before and after an order item is created:

```sql
-- Check stock level of product 1
SELECT stock_qty FROM Products WHERE product_id = 1;

-- Creating an order item will automatically fire the trigger
INSERT INTO Orders (order_id, user_id, total_amount) VALUES (999, 1, 109999.00);
INSERT INTO Order_Items (order_id, product_id, quantity, price_at_purchase) 
VALUES (999, 1, 2, 109999.00);

-- Verify stock level was reduced by 2
SELECT stock_qty FROM Products WHERE product_id = 1;
-- Verify stock log entry
SELECT * FROM Stock_Movements ORDER BY movement_id DESC LIMIT 1;
```