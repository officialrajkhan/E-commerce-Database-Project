-- E-Commerce Platform Database Schema
-- Standardised for PostgreSQL

-- Drop existing objects in reverse dependency order
DROP VIEW IF EXISTS active_orders_view CASCADE;
DROP VIEW IF EXISTS revenue_by_category_view CASCADE;
DROP TRIGGER IF EXISTS trigger_decrement_stock ON Order_Items CASCADE;
DROP FUNCTION IF EXISTS decrement_stock_func CASCADE;
DROP TRIGGER IF EXISTS trigger_flag_order_paid ON Payments CASCADE;
DROP FUNCTION IF EXISTS flag_order_paid_func CASCADE;
DROP PROCEDURE IF EXISTS place_order CASCADE;
DROP PROCEDURE IF EXISTS process_refund CASCADE;

DROP TABLE IF EXISTS Stock_Movements CASCADE;
DROP TABLE IF EXISTS Reviews CASCADE;
DROP TABLE IF EXISTS Shipping_Details CASCADE;
DROP TABLE IF EXISTS Payments CASCADE;
DROP TABLE IF EXISTS Order_Items CASCADE;
DROP TABLE IF EXISTS Orders CASCADE;
DROP TABLE IF EXISTS Wishlist_Items CASCADE;
DROP TABLE IF EXISTS Wishlists CASCADE;
DROP TABLE IF EXISTS Cart_Items CASCADE;
DROP TABLE IF EXISTS Carts CASCADE;
DROP TABLE IF EXISTS Product_Tags CASCADE;
DROP TABLE IF EXISTS Tags CASCADE;
DROP TABLE IF EXISTS Products CASCADE;
DROP TABLE IF EXISTS Categories CASCADE;
DROP TABLE IF EXISTS Sellers CASCADE;
DROP TABLE IF EXISTS Address CASCADE;
DROP TABLE IF EXISTS City CASCADE;
DROP TABLE IF EXISTS State CASCADE;
DROP TABLE IF EXISTS Country CASCADE;
DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS Coupons CASCADE;

-- =========================================================================
-- 1. CORE USER & SELLER TABLES
-- =========================================================================

-- Users
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Sellers (Multi-vendor support)
CREATE TABLE Sellers (
    seller_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    business_name VARCHAR(150),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================================
-- 2. ADDRESS HIERARCHY TABLES (3NF normalization)
-- =========================================================================

-- Country
CREATE TABLE Country (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) UNIQUE NOT NULL
);

-- State
CREATE TABLE State (
    state_id SERIAL PRIMARY KEY,
    state_name VARCHAR(100) NOT NULL,
    country_id INT REFERENCES Country(country_id) ON DELETE CASCADE
);

-- City
CREATE TABLE City (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    state_id INT REFERENCES State(state_id) ON DELETE CASCADE
);

-- Address
CREATE TABLE Address (
    address_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    line1 VARCHAR(255) NOT NULL,
    zipcode VARCHAR(20),
    city_id INT REFERENCES City(city_id) ON DELETE RESTRICT,
    type VARCHAR(20) CHECK (type IN ('Billing','Shipping')) NOT NULL
);

-- =========================================================================
-- 3. PRODUCT & CATEGORISATION TABLES
-- =========================================================================

-- Categories (Hierarchical category tree)
CREATE TABLE Categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    parent_id INT REFERENCES Categories(category_id) ON DELETE SET NULL
);

-- Products
CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    seller_id INT REFERENCES Sellers(seller_id) ON DELETE SET NULL,
    category_id INT REFERENCES Categories(category_id) ON DELETE SET NULL,
    name VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0.00),
    stock_qty INT DEFAULT 0 CHECK (stock_qty >= 0),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Tags
CREATE TABLE Tags (
    tag_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Product Tags (Many-to-Many join table)
CREATE TABLE Product_Tags (
    product_id INT REFERENCES Products(product_id) ON DELETE CASCADE,
    tag_id INT REFERENCES Tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, tag_id)
);

-- =========================================================================
-- 4. CART & WISHLIST TABLES
-- =========================================================================

-- Carts
CREATE TABLE Carts (
    cart_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES Users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Cart Items
CREATE TABLE Cart_Items (
    cart_item_id SERIAL PRIMARY KEY,
    cart_id INT REFERENCES Carts(cart_id) ON DELETE CASCADE,
    product_id INT REFERENCES Products(product_id) ON DELETE CASCADE,
    quantity INT NOT NULL CHECK (quantity > 0),
    UNIQUE(cart_id, product_id)
);

-- Wishlists
CREATE TABLE Wishlists (
    wishlist_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES Users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Wishlist Items
CREATE TABLE Wishlist_Items (
    wishlist_item_id SERIAL PRIMARY KEY,
    wishlist_id INT REFERENCES Wishlists(wishlist_id) ON DELETE CASCADE,
    product_id INT REFERENCES Products(product_id) ON DELETE CASCADE,
    UNIQUE(wishlist_id, product_id)
);

-- =========================================================================
-- 5. COUPONS, ORDERS & TRANSACTION TABLES
-- =========================================================================

-- Coupons
CREATE TABLE Coupons (
    coupon_id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    discount_type VARCHAR(20) CHECK (discount_type IN ('percentage', 'fixed')) NOT NULL,
    discount_value DECIMAL(10,2) NOT NULL CHECK (discount_value > 0.00),
    min_order_amount DECIMAL(10,2) DEFAULT 0.00 CHECK (min_order_amount >= 0.00),
    active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMPTZ
);

-- Orders
CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE RESTRICT,
    coupon_id INT REFERENCES Coupons(coupon_id) ON DELETE SET NULL,
    order_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Paid', 'Shipped', 'Delivered', 'Cancelled', 'Refunded')),
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0.00)
);

-- Order Items
CREATE TABLE Order_Items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES Orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES Products(product_id) ON DELETE RESTRICT,
    quantity INT NOT NULL CHECK (quantity > 0),
    price_at_purchase DECIMAL(10,2) NOT NULL CHECK (price_at_purchase >= 0.00)
);

-- Payments
CREATE TABLE Payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES Orders(order_id) ON DELETE CASCADE,
    method VARCHAR(20) CHECK (method IN ('UPI', 'Card', 'COD')),
    status VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Paid', 'Refunded', 'Failed')),
    amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0.00),
    transaction_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================================
-- 6. SHIPPING & LOGISTICS
-- =========================================================================

-- Shipping Details (Order delivery tracking)
CREATE TABLE Shipping_Details (
    shipping_id SERIAL PRIMARY KEY,
    order_id INT UNIQUE REFERENCES Orders(order_id) ON DELETE CASCADE,
    address_id INT REFERENCES Address(address_id) ON DELETE RESTRICT,
    shipping_method VARCHAR(50) NOT NULL,
    tracking_number VARCHAR(100) UNIQUE,
    status VARCHAR(50) DEFAULT 'Preparing' CHECK (status IN ('Preparing', 'Shipped', 'In Transit', 'Out for Delivery', 'Delivered', 'Failed')),
    estimated_delivery TIMESTAMPTZ,
    shipped_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ
);

-- =========================================================================
-- 7. REVIEWS & RATINGS
-- =========================================================================

-- Reviews
CREATE TABLE Reviews (
    review_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    product_id INT REFERENCES Products(product_id) ON DELETE CASCADE,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, product_id)
);

-- =========================================================================
-- 8. INVENTORY / STOCK LOGGING
-- =========================================================================

-- Stock Movements (Tracking changes in inventory)
CREATE TABLE Stock_Movements (
    movement_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES Products(product_id) ON DELETE CASCADE,
    quantity_changed INT NOT NULL, -- Negative for sales, positive for restocks
    reason VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================================
-- 9. INDEXES
-- =========================================================================

-- Foreign Key Indexes for optimization during joins
CREATE INDEX idx_orders_user_id ON Orders(user_id);
CREATE INDEX idx_order_items_order_id ON Order_Items(order_id);
CREATE INDEX idx_order_items_product_id ON Order_Items(product_id);
CREATE INDEX idx_products_category_id ON Products(category_id);
CREATE INDEX idx_products_seller_id ON Products(seller_id);
CREATE INDEX idx_address_user_id ON Address(user_id);
CREATE INDEX idx_payments_order_id ON Payments(order_id);
CREATE INDEX idx_shipping_details_order_id ON Shipping_Details(order_id);
CREATE INDEX idx_cart_items_cart_id ON Cart_Items(cart_id);

-- Performance-critical search indexes
CREATE INDEX idx_products_name ON Products(name);
CREATE INDEX idx_products_price ON Products(price);
CREATE INDEX idx_reviews_product_id ON Reviews(product_id);


-- =========================================================================
-- 10. TRIGGERS
-- =========================================================================

-- Trigger A: Automatically decrement stock and log movement when Order Item is added
CREATE OR REPLACE FUNCTION decrement_stock_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if there is enough stock
    IF (SELECT stock_qty FROM Products WHERE product_id = NEW.product_id) < NEW.quantity THEN
        RAISE EXCEPTION 'Insufficient stock for product ID %', NEW.product_id;
    END IF;

    -- Decrement stock in Products
    UPDATE Products
    SET stock_qty = stock_qty - NEW.quantity
    WHERE product_id = NEW.product_id;

    -- Log stock movement
    INSERT INTO Stock_Movements (product_id, quantity_changed, reason)
    VALUES (NEW.product_id, -NEW.quantity, 'Order Placed - Item ID: ' || NEW.order_item_id);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_decrement_stock
BEFORE INSERT ON Order_Items
FOR EACH ROW
EXECUTE FUNCTION decrement_stock_func();


-- Trigger B: Automatically mark Order as 'Paid' when Payment status is set to 'Paid'
CREATE OR REPLACE FUNCTION flag_order_paid_func()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'Paid' AND (OLD IS NULL OR OLD.status <> 'Paid') THEN
        UPDATE Orders
        SET status = 'Paid'
        WHERE order_id = NEW.order_id;
        
        -- Update shipping detail status
        UPDATE Shipping_Details
        SET status = 'Shipped', shipped_at = CURRENT_TIMESTAMP
        WHERE order_id = NEW.order_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_flag_order_paid
AFTER INSERT OR UPDATE ON Payments
FOR EACH ROW
EXECUTE FUNCTION flag_order_paid_func();


-- =========================================================================
-- 11. VIEWS
-- =========================================================================

-- View A: Active Orders for warehouse & shipping fulfillment
CREATE OR REPLACE VIEW active_orders_view AS
SELECT 
    o.order_id,
    o.order_date,
    o.status AS order_status,
    o.total_amount,
    u.user_id,
    u.name AS customer_name,
    u.email AS customer_email,
    p.payment_id,
    p.status AS payment_status,
    p.method AS payment_method,
    sd.shipping_id,
    sd.status AS shipping_status,
    sd.tracking_number,
    sd.estimated_delivery
FROM Orders o
JOIN Users u ON o.user_id = u.user_id
LEFT JOIN Payments p ON o.order_id = p.order_id
LEFT JOIN Shipping_Details sd ON o.order_id = sd.order_id
WHERE o.status IN ('Pending', 'Paid', 'Shipped');


-- View B: Revenue by category including nested child nodes (Recursive CTE view)
CREATE OR REPLACE VIEW revenue_by_category_view AS
WITH RECURSIVE category_path AS (
    -- Anchor member
    SELECT 
        category_id,
        name,
        parent_id,
        name::TEXT AS path
    FROM Categories
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Recursive member
    SELECT 
        c.category_id,
        c.name,
        c.parent_id,
        (cp.path || ' > ' || c.name)::TEXT
    FROM Categories c
    JOIN category_path cp ON c.parent_id = cp.category_id
)
SELECT 
    cp.category_id,
    cp.path AS category_path,
    COALESCE(SUM(oi.quantity * oi.price_at_purchase), 0) AS total_revenue,
    COALESCE(SUM(oi.quantity), 0) AS total_units_sold
FROM category_path cp
LEFT JOIN Products p ON p.category_id = cp.category_id
LEFT JOIN Order_Items oi ON oi.product_id = p.product_id
LEFT JOIN Orders o ON oi.order_id = o.order_id AND o.status IN ('Paid', 'Completed', 'Shipped', 'Delivered')
GROUP BY cp.category_id, cp.path;


-- =========================================================================
-- 12. STORED PROCEDURES
-- =========================================================================

-- Procedure A: place_order()
CREATE OR REPLACE PROCEDURE place_order(
    p_user_id INT,
    p_shipping_address_id INT,
    p_shipping_method VARCHAR(50),
    p_coupon_code VARCHAR(50),
    INOUT p_order_id INT DEFAULT NULL
) AS $$
DECLARE
    v_cart_id INT;
    v_total DECIMAL(10,2) := 0;
    v_coupon_id INT := NULL;
    v_discount DECIMAL(10,2) := 0;
    v_item RECORD;
BEGIN
    -- Find active cart
    SELECT cart_id INTO v_cart_id FROM Carts WHERE user_id = p_user_id;
    IF v_cart_id IS NULL THEN
        RAISE EXCEPTION 'No active cart found for user ID %', p_user_id;
    END IF;

    -- Check if cart is empty
    IF NOT EXISTS (SELECT 1 FROM Cart_Items WHERE cart_id = v_cart_id) THEN
        RAISE EXCEPTION 'Cart is empty for user ID %', p_user_id;
    END IF;

    -- Calculate initial subtotal
    SELECT SUM(p.price * ci.quantity) INTO v_total
    FROM Cart_Items ci
    JOIN Products p ON ci.product_id = p.product_id
    WHERE ci.cart_id = v_cart_id;

    -- Apply coupon if provided
    IF p_coupon_code IS NOT NULL AND p_coupon_code <> '' THEN
        SELECT coupon_id, 
               CASE 
                   WHEN discount_type = 'percentage' THEN (v_total * discount_value / 100)
                   WHEN discount_type = 'fixed' THEN discount_value
                   ELSE 0
               END
        INTO v_coupon_id, v_discount
        FROM Coupons 
        WHERE code = p_coupon_code AND active = TRUE AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP) AND min_order_amount <= v_total;
        
        IF v_coupon_id IS NULL THEN
            RAISE NOTICE 'Coupon % is invalid, expired, or minimum purchase amount not met.', p_coupon_code;
        ELSE
            v_total := GREATEST(v_total - v_discount, 0);
        END IF;
    END IF;

    -- Insert Order
    INSERT INTO Orders (user_id, status, total_amount, coupon_id)
    VALUES (p_user_id, 'Pending', v_total, v_coupon_id)
    RETURNING order_id INTO p_order_id;

    -- Insert Order Items (This will fire trigger_decrement_stock)
    INSERT INTO Order_Items (order_id, product_id, quantity, price_at_purchase)
    SELECT p_order_id, ci.product_id, ci.quantity, p.price
    FROM Cart_Items ci
    JOIN Products p ON ci.product_id = p.product_id
    WHERE ci.cart_id = v_cart_id;

    -- Insert default Shipping Details
    INSERT INTO Shipping_Details (order_id, address_id, shipping_method, status, estimated_delivery)
    VALUES (p_order_id, p_shipping_address_id, p_shipping_method, 'Preparing', CURRENT_TIMESTAMP + INTERVAL '5 days');

    -- Clear Cart Items
    DELETE FROM Cart_Items WHERE cart_id = v_cart_id;
    
    RAISE NOTICE 'Order % successfully placed for user ID %', p_order_id, p_user_id;
END;
$$ LANGUAGE plpgsql;


-- Procedure B: process_refund()
CREATE OR REPLACE PROCEDURE process_refund(p_order_id INT) AS $$
DECLARE
    v_order_status VARCHAR(20);
    v_item RECORD;
BEGIN
    -- Check order status
    SELECT status INTO v_order_status FROM Orders WHERE order_id = p_order_id;
    IF v_order_status IS NULL THEN
        RAISE EXCEPTION 'Order ID % not found', p_order_id;
    END IF;
    
    IF v_order_status = 'Refunded' THEN
        RAISE EXCEPTION 'Order ID % has already been refunded', p_order_id;
    END IF;

    -- Update Order Status
    UPDATE Orders SET status = 'Refunded' WHERE order_id = p_order_id;

    -- Update Payment Status
    UPDATE Payments SET status = 'Refunded' WHERE order_id = p_order_id;

    -- Return items to stock and log
    FOR v_item IN 
        SELECT product_id, quantity 
        FROM Order_Items 
        WHERE order_id = p_order_id
    LOOP
        -- Increment stock
        UPDATE Products 
        SET stock_qty = stock_qty + v_item.quantity 
        WHERE product_id = v_item.product_id;

        -- Log stock movement
        INSERT INTO Stock_Movements (product_id, quantity_changed, reason)
        VALUES (v_item.product_id, v_item.quantity, 'Order Refunded - Order ID: ' || p_order_id);
    END LOOP;

    -- Update shipping status
    UPDATE Shipping_Details
    SET status = 'Failed'
    WHERE order_id = p_order_id;

    RAISE NOTICE 'Order % and associated payments successfully refunded', p_order_id;
END;
$$ LANGUAGE plpgsql;
