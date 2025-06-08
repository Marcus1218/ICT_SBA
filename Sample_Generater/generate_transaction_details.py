#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate 1000 sample transaction detail data
"""

import random
from decimal import Decimal

def generate_transaction_details(num_records=1000, num_transactions=1000, num_products=1000):
    """Generate transaction detail data"""
    transaction_details = []

    # Keep track of detail IDs and transaction totals
    detail_id = 1
    transaction_items = {}  # Dictionary to track items per transaction

    # Each transaction has between 1 and 5 items
    for transaction_id in range(1, num_transactions + 1):
        # Determine number of items for this transaction
        num_items = random.choices(
            [1, 2, 3, 4, 5],
            weights=[0.2, 0.3, 0.3, 0.15, 0.05],  # Most transactions have 1-3 items
            k=1
        )[0]

        # Create a set of products for this transaction (no duplicates)
        transaction_products = set()

        # Add random products to this transaction
        while len(transaction_products) < num_items and len(transaction_products) < num_products:
            product_id = random.randint(1, num_products)
            transaction_products.add(product_id)

        # Create detail records for each product in this transaction
        transaction_items[transaction_id] = []

        for product_id in transaction_products:
            # Most items are purchased in quantities of 1-3
            quantity = random.choices(
                [1, 2, 3, 4, 5],
                weights=[0.6, 0.25, 0.1, 0.03, 0.02],
                k=1
            )[0]

            # Unit price depends on the product
            # We'll create a realistic price based on the product ID
            # Higher ID values tend to be newer products with potentially higher prices
            base_price = Decimal(5.0)  # Minimum price
            price_factor = Decimal(product_id / 100)  # Price increases with product ID
            price_variance = Decimal(random.uniform(-2.0, 5.0))  # Add some randomness

            unit_price = round(base_price + price_factor + price_variance, 1)
            # Ensure minimum price is 5.0
            unit_price = max(unit_price, Decimal(5.0))

            transaction_details.append({
                'DetailID': detail_id,
                'TransactionID': transaction_id,
                'ProductID': product_id,
                'Quantity': quantity,
                'UnitPrice': unit_price
            })

            transaction_items[transaction_id].append({
                'ProductID': product_id,
                'Quantity': quantity,
                'UnitPrice': unit_price
            })

            detail_id += 1

    # If we need exactly 1000 records but have generated more or less, adjust
    if len(transaction_details) > num_records:
        # Randomly select records to keep
        transaction_details = random.sample(transaction_details, num_records)
        # Re-number DetailIDs
        for i, detail in enumerate(transaction_details):
            detail['DetailID'] = i + 1
    elif len(transaction_details) < num_records:
        # Add more records by duplicating some transactions with different products
        current_count = len(transaction_details)
        additional_needed = num_records - current_count

        # Duplicate some transactions with new products
        for _ in range(additional_needed):
            transaction_id = random.randint(1, num_transactions)
            product_id = random.randint(1, num_products)

            # Check for existing product in this transaction
            existing_products = [item['ProductID'] for item in transaction_items.get(transaction_id, [])]

            # Try to find a product not already in this transaction
            attempts = 0
            while product_id in existing_products and attempts < 10:
                product_id = random.randint(1, num_products)
                attempts += 1

            quantity = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1], k=1)[0]
            unit_price = round(Decimal(random.uniform(5.0, 50.0)), 1)

            transaction_details.append({
                'DetailID': detail_id,
                'TransactionID': transaction_id,
                'ProductID': product_id,
                'Quantity': quantity,
                'UnitPrice': unit_price
            })

            if transaction_id in transaction_items:
                transaction_items[transaction_id].append({
                    'ProductID': product_id,
                    'Quantity': quantity,
                    'UnitPrice': unit_price
                })
            else:
                transaction_items[transaction_id] = [{
                    'ProductID': product_id,
                    'Quantity': quantity,
                    'UnitPrice': unit_price
                }]

            detail_id += 1

    return transaction_details

def save_to_sql(transaction_details, output_file='transaction_details_data.sql'):
    """Save as SQL insert statements"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("USE canteen_management;\n")
        f.write("-- Bulk insert transaction detail data\n")
        f.write("INSERT INTO TransactionDetail (TransactionID, ProductID, Quantity, UnitPrice) VALUES\n")

        values = []
        for detail in transaction_details:
            value = f"({detail['TransactionID']}, {detail['ProductID']}, {detail['Quantity']}, {detail['UnitPrice']})"
            values.append(value)

        f.write(',\n'.join(values) + ';\n')

if __name__ == "__main__":
    print("Generating transaction detail data...")
    transaction_details = generate_transaction_details(1000)
    save_to_sql(transaction_details)
    print(f"Successfully generated 1000 transaction detail data samples!")
