# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-06-03

### Added
- **Multi-Vendor Support**: Added `Sellers` table and associated foreign keys to allow multiple vendors to list products.
- **Hierarchical Categories**: Added self-referencing `parent_id` on `Categories` to support nested product directories.
- **Persistent Carts & Wishlists**: Persistence for active checkouts with `Carts`, `Cart_Items`, `Wishlists`, and `Wishlist_Items`.
- **Review System**: Rating and comment verification in `Reviews` with unique customer constraints.
- **Coupon System**: Coupon code checks and validation routines inside `Coupons` table.
- **Stock Movement Log**: Stock changes ledger tracking through `Stock_Movements` table.
- **Stored Procedures**:
  - `place_order()` to check out cart items and apply coupon discounts.
  - `process_refund()` to restore stocks and mark orders/payments refunded.
- **Triggers**:
  - `trigger_decrement_stock` to reduce stock levels on item checkout.
  - `trigger_flag_order_paid` to update status logs upon transaction confirmation.
- **Indexes**: Applied B-tree indexes to all critical foreign key paths and search filters.
- **Recursive Views**:
  - `active_orders_view` for live warehouse logistics tracking.
  - `revenue_by_category_view` using recursive CTEs to aggregate subcategory revenues.
- **Docker Compose Setup**: Integrated PostgreSQL 15 configuration with auto-seeding schema and transactional logs.
- **Data Generator Script**: Python-based mock database generator `scripts/generate_sample_data.py`.
- **Advanced SQL Query Bank**: Window functions (`RANK`, `LAG`), CTE hierarchies, and EXPLAIN ANALYZE comparison walkthrough.

### Changed
- Migrated flat text category mappings to normalized tables.
- Upgraded sample data from 5 users to 60 users and 115 chronological transactions.
- Replaced text-based ER diagram links with an interactive schema image.
