## Relationships Summary

The upgraded e-commerce platform features the following data connections:

- **Customer Purchasing Flow**:
  - `Users` (1) → (M) `Orders` (1) → (M) `Order_Items` (M) ← (1) `Products`

- **Sellers & Categorization**:
  - `Sellers` (1) → (M) `Products`
  - `Categories` (1) [Self-Referencing Parent] → (M) `Products`
  - `Products` (M) ↔ (M) `Tags` (via `Product_Tags` bridge table)

- **Sessions & Carts**:
  - `Users` (1) ↔ (1) `Carts` (1) → (M) `Cart_Items` (M) ← (1) `Products`
  - `Users` (1) ↔ (1) `Wishlists` (1) → (M) `Wishlist_Items` (M) ← (1) `Products`

- **Transactions & Logistics**:
  - `Orders` (1) → (M) `Payments`
  - `Coupons` (1) → (M) `Orders`
  - `Orders` (1) ↔ (1) `Shipping_Details` (1) → (1) `Address` (M) → (1) `City` (M) → (1) `State` (M) → (1) `Country`

- **Auditing & Engagement**:
  - `Users` (1) → (M) `Reviews` (M) ← (1) `Products`
  - `Products` (1) → (M) `Stock_Movements`
