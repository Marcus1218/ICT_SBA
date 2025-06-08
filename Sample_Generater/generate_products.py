#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate 1000 sample product data
"""

import random
import datetime
from decimal import Decimal

def generate_products(num_records=1000, num_suppliers=1000):
    """Generate product data"""
    products = []

    # Product categories
    categories = {
        'Main Dish': ['Sandwich', 'Burger', 'Pasta', 'Rice Box', 'Noodles', 'Sushi', 'Dumplings', 'Pizza Slice', 'Wrap'],
        'Drinks': ['Water', 'Juice', 'Milk', 'Soda', 'Tea', 'Coffee', 'Energy Drink', 'Smoothie', 'Yogurt Drink'],
        'Snacks': ['Chips', 'Chocolate', 'Cookies', 'Candy', 'Nuts', 'Popcorn', 'Crackers', 'Fruit Cup', 'Jelly'],
        'Fruits': ['Apple', 'Banana', 'Orange', 'Grapes', 'Watermelon Cup', 'Pear', 'Peach', 'Mixed Fruit Cup'],
        'Bakery': ['Bread', 'Cake', 'Donut', 'Muffin', 'Croissant', 'Pastry', 'Egg Tart', 'Bun', 'Cookie'],
        'Desserts': ['Ice Cream', 'Pudding', 'Jelly', 'Sweet Soup', 'Mousse', 'Custard', 'Trifle']
    }

    # Create a list of all products with their categories
    all_products = []
    for category, items in categories.items():
        for item in items:
            # Add some variations
            variations = ['Regular', 'Large', 'Small', 'Special', 'Premium', 'Light', 'Double']
            for variation in random.sample(variations, min(3, len(variations))):
                all_products.append((f"{variation} {item}", category))

    # Generate additional product names if needed
    while len(all_products) < num_records:
        category = random.choice(list(categories.keys()))
        base_item = random.choice(categories[category])
        variation = random.choice(['Regular', 'Large', 'Small', 'Special', 'Premium', 'Light', 'Double', 'Extra', 'Mini'])
        flavor = random.choice(['Classic', 'Spicy', 'Sweet', 'Sour', 'Tangy', 'Mild', 'Hot', 'Rich', 'Original'])
        all_products.append((f"{variation} {flavor} {base_item}", category))

    # Shuffle and take required number of products
    random.shuffle(all_products)
    product_names_categories = all_products[:num_records]

    # Current date for expiry date generation
    today = datetime.date(2025, 6, 8)  # Current date

    for i in range(1, num_records + 1):
        product_name, category = product_names_categories[i-1]

        # Price generation
        if category in ['Main Dish']:
            price = round(Decimal(random.uniform(15.0, 40.0)), 1)
        elif category in ['Drinks']:
            price = round(Decimal(random.uniform(5.0, 15.0)), 1)
        elif category in ['Snacks', 'Fruits']:
            price = round(Decimal(random.uniform(3.0, 12.0)), 1)
        elif category in ['Bakery', 'Desserts']:
            price = round(Decimal(random.uniform(7.0, 25.0)), 1)
        else:
            price = round(Decimal(random.uniform(5.0, 30.0)), 1)

        # Cost price (60-80% of selling price)
        cost_price_percentage = random.uniform(0.6, 0.8)
        cost_price = round(price * Decimal(cost_price_percentage), 1)

        # Stock
        stock_quantity = random.randint(0, 150)
        min_stock_threshold = random.randint(10, 30)

        # Supplier ID
        supplier_id = random.randint(1, min(num_suppliers, 1000))

        # Expiry date (only for perishable items)
        if category in ['Main Dish', 'Bakery', 'Fruits', 'Desserts'] or random.random() < 0.3:
            days_to_expire = random.randint(-5, 60)  # Some products may already be expired
            expiry_date = today + datetime.timedelta(days=days_to_expire)
            expiry_date_str = expiry_date.strftime('%Y-%m-%d')
        else:
            expiry_date_str = None

        products.append({
            'ProductID': i,
            'ProductName': product_name,
            'Price': price,
            'CostPrice': cost_price,
            'StockQuantity': stock_quantity,
            'MinStockThreshold': min_stock_threshold,
            'Category': category,
            'SupplierID': supplier_id,
            'ExpiryDate': expiry_date_str
        })

    return products

def save_to_sql(products, output_file='products_data.sql'):
    """Save as SQL insert statements"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("USE canteen_management;\n")
        f.write("-- Bulk insert product data\n")
        f.write("INSERT INTO Product (ProductName, Price, CostPrice, StockQuantity, MinStockThreshold, Category, SupplierID, ExpiryDate) VALUES\n")

        values = []
        for product in products:
            # Escape single quotes in product name
            product_name = product['ProductName'].replace("'", "''")

            expiry_date = f"'{product['ExpiryDate']}'" if product['ExpiryDate'] else "NULL"
            value = f"('{product_name}', {product['Price']}, {product['CostPrice']}, {product['StockQuantity']}, {product['MinStockThreshold']}, '{product['Category']}', {product['SupplierID']}, {expiry_date})"
            values.append(value)

        f.write(',\n'.join(values) + ';\n')

if __name__ == "__main__":
    print("Generating product data...")
    products = generate_products(1000)
    save_to_sql(products)
    print(f"Successfully generated 1000 product data samples!")
