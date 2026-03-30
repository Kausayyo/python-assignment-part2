# ============================================================
# Part 2: Restaurant Menu & Order Management System
# ============================================================

import copy  # needed for deep copy in Task 3

# -------------------- Provided Data ------------------------

menu = {
    "Paneer Tikka":   {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings":  {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":       {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":      {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":    {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":    {"category": "Mains",     "price":  40.0, "available": True},
    "Gulab Jamun":    {"category": "Desserts",  "price":  90.0, "available": True},
    "Rasgulla":       {"category": "Desserts",  "price":  80.0, "available": True},
    "Ice Cream":      {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":   {"stock": 10, "reorder_level": 3},
    "Chicken Wings":  {"stock":  8, "reorder_level": 2},
    "Veg Soup":       {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka":      {"stock": 20, "reorder_level": 5},
    "Veg Biryani":    {"stock":  6, "reorder_level": 3},
    "Garlic Naan":    {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":    {"stock":  5, "reorder_level": 2},
    "Rasgulla":       {"stock":  4, "reorder_level": 3},
    "Ice Cream":      {"stock":  7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1,  "items": ["Paneer Tikka", "Garlic Naan"],          "total": 220.0},
        {"order_id": 2,  "items": ["Gulab Jamun", "Veg Soup"],              "total": 210.0},
        {"order_id": 3,  "items": ["Butter Chicken", "Garlic Naan"],        "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4,  "items": ["Dal Tadka", "Garlic Naan"],             "total": 220.0},
        {"order_id": 5,  "items": ["Veg Biryani", "Gulab Jamun"],           "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6,  "items": ["Paneer Tikka", "Rasgulla"],             "total": 260.0},
        {"order_id": 7,  "items": ["Butter Chicken", "Veg Biryani"],        "total": 570.0},
        {"order_id": 8,  "items": ["Garlic Naan", "Gulab Jamun"],           "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9,  "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"],          "total": 270.0},
    ],
}


# ============================================================
# Task 1 — Explore the Menu (5 marks)
# ============================================================

# Get unique categories while preserving order
categories = []
for item in menu.values():
    if item["category"] not in categories:
        categories.append(item["category"])

# Print menu grouped by category
for category in categories:
    print(f"\n===== {category} =====")
    for item_name, details in menu.items():
        if details["category"] == category:
            status = "[Available]" if details["available"] else "[Unavailable]"
            print(f"{item_name:<18} ₹{details['price']:<8.2f} {status}")

# Stats using dictionary methods
total_items     = len(menu)
available_items = sum(1 for d in menu.values() if d["available"])

# Most expensive item — manual loop to avoid max() with key
most_expensive_name  = None
most_expensive_price = 0
for item_name, details in menu.items():
    if details["price"] > most_expensive_price:
        most_expensive_price = details["price"]
        most_expensive_name  = item_name

print(f"\nTotal menu items   : {total_items}")
print(f"Available items    : {available_items}")
print(f"Most expensive item: {most_expensive_name} (₹{most_expensive_price:.2f})")

print("\nItems priced under ₹150:")
for item_name, details in menu.items():
    if details["price"] < 150:
        print(f"  {item_name:<18} ₹{details['price']:.2f}")


# ============================================================
# Task 2 — Cart Operations (8 marks)
# ============================================================

cart = []  # each entry: {"item": name, "quantity": qty, "price": price}

# --- Add item to cart ---
def add_to_cart(item_name, quantity):
    # Check if item exists in menu
    if item_name not in menu:
        print(f"  ✗ '{item_name}' does not exist in the menu.")
        return
    # Check if item is available
    if not menu[item_name]["available"]:
        print(f"  ✗ '{item_name}' is currently unavailable.")
        return
    # Check if item already in cart — update quantity if so
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] += quantity
            print(f"  ✓ Updated '{item_name}' quantity to {entry['quantity']}")
            return
    # New item — add fresh entry
    cart.append({
        "item":     item_name,
        "quantity": quantity,
        "price":    menu[item_name]["price"]
    })
    print(f"  ✓ Added '{item_name}' x{quantity} to cart.")

# --- Remove item from cart ---
def remove_from_cart(item_name):
    for entry in cart:
        if entry["item"] == item_name:
            cart.remove(entry)
            print(f"  ✓ Removed '{item_name}' from cart.")
            return
    print(f"  ✗ '{item_name}' is not in the cart.")

# --- Update quantity of item in cart ---
def update_quantity(item_name, new_quantity):
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] = new_quantity
            print(f"  ✓ Updated '{item_name}' quantity to {new_quantity}.")
            return
    print(f"  ✗ '{item_name}' is not in the cart.")

# --- Helper to print current cart state ---
def print_cart(label="Cart State"):
    print(f"\n  [{label}]")
    if not cart:
        print("  Cart is empty.")
    for entry in cart:
        print(f"  {entry['item']:<18} x{entry['quantity']}  ₹{entry['price'] * entry['quantity']:.2f}")

# --- Simulate the sequence ---
print("\n========== Cart Operations ==========")

add_to_cart("Paneer Tikka", 2)
print_cart("After adding Paneer Tikka x2")

add_to_cart("Gulab Jamun", 1)
print_cart("After adding Gulab Jamun x1")

add_to_cart("Paneer Tikka", 1)   # should update to 3
print_cart("After adding Paneer Tikka x1 again")

add_to_cart("Mystery Burger", 1) # does not exist
add_to_cart("Chicken Wings", 1)  # unavailable
print_cart("After invalid attempts")

remove_from_cart("Gulab Jamun")
print_cart("After removing Gulab Jamun")

# --- Final Order Summary ---
subtotal = sum(e["price"] * e["quantity"] for e in cart)
gst      = round(subtotal * 0.05, 2)
total    = round(subtotal + gst, 2)

print("\n========== Order Summary ==========")
for entry in cart:
    line_total = entry["price"] * entry["quantity"]
    print(f"{entry['item']:<20} x{entry['quantity']}   ₹{line_total:.2f}")
print("------------------------------------")
print(f"{'Subtotal:':<28} ₹{subtotal:.2f}")
print(f"{'GST (5%):':<28} ₹{gst:.2f}")
print(f"{'Total Payable:':<28} ₹{total:.2f}")
print("====================================")


# ============================================================
# Task 3 — Inventory Tracker with Deep Copy (6 marks)
# ============================================================

# Deep copy inventory BEFORE any changes
inventory_backup = copy.deepcopy(inventory)

# Demonstrate deep copy works — change one value, backup unaffected
print("\n--- Deep Copy Demonstration ---")
inventory["Garlic Naan"]["stock"] = 999  # temporary change
print(f"inventory['Garlic Naan'] stock       : {inventory['Garlic Naan']['stock']}")
print(f"inventory_backup['Garlic Naan'] stock: {inventory_backup['Garlic Naan']['stock']}")

# Restore inventory to original
inventory["Garlic Naan"]["stock"] = 30
print("Inventory restored to original.\n")

# Simulate order fulfilment — deduct cart quantities from inventory
print("--- Deducting cart items from inventory ---")
for entry in cart:
    item_name = entry["item"]
    qty       = entry["quantity"]
    available_stock = inventory[item_name]["stock"]

    if available_stock >= qty:
        inventory[item_name]["stock"] -= qty
        print(f"  ✓ Deducted {qty} of '{item_name}'. Stock left: {inventory[item_name]['stock']}")
    else:
        # Insufficient stock — deduct only what's available
        print(f"  ⚠ Insufficient stock for '{item_name}'. Deducting {available_stock} (requested {qty}).")
        inventory[item_name]["stock"] = 0

# Reorder alerts
print("\n--- Reorder Alerts ---")
for item_name, details in inventory.items():
    if details["stock"] <= details["reorder_level"]:
        print(f"  ⚠ Reorder Alert: {item_name} — Only {details['stock']} unit(s) left (reorder level: {details['reorder_level']})")

# Confirm deep copy — print both to show they differ
print("\n--- Inventory vs Backup (showing difference) ---")
print(f"{'Item':<18} {'Current Stock':<16} {'Backup Stock'}")
print("-" * 48)
for item_name in inventory:
    curr = inventory[item_name]["stock"]
    bkp  = inventory_backup[item_name]["stock"]
    diff = " ← changed" if curr != bkp else ""
    print(f"{item_name:<18} {curr:<16} {bkp}{diff}")


# ============================================================
# Task 4 — Daily Sales Log Analysis (6 marks)
# ============================================================

print("\n========== Daily Sales Log Analysis ==========")

# --- Revenue per day ---
print("\nRevenue per day:")
best_day     = None
best_revenue = 0

for date, orders in sales_log.items():
    daily_revenue = sum(order["total"] for order in orders)
    print(f"  {date}  ₹{daily_revenue:.2f}")
    if daily_revenue > best_revenue:
        best_revenue = daily_revenue
        best_day     = date

print(f"\nBest-selling day: {best_day} (₹{best_revenue:.2f})")

# --- Most ordered item across all orders ---
item_count = {}  # counts how many orders each item appears in

for orders in sales_log.values():
    for order in orders:
        for item in order["items"]:
            if item not in item_count:
                item_count[item] = 0
            item_count[item] += 1

# Find item with highest count manually
most_ordered_item  = None
most_ordered_count = 0
for item, count in item_count.items():
    if count > most_ordered_count:
        most_ordered_count = count
        most_ordered_item  = item

print(f"Most ordered item : {most_ordered_item} (appeared in {most_ordered_count} orders)")

# --- Add new day to sales_log ---
sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"],                     "total": 260.0},
]

# Reprint revenue per day + best selling day after update
print("\n--- Updated Revenue Per Day ---")
best_day     = None
best_revenue = 0

for date, orders in sales_log.items():
    daily_revenue = sum(order["total"] for order in orders)
    print(f"  {date}  ₹{daily_revenue:.2f}")
    if daily_revenue > best_revenue:
        best_revenue = daily_revenue
        best_day     = date

print(f"\nUpdated Best-selling day: {best_day} (₹{best_revenue:.2f})")

# --- Numbered list of all orders using enumerate ---
print("\n--- All Orders (Numbered) ---")
counter = 1  # global counter across all dates
for date, orders in sales_log.items():
    for order in orders:
        items_str = ", ".join(order["items"])
        print(f"{counter:<4} [{date}] Order #{order['order_id']:<3} — ₹{order['total']:.2f} — Items: {items_str}")
        counter += 1
