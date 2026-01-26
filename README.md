# E-Commerce Database Project

A **relational database system** built in **PostgreSQL** to simulate a realistic e-commerce platform.  
The project models **Users, Products, Orders, Payments, and Addresses** (fully normalized in 3NF), includes sample data, advanced queries, and an ER diagram.

---

## Key Features

- **Normalized Schema (3NF):**  
  Separate tables for City, State, and Country for clean and scalable address management.
- **Core Entities:** Users, Products, Orders, Order_Items, Payments, Addresses.
- **Sample Dataset:** 5 users, multiple products, orders, and payments to simulate real-world transactions.
- **SQL Query Bank:**  
  - Customer purchase history  
  - Top-selling products  
  - Monthly and category-wise sales reports  
  - Orders by city/state  
  - Pending payments
- **ER Diagram:** Visual representation of all entities and relationships.

---

## Repository Structure

    ecommerce-database-project/
    ├── README.md
    ├── schema/
    │ ├── create_tables.sql # PostgreSQL CREATE TABLE scripts
    │ └── sample_data.sql # Sample data inserts
    │ └── relationship_summary.md
    ├── queries/
    │ └── query_bank.md # SQL queries (basic → advanced analytics)
    ├── diagrams/
     └── er_diagram.md # ER diagram

---

## How to Run

1. Create a PostgreSQL database using **pgAdmin** or **psql**.  
2. Execute `schema/create_tables.sql` to create all tables.  
3. Load `schema/sample_data.sql` to populate sample data.  
4. Explore queries in `queries/query_bank.md` to analyze data.  
5. Refer to `diagrams/er_diagram.md` for schema visualization.

---

## Learning Outcomes

- Design **normalized relational databases** suitable for real-world e-commerce systems.  
- Write **complex SQL queries** for analytics and reporting.  
- Build **scalable, professional database projects** for portfolio or resume.  
- Understand **foreign keys, relationships, and data integrity** in PostgreSQL.

---

## Tech Stack

- **Database:** PostgreSQL 14+  
- **Tools:** pgAdmin, SQL  
- **Skills Demonstrated:** Database Design, 3NF Normalization, SQL Queries, Analytics, ER Modeling