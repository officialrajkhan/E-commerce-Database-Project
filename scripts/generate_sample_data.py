import random
import datetime
import os

def generate_data():
    # Setup random seed for deterministic generation
    random.seed(42)

    # 1. Countries, States, Cities (match create_tables.sql structure)
    countries = [
        (1, "India"),
        (2, "USA")
    ]
    
    states = [
        (1, "Maharashtra", 1),
        (2, "Karnataka", 1),
        (3, "California", 2),
        (4, "New York", 2),
        (5, "Texas", 2)
    ]
    
    cities = [
        (1, "Mumbai", 1),
        (2, "Pune", 1),
        (3, "Bangalore", 2),
        (4, "San Francisco", 3),
        (5, "Los Angeles", 3),
        (6, "New York City", 4),
        (7, "Austin", 5)
    ]

    # 2. Users (60 users)
    first_names = [
        "Raj", "Aisha", "John", "Emily", "Arjun", "Neha", "Michael", "Sarah", "Vikram", "Priya",
        "David", "Jessica", "Amit", "Anjali", "James", "Katelyn", "Rahul", "Pooja", "Robert", "Mary",
        "Karan", "Sneha", "William", "Patricia", "Sanjay", "Ritu", "Daniel", "Jennifer", "Vijay", "Divya",
        "Joseph", "Elizabeth", "Abhishek", "Komal", "Charles", "Linda", "Rohan", "Shalini", "Thomas", "Barbara",
        "Aditya", "Swati", "Christopher", "Susan", "Yash", "Tanvi", "Matthew", "Margaret", "Harsh", "Deepika",
        "Donald", "Dorothy", "Gaurav", "Nisha", "Mark", "Lisa", "Pranav", "Kriti", "Paul", "Nancy"
    ]
    
    last_names = [
        "Kumar", "Sharma", "Smith", "Davis", "Mehta", "Patel", "Johnson", "Brown", "Singh", "Gupta",
        "Miller", "Wilson", "Joshi", "Verma", "Jones", "Garcia", "Reddy", "Rao", "Williams", "Miller",
        "Malhotra", "Iyer", "Anderson", "Thomas", "Nair", "Kapoor", "Taylor", "Moore", "Sen", "Bose",
        "Jackson", "Martin", "Choudhury", "Das", "Lee", "Perez", "Goel", "Bansal", "Thompson", "White",
        "Chawla", "Sinha", "Harris", "Sanchez", "Shah", "Dubey", "Clark", "Ramirez", "Trivedi", "Saxena",
        "Lewis", "Robinson", "Pandey", "Mishra", "Walker", "Young", "Deshmukh", "Kulkarni", "Allen", "King"
    ]

    users = []
    emails_set = set()
    for i in range(1, 61):
        name = f"{first_names[i-1]} {last_names[i-1]}"
        email_prefix = name.lower().replace(" ", "")
        email = f"{email_prefix}@example.com"
        
        # Ensure email uniqueness
        counter = 1
        while email in emails_set:
            email = f"{email_prefix}{counter}@example.com"
            counter += 1
        emails_set.add(email)
        
        phone = f"{random.randint(60000, 99999)}{random.randint(10000, 99999)}"
        created_at = datetime.datetime(2025, 12, 1) + datetime.timedelta(days=random.randint(0, 100))
        users.append((i, name, email, phone, created_at.strftime('%Y-%m-%d %H:%M:%S+00')))

    # Addresses (1 to 2 addresses per user)
    addresses = []
    address_id_counter = 1
    streets = [
        "MG Road Apt", "Sunset Blvd Apt", "Broadway St Suite", "Market St Flat", "Link Road Floor",
        "Park Avenue House", "High Street Apt", "Baker Street", "Oak Road", "Main Street Villa"
    ]
    for user_id in range(1, 61):
        # Shipping address
        city = random.choice(cities)
        line1 = f"{random.randint(1, 500)} {random.choice(streets)} {random.randint(1, 100)}"
        zipcode = f"{random.randint(100000, 999999)}" if city[2] <= 2 else f"{random.randint(10000, 99999)}"
        addresses.append((address_id_counter, user_id, line1, zipcode, city[0], "Shipping"))
        address_id_counter += 1
        
        # Billing address (50% chance of being different)
        if random.random() < 0.5:
            line1_bill = f"{random.randint(1, 500)} {random.choice(streets)} {random.randint(1, 100)}"
            addresses.append((address_id_counter, user_id, line1_bill, zipcode, city[0], "Billing"))
            address_id_counter += 1
        else:
            addresses.append((address_id_counter, user_id, line1, zipcode, city[0], "Billing"))
            address_id_counter += 1

    # 3. Sellers (10 sellers)
    seller_names = [
        "Appario Retail", "Cloudtail India", "OmniTech Solutions", "Clicktech Retail", 
        "Global Fashion Corp", "Supercom Net", "RetailNet", "Kay Kay Deals", "Cocoblu Retail", "Darshita Electronics"
    ]
    sellers = []
    for i in range(1, 11):
        name = seller_names[i-1]
        email = f"contact@{name.lower().replace(' ', '')}.com"
        phone = f"98765{i:05d}"
        biz = f"{name} Private Limited"
        sellers.append((i, name, email, phone, biz))

    # 4. Categories (Hierarchical category tree)
    # parent_id matches: Electronics(1), Fashion(4), Computers(7), Home & Kitchen(10)
    categories = [
        (1, "Electronics", "NULL"),
        (2, "Mobile Phones", 1),
        (3, "Audio", 1),
        (4, "Fashion", "NULL"),
        (5, "Clothing", 4),
        (6, "Footwear", 4),
        (7, "Computers", "NULL"),
        (8, "Laptops", 7),
        (9, "Accessories", 7),
        (10, "Home & Kitchen", "NULL")
    ]

    # 5. Products (35 Products)
    # Category mappings:
    # 2: Mobile (Electronics)
    # 3: Audio (Electronics)
    # 5: Clothing (Fashion)
    # 6: Footwear (Fashion)
    # 8: Laptops (Computers)
    # 9: Accessories (Computers)
    # 10: Home & Kitchen
    product_pool = [
        # Mobile Phones
        ("iPhone 15 Pro", 2, 109999.00),
        ("Samsung Galaxy S24 Ultra", 2, 124999.00),
        ("OnePlus 12", 2, 64999.00),
        ("Google Pixel 8 Pro", 2, 93999.00),
        ("Redmi Note 13 Pro", 2, 25999.00),
        # Audio
        ("Sony WH-1000XM5", 3, 29999.00),
        ("Bose QuietComfort Ultra", 3, 35999.00),
        ("Apple AirPods Pro (2nd Gen)", 3, 24999.00),
        ("Boat Airdopes 141", 3, 1499.00),
        ("JBL Flip 6 Speaker", 3, 9999.00),
        # Clothing
        ("Levi's 511 Slim Fit Jeans", 5, 3499.00),
        ("Nike Windrunner Jacket", 5, 4999.00),
        ("Adidas Originals Hoodie", 5, 3999.00),
        ("Zara Cotton Oxford Shirt", 5, 2499.00),
        ("Puma Classic Sports Tee", 5, 1299.00),
        # Footwear
        ("Nike Air Max 90", 6, 9999.00),
        ("Adidas Ultraboost Light", 6, 17999.00),
        ("Puma Suede Classic", 6, 5999.00),
        ("Crocs Classic Clogs", 6, 2999.00),
        ("Birkenstock Arizona Sandals", 6, 8999.00),
        # Laptops
        ("Apple MacBook Air M3", 8, 114900.00),
        ("Apple MacBook Pro 16 M3 Max", 8, 349900.00),
        ("Dell XPS 13", 8, 129999.00),
        ("Lenovo ThinkPad X1 Carbon", 8, 159999.00),
        ("ASUS ROG Zephyrus G14", 8, 144999.00),
        # Accessories
        ("Logitech MX Master 3S", 9, 9499.00),
        ("Keychron K2 Mechanical Keyboard", 9, 7999.00),
        ("Samsung T7 2TB Portable SSD", 9, 14999.00),
        ("LG 27-inch Ultrawide Monitor", 9, 19999.00),
        ("Anker 737 Power Bank", 9, 8999.00),
        # Home & Kitchen
        ("Instant Pot Duo 7-in-1", 10, 8999.00),
        ("Philips Air Fryer HD9200", 10, 6999.00),
        ("Dyson V11 Absolute Vacuum", 10, 49900.00),
        ("Ninja Professional Blender", 10, 11999.00),
        ("Philips Garment Steamer", 10, 3499.00)
    ]
    
    products = []
    for i, item in enumerate(product_pool, 1):
        name, cat_id, price = item
        seller_id = random.randint(1, 10)
        stock = random.randint(10, 150)
        products.append((i, seller_id, cat_id, name, price, stock))

    # 6. Tags & Product Tags
    tags = ["Premium", "Bestseller", "New Arrival", "Wireless", "Eco-friendly", "Durable", "Comfort", "Smart"]
    product_tags = []
    for p_id in range(1, 36):
        # Pick 1-3 tags randomly
        chosen_tags = random.sample(range(1, len(tags) + 1), random.randint(1, 3))
        for t_id in chosen_tags:
            product_tags.append((p_id, t_id))

    # 7. Coupons (10 coupons)
    coupons = [
        (1, "WELCOME10", "percentage", 10.00, 0.00, "TRUE", "NULL"),
        (2, "SAVE500", "fixed", 500.00, 3000.00, "TRUE", "NULL"),
        (3, "BIGDEAL25", "percentage", 25.00, 5000.00, "TRUE", "CURRENT_TIMESTAMP + INTERVAL '60 days'"),
        (4, "FESTIVE15", "percentage", 15.00, 1000.00, "TRUE", "CURRENT_TIMESTAMP + INTERVAL '90 days'"),
        (5, "FLASH50", "percentage", 50.00, 10000.00, "TRUE", "CURRENT_TIMESTAMP - INTERVAL '5 days'"), # Expired
        (6, "SUPER1000", "fixed", 1000.00, 8000.00, "TRUE", "NULL"),
        (7, "MOBILE5", "percentage", 5.00, 20000.00, "TRUE", "NULL"),
        (8, "CLOTHING20", "percentage", 20.00, 2000.00, "TRUE", "NULL"),
        (9, "EXPIRED100", "fixed", 100.00, 500.00, "FALSE", "NULL"), # Inactive
        (10, "FREESHIP", "fixed", 150.00, 1500.00, "TRUE", "NULL")
    ]

    # 8. Orders, Order Items, Payments, Shipping Details (115 orders)
    orders = []
    order_items = []
    payments = []
    shipping_details = []
    
    order_item_id_counter = 1
    payment_id_counter = 1
    shipping_id_counter = 1
    
    # Generate dates over the last 6 months (chronological logic)
    start_date = datetime.datetime(2026, 1, 1)
    
    for order_id in range(1, 116):
        user_id = random.randint(1, 60)
        
        # Chronological order dates
        order_date = start_date + datetime.timedelta(days=(order_id * 1.5))
        order_date_str = order_date.strftime('%Y-%m-%d %H:%M:%S+00')
        
        # Order status distribution
        status_rand = random.random()
        if status_rand < 0.70:
            order_status = "Delivered"
        elif status_rand < 0.85:
            order_status = "Shipped"
        elif status_rand < 0.92:
            order_status = "Paid"
        elif status_rand < 0.96:
            order_status = "Pending"
        else:
            order_status = random.choice(["Cancelled", "Refunded"])
            
        # Determine items (1 to 3 items)
        num_items = random.randint(1, 3)
        chosen_products = random.sample(products, num_items)
        
        subtotal = 0.0
        items_detail = []
        for prod in chosen_products:
            prod_id, _, _, name, price, _ = prod
            qty = random.randint(1, 2)
            item_price = float(price)
            subtotal += item_price * qty
            items_detail.append((prod_id, qty, item_price))
            
        # Apply coupon (25% chance if subtotal qualifies)
        coupon_id = "NULL"
        discount = 0.0
        if random.random() < 0.25:
            valid_coupons = []
            for c in coupons:
                min_amt = float(c[3])
                # Filter applicable coupons (active, valid expiry, min amount)
                if c[5] == "TRUE" and "INTERVAL '-5 days'" not in c[6] and subtotal >= min_amt:
                    valid_coupons.append(c)
            if valid_coupons:
                chosen_coupon = random.choice(valid_coupons)
                coupon_id = chosen_coupon[0]
                disc_type = chosen_coupon[2]
                disc_val = float(chosen_coupon[3])
                if disc_type == "percentage":
                    discount = subtotal * (disc_val / 100.0)
                else:
                    discount = disc_val
                discount = min(discount, subtotal) # Coupon discount shouldn't exceed subtotal
                
        total_amount = max(subtotal - discount, 0.0)
        orders.append((order_id, user_id, coupon_id, order_date_str, order_status, total_amount))
        
        # Add order items
        for prod_id, qty, item_price in items_detail:
            order_items.append((order_item_id_counter, order_id, prod_id, qty, item_price))
            order_item_id_counter += 1
            
        # Payments
        pay_method = random.choice(["UPI", "Card", "COD"])
        if order_status in ["Delivered", "Shipped", "Paid"]:
            pay_status = "Paid"
        elif order_status == "Pending":
            pay_status = "Pending" if pay_method == "COD" else random.choice(["Pending", "Failed"])
        elif order_status == "Refunded":
            pay_status = "Refunded"
        else: # Cancelled
            pay_status = "Failed" if pay_method != "COD" else "Pending"
            
        payments.append((payment_id_counter, order_id, pay_method, pay_status, total_amount, order_date_str))
        payment_id_counter += 1
        
        # Shipping Details
        # Address matching user
        user_shipping_addresses = [a for a in addresses if a[1] == user_id and a[5] == "Shipping"]
        address_id = user_shipping_addresses[0][0] if user_shipping_addresses else 1
        
        ship_method = random.choice(["Standard", "Express"])
        tracking_num = f"TRK{order_date.strftime('%Y%m%d')}{order_id:04d}"
        
        if order_status == "Delivered":
            ship_status = "Delivered"
            est_del = order_date + datetime.timedelta(days=random.randint(2, 4))
            ship_at = order_date + datetime.timedelta(days=1)
            del_at = est_del
            est_del_str = f"'{est_del.strftime('%Y-%m-%d %H:%M:%S+00')}'"
            ship_at_str = f"'{ship_at.strftime('%Y-%m-%d %H:%M:%S+00')}'"
            del_at_str = f"'{del_at.strftime('%Y-%m-%d %H:%M:%S+00')}'"
        elif order_status == "Shipped":
            ship_status = random.choice(["Shipped", "In Transit", "Out for Delivery"])
            est_del = order_date + datetime.timedelta(days=3)
            ship_at = order_date + datetime.timedelta(days=1)
            est_del_str = f"'{est_del.strftime('%Y-%m-%d %H:%M:%S+00')}'"
            ship_at_str = f"'{ship_at.strftime('%Y-%m-%d %H:%M:%S+00')}'"
            del_at_str = "NULL"
        elif order_status in ["Paid", "Pending"]:
            ship_status = "Preparing"
            est_del = order_date + datetime.timedelta(days=4)
            est_del_str = f"'{est_del.strftime('%Y-%m-%d %H:%M:%S+00')}'"
            ship_at_str = "NULL"
            del_at_str = "NULL"
        else: # Cancelled/Refunded
            ship_status = "Failed"
            est_del_str = "NULL"
            ship_at_str = "NULL"
            del_at_str = "NULL"
            
        shipping_details.append((
            shipping_id_counter, order_id, address_id, ship_method, 
            tracking_num, ship_status, est_del_str, ship_at_str, del_at_str
        ))
        shipping_id_counter += 1

    # 9. Reviews (45 random product reviews from users who purchased)
    reviews = []
    review_id_counter = 1
    review_templates = {
        5: ["Absolutely loved it! Premium feel.", "Amazing quality, highly recommend.", "Worth every single penny.", "Exceptional performance, fits perfectly!"],
        4: ["Very good product, satisfied.", "Great value for money.", "Works well, solid build quality.", "Delivery was fast, product is great."],
        3: ["Average quality, does the job.", "Decent but could be better.", "Okay for the price.", "Standard product, nothing special."],
        2: ["Disappointed with the quality.", "Build is flimsy, expected better.", "Average performance, not worth the hype.", "Not satisfied, has some issues."],
        1: ["Terrible experience, broke in a day.", "Waste of money, do not buy.", "Poor quality, extremely disappointed.", "Faulty unit, returning immediately."]
    }
    
    # Find combinations of users and products who had completed/delivered orders
    delivered_purchases = []
    for oi in order_items:
        o_id = oi[1]
        p_id = oi[2]
        # Find order user
        order_row = [o for o in orders if o[0] == o_id][0]
        u_id = order_row[1]
        if order_row[4] == "Delivered":
            delivered_purchases.append((u_id, p_id))
            
    # Deduplicate purchases
    delivered_purchases = list(set(delivered_purchases))
    random.shuffle(delivered_purchases)
    
    # Create ~45 reviews
    reviewed_pairs = set()
    for u_id, p_id in delivered_purchases[:45]:
        if (u_id, p_id) in reviewed_pairs:
            continue
        reviewed_pairs.add((u_id, p_id))
        rating = random.choices([5, 4, 3, 2, 1], weights=[45, 30, 15, 6, 4])[0]
        comment = random.choice(review_templates[rating])
        created = datetime.datetime(2026, 4, 1) + datetime.timedelta(days=random.randint(1, 60))
        reviews.append((
            review_id_counter, u_id, p_id, rating, 
            comment.replace("'", "''"), created.strftime('%Y-%m-%d %H:%M:%S+00')
        ))
        review_id_counter += 1

    # 10. Live Carts and Wishlists (simulating current session data)
    carts = []
    cart_items = []
    cart_item_id_counter = 1
    
    wishlists = []
    wishlist_items = []
    wishlist_item_id_counter = 1
    
    for u_id in range(1, 61):
        carts.append((u_id, u_id))
        wishlists.append((u_id, u_id))
        
        # 15 users have items in carts
        if u_id in range(5, 20):
            num_cart_items = random.randint(1, 3)
            cart_prods = random.sample(products, num_cart_items)
            for prod in cart_prods:
                cart_items.append((cart_item_id_counter, u_id, prod[0], random.randint(1, 2)))
                cart_item_id_counter += 1
                
        # 25 users have items in wishlists
        if u_id in range(15, 40):
            num_wish_items = random.randint(1, 4)
            wish_prods = random.sample(products, num_wish_items)
            for prod in wish_prods:
                wishlist_items.append((wishlist_item_id_counter, u_id, prod[0]))
                wishlist_item_id_counter += 1

    # 11. Initial Stock Movements
    stock_movements = []
    movement_id_counter = 1
    for p in products:
        p_id = p[0]
        initial_stock = p[5]
        stock_movements.append((movement_id_counter, p_id, initial_stock, "Initial Restock"))
        movement_id_counter += 1
        
    # Also log stock reductions for Delivered orders (since our trigger does it automatically, 
    # we don't strictly need to write manual stock_movements for them to prevent duplication. 
    # But writing a seed script means we let the INSERT queries run. 
    # If the user disables trigger or loads data directly, having a few logs is nice. 
    # Since we are using standard INSERT into Order_Items, the trigger will AUTOMATICALLY 
    # fire during DB initialization and insert Stock_Movements and decrement stock!
    # Therefore, we must seed Products with their CURRENT stock + total ordered stock, OR 
    # we can seed Products with the target stock and NOT insert manual stock logs for sales.
    # To keep things consistent, since our trigger is enabled, when the docker image loads 
    # sample_data.sql and inserts Order_Items, it will decrement stock automatically!
    # So if a product has price 100 and stock_qty 50 in Products insert, and Order_Items 
    # inserts a quantity of 5, the product stock will drop to 45, and a stock log will be created.
    # This is perfect! So we don't need manual Stock_Movements for orders. We only insert the 
    # "Initial Restock" movement to represent the initial load of products!)

    # =========================================================================
    # BUILD SQL FILE CONTENT
    # =========================================================================
    
    sql = []
    sql.append("-- =========================================================================")
    sql.append("-- SEED DATA FOR E-COMMERCE DATABASE SYSTEM")
    sql.append("-- Generated Chronologically and Normalized")
    sql.append("-- =========================================================================")
    sql.append("\nBEGIN;\n")
    
    # Country, State, City
    sql.append("-- Countries")
    for row in countries:
        sql.append(f"INSERT INTO Country (country_id, country_name) VALUES ({row[0]}, '{row[1]}') ON CONFLICT (country_id) DO NOTHING;")
    sql.append("SELECT setval('country_country_id_seq', COALESCE((SELECT MAX(country_id)+1 FROM Country), 1), false);\n")
    
    sql.append("-- States")
    for row in states:
        sql.append(f"INSERT INTO State (state_id, state_name, country_id) VALUES ({row[0]}, '{row[1]}', {row[2]}) ON CONFLICT (state_id) DO NOTHING;")
    sql.append("SELECT setval('state_state_id_seq', COALESCE((SELECT MAX(state_id)+1 FROM State), 1), false);\n")
    
    sql.append("-- Cities")
    for row in cities:
        sql.append(f"INSERT INTO City (city_id, city_name, state_id) VALUES ({row[0]}, '{row[1]}', {row[2]}) ON CONFLICT (city_id) DO NOTHING;")
    sql.append("SELECT setval('city_city_id_seq', COALESCE((SELECT MAX(city_id)+1 FROM City), 1), false);\n")

    # Users
    sql.append("-- Users")
    for u in users:
        sql.append(f"INSERT INTO Users (user_id, name, email, phone, created_at) VALUES ({u[0]}, '{u[1]}', '{u[2]}', '{u[3]}', '{u[4]}');")
    sql.append("SELECT setval('users_user_id_seq', COALESCE((SELECT MAX(user_id)+1 FROM Users), 1), false);\n")

    # Addresses
    sql.append("-- Addresses")
    for a in addresses:
        sql.append(f"INSERT INTO Address (address_id, user_id, line1, zipcode, city_id, type) VALUES ({a[0]}, {a[1]}, '{a[2]}', '{a[3]}', {a[4]}, '{a[5]}');")
    sql.append("SELECT setval('address_address_id_seq', COALESCE((SELECT MAX(address_id)+1 FROM Address), 1), false);\n")

    # Sellers
    sql.append("-- Sellers")
    for s in sellers:
        sql.append(f"INSERT INTO Sellers (seller_id, name, email, phone, business_name) VALUES ({s[0]}, '{s[1]}', '{s[2]}', '{s[3]}', '{s[4]}');")
    sql.append("SELECT setval('sellers_seller_id_seq', COALESCE((SELECT MAX(seller_id)+1 FROM Sellers), 1), false);\n")

    # Categories
    sql.append("-- Categories")
    for c in categories:
        sql.append(f"INSERT INTO Categories (category_id, name, parent_id) VALUES ({c[0]}, '{c[1]}', {c[2]});")
    sql.append("SELECT setval('categories_category_id_seq', COALESCE((SELECT MAX(category_id)+1 FROM Categories), 1), false);\n")

    # Products
    # NOTE: Set initial stock high so that when triggers run on the 115 orders, they don't fail for insufficient stock!
    sql.append("-- Products (Stock quantities are pre-sale values; triggers will decrement them on Order_Items insert)")
    for p in products:
        # Increase the insert stock so they don't run out during order insertion
        pre_sale_stock = p[5] + 100
        sql.append(f"INSERT INTO Products (product_id, seller_id, category_id, name, price, stock_qty) VALUES ({p[0]}, {p[1]}, {p[2]}, '{p[3]}', {p[4]}, {pre_sale_stock});")
    sql.append("SELECT setval('products_product_id_seq', COALESCE((SELECT MAX(product_id)+1 FROM Products), 1), false);\n")

    # Tags & Product Tags
    sql.append("-- Tags")
    for idx, tag in enumerate(tags, 1):
        sql.append(f"INSERT INTO Tags (tag_id, name) VALUES ({idx}, '{tag}');")
    sql.append("SELECT setval('tags_tag_id_seq', COALESCE((SELECT MAX(tag_id)+1 FROM Tags), 1), false);\n")

    sql.append("-- Product Tags")
    for pt in product_tags:
        sql.append(f"INSERT INTO Product_Tags (product_id, tag_id) VALUES ({pt[0]}, {pt[1]});")
    sql.append("")

    # Coupons
    sql.append("-- Coupons")
    for c in coupons:
        sql.append(f"INSERT INTO Coupons (coupon_id, code, discount_type, discount_value, min_order_amount, active, expires_at) VALUES ({c[0]}, '{c[1]}', '{c[2]}', {c[3]}, {c[4]}, {c[5]}, {c[6]});")
    sql.append("SELECT setval('coupons_coupon_id_seq', COALESCE((SELECT MAX(coupon_id)+1 FROM Coupons), 1), false);\n")

    # Carts & Wishlists
    sql.append("-- Carts & Wishlists (Session state)")
    for u_id in range(1, 61):
        sql.append(f"INSERT INTO Carts (cart_id, user_id) VALUES ({u_id}, {u_id});")
        sql.append(f"INSERT INTO Wishlists (wishlist_id, user_id) VALUES ({u_id}, {u_id});")
    sql.append("SELECT setval('carts_cart_id_seq', COALESCE((SELECT MAX(cart_id)+1 FROM Carts), 1), false);")
    sql.append("SELECT setval('wishlists_wishlist_id_seq', COALESCE((SELECT MAX(wishlist_id)+1 FROM Wishlists), 1), false);\n")

    sql.append("-- Cart Items")
    for ci in cart_items:
        sql.append(f"INSERT INTO Cart_Items (cart_item_id, cart_id, product_id, quantity) VALUES ({ci[0]}, {ci[1]}, {ci[2]}, {ci[3]});")
    sql.append("SELECT setval('cart_items_cart_item_id_seq', COALESCE((SELECT MAX(cart_item_id)+1 FROM Cart_Items), 1), false);\n")

    sql.append("-- Wishlist Items")
    for wi in wishlist_items:
        sql.append(f"INSERT INTO Wishlist_Items (wishlist_item_id, wishlist_id, product_id) VALUES ({wi[0]}, {wi[1]}, {wi[2]});")
    sql.append("SELECT setval('wishlist_items_wishlist_item_id_seq', COALESCE((SELECT MAX(wishlist_item_id)+1 FROM Wishlist_Items), 1), false);\n")

    # Initial Stock Movements
    sql.append("-- Initial Stock Movements (Ledger entries)")
    for sm in stock_movements:
        sql.append(f"INSERT INTO Stock_Movements (movement_id, product_id, quantity_changed, reason) VALUES ({sm[0]}, {sm[1]}, {sm[2]}, '{sm[3]}');")
    sql.append("SELECT setval('stock_movements_movement_id_seq', COALESCE((SELECT MAX(movement_id)+1 FROM Stock_Movements), 1), false);\n")

    # Orders (Insert order items will trigger stock decrement)
    sql.append("-- Orders (Triggers will fire upon subsequent inserts)")
    for o in orders:
        sql.append(f"INSERT INTO Orders (order_id, user_id, coupon_id, order_date, status, total_amount) VALUES ({o[0]}, {o[1]}, {o[2]}, '{o[3]}', '{o[4]}', {o[5]});")
    sql.append("SELECT setval('orders_order_id_seq', COALESCE((SELECT MAX(order_id)+1 FROM Orders), 1), false);\n")

    # Shipping Details (Needs to be inserted before order items, or order items first? 
    # Order items trigger decrement, while payments trigger order status update.
    # In order to let triggers work seamlessly without integrity error, we insert Shipping Details, then Order Items, then Payments.)
    sql.append("-- Shipping Details")
    for sd in shipping_details:
        sql.append(f"INSERT INTO Shipping_Details (shipping_id, order_id, address_id, shipping_method, tracking_number, status, estimated_delivery, shipped_at, delivered_at) VALUES ({sd[0]}, {sd[1]}, {sd[2]}, '{sd[3]}', '{sd[4]}', '{sd[5]}', {sd[6]}, {sd[7]}, {sd[8]});")
    sql.append("SELECT setval('shipping_details_shipping_id_seq', COALESCE((SELECT MAX(shipping_id)+1 FROM Shipping_Details), 1), false);\n")

    sql.append("-- Order Items (This triggers decrement_stock_func)")
    for oi in order_items:
        sql.append(f"INSERT INTO Order_Items (order_item_id, order_id, product_id, quantity, price_at_purchase) VALUES ({oi[0]}, {oi[1]}, {oi[2]}, {oi[3]}, {oi[4]});")
    sql.append("SELECT setval('order_items_order_item_id_seq', COALESCE((SELECT MAX(order_item_id)+1 FROM Order_Items), 1), false);\n")

    # Payments
    sql.append("-- Payments")
    for pay in payments:
        sql.append(f"INSERT INTO Payments (payment_id, order_id, method, status, amount, transaction_date) VALUES ({pay[0]}, {pay[1]}, '{pay[2]}', '{pay[3]}', {pay[4]}, '{pay[5]}');")
    sql.append("SELECT setval('payments_payment_id_seq', COALESCE((SELECT MAX(payment_id)+1 FROM Payments), 1), false);\n")

    # Reviews
    sql.append("-- Reviews")
    for r in reviews:
        sql.append(f"INSERT INTO Reviews (review_id, user_id, product_id, rating, comment, created_at) VALUES ({r[0]}, {r[1]}, {r[2]}, {r[3]}, '{r[4]}', '{r[5]}');")
    sql.append("SELECT setval('reviews_review_id_seq', COALESCE((SELECT MAX(review_id)+1 FROM Reviews), 1), false);\n")

    sql.append("COMMIT;")
    
    # Save the output file
    target_path = "schema/sample_data.sql"
    with open(target_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sql))
        
    print(f"Sample data SQL generated successfully at {target_path}!")

if __name__ == "__main__":
    generate_data()
