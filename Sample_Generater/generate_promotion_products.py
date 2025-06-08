#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate 1000 sample promotion-product relationship data
"""

import random

def generate_promotion_products(num_records=1000, num_promotions=1000, num_products=1000):
    """Generate promotion-product relationship data"""
    promotion_products = []

    # Track unique combinations to avoid duplicates
    unique_combinations = set()

    # Generate unique promotion-product combinations
    while len(promotion_products) < num_records:
        promotion_id = random.randint(1, num_promotions)
        product_id = random.randint(1, num_products)

        # Ensure this is a unique combination
        combination = (promotion_id, product_id)
        if combination not in unique_combinations:
            unique_combinations.add(combination)

            promotion_products.append({
                'PromotionID': promotion_id,
                'ProductID': product_id
            })

    # Sort by promotion ID for better readability
    promotion_products.sort(key=lambda x: (x['PromotionID'], x['ProductID']))

    return promotion_products

def save_to_sql(promotion_products, output_file='promotion_products_data.sql'):
    """Save as SQL insert statements"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("USE canteen_management;\n")
        f.write("-- Bulk insert promotion-product relationship data\n")
        f.write("INSERT INTO PromotionProduct (PromotionID, ProductID) VALUES\n")

        values = []
        for relation in promotion_products:
            value = f"({relation['PromotionID']}, {relation['ProductID']})"
            values.append(value)

        f.write(',\n'.join(values) + ';\n')

if __name__ == "__main__":
    print("Generating promotion-product relationship data...")
    promotion_products = generate_promotion_products(1000)
    save_to_sql(promotion_products)
    print(f"Successfully generated 1000 promotion-product relationship data samples!")
