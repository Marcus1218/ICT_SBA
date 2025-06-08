#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate 1000 sample promotion data
"""

import random
import datetime
from faker import Faker

# Initialize Faker
fake = Faker('en_US')

def generate_promotions(num_records=1000):
    """Generate promotion data"""
    promotions = []

    # Promotion types and descriptions
    promotion_types = [
        "Discount", "Special Offer", "Bundle Deal", "Seasonal Promotion",
        "Holiday Special", "Flash Sale", "Clearance", "Member Exclusive",
        "Buy One Get One", "Limited Time", "Student Special", "Teacher Deal"
    ]

    # Item descriptors
    item_descriptors = [
        "Food Items", "Snacks", "Beverages", "Combo Meals", "Main Dishes",
        "Desserts", "Breakfast Items", "Lunch Specials", "Fresh Products",
        "Healthy Options", "Popular Items", "Premium Selection"
    ]

    # Date ranges for promotions (we'll create promotions spanning the past and future)
    today = datetime.date(2025, 6, 8)  # Current date
    earliest_start = today - datetime.timedelta(days=365)  # Up to a year ago
    latest_end = today + datetime.timedelta(days=365)  # Up to a year in future

    for i in range(1, num_records + 1):
        # Generate promotion name
        promotion_type = random.choice(promotion_types)
        item_descriptor = random.choice(item_descriptors)

        if random.random() < 0.3:
            # Some promotions are for specific products
            product_name = fake.word().capitalize()
            promotion_name = f"{promotion_type}: {product_name} {item_descriptor}"
        else:
            # General promotions
            promotion_name = f"{promotion_type} on {item_descriptor}"

        # Generate discount rate (between 5% and 50% off)
        discount_rate = round(random.uniform(0.5, 0.95), 2)

        # Generate promotion dates
        # Some promotions start in the past, some start in the future
        days_offset_start = random.randint(-365, 180)
        start_date = today + datetime.timedelta(days=days_offset_start)

        # Duration between 1 day and 60 days
        duration = random.randint(1, 60)
        end_date = start_date + datetime.timedelta(days=duration)

        # Ensure end date is not beyond latest_end
        if end_date > latest_end:
            end_date = latest_end

        promotions.append({
            'PromotionID': i,
            'PromotionName': promotion_name,
            'DiscountRate': discount_rate,
            'StartDate': start_date.strftime('%Y-%m-%d'),
            'EndDate': end_date.strftime('%Y-%m-%d')
        })

    return promotions

def save_to_sql(promotions, output_file='promotions_data.sql'):
    """Save as SQL insert statements"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("USE canteen_management;\n")
        f.write("-- Bulk insert promotion data\n")
        f.write("INSERT INTO Promotion (PromotionName, DiscountRate, StartDate, EndDate) VALUES\n")

        values = []
        for promo in promotions:
            # Escape single quotes in promotion name
            promo_name = promo['PromotionName'].replace("'", "''")
            value = f"('{promo_name}', {promo['DiscountRate']}, '{promo['StartDate']}', '{promo['EndDate']}')"
            values.append(value)

        f.write(',\n'.join(values) + ';\n')

if __name__ == "__main__":
    print("Generating promotion data...")
    promotions = generate_promotions(1000)
    save_to_sql(promotions)
    print(f"Successfully generated 1000 promotion data samples!")
