#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate 1000 sample restock order data
"""

import random
import datetime

def generate_restock_orders(num_records=1000, num_products=1000, num_suppliers=1000):
    """Generate restock order data"""
    restock_orders = []

    # Define status options and their probabilities
    statuses = ['Pending', 'Shipped', 'Delivered', 'Cancelled']
    status_weights = [0.3, 0.2, 0.45, 0.05]  # 30% pending, 20% shipped, 45% delivered, 5% cancelled

    # Define date range for orders
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2025, 6, 8)  # Current date
    date_range = (end_date - start_date).days

    for i in range(1, num_records + 1):
        # Select random product and its supplier
        product_id = random.randint(1, num_products)
        supplier_id = random.randint(1, num_suppliers)

        # Generate order quantity (typically between 10 and 200)
        order_quantity = random.randint(10, 200)

        # Random order date
        days_before_now = random.randint(0, date_range)
        order_date = end_date - datetime.timedelta(days=days_before_now)

        # Status and arrival date
        status = random.choices(statuses, weights=status_weights)[0]

        if status == 'Delivered':
            # Delivered orders have arrival dates
            # Typically arrive 1-14 days after ordering
            arrival_days = random.randint(1, 14)
            arrival_date = order_date + datetime.timedelta(days=arrival_days)

            # Ensure arrival date is not in the future
            if arrival_date > end_date:
                arrival_date = end_date
        elif status == 'Shipped':
            # Shipped orders have arrival dates in the future
            arrival_days = random.randint(1, 7)
            arrival_date = order_date + datetime.timedelta(days=arrival_days)

            # If the computed arrival date is in the past, change status to 'Delivered'
            if arrival_date <= end_date:
                status = 'Delivered'
            else:
                # For shipped items with future arrival dates, set arrival_date to None
                # We'll output it as NULL in SQL
                arrival_date = None
        else:
            # Pending and cancelled orders don't have arrival dates
            arrival_date = None

        restock_orders.append({
            'RestockID': i,
            'ProductID': product_id,
            'OrderQuantity': order_quantity,
            'OrderDate': order_date.strftime('%Y-%m-%d'),
            'ArrivalDate': arrival_date.strftime('%Y-%m-%d') if arrival_date else None,
            'SupplierID': supplier_id,
            'Status': status
        })

    return restock_orders

def save_to_sql(restock_orders, output_file='restock_orders_data.sql'):
    """Save as SQL insert statements"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("USE canteen_management;\n")
        f.write("-- Bulk insert restock order data\n")
        f.write("INSERT INTO RestockOrder (ProductID, OrderQuantity, OrderDate, ArrivalDate, SupplierID, Status) VALUES\n")

        values = []
        for order in restock_orders:
            arrival_date = f"'{order['ArrivalDate']}'" if order['ArrivalDate'] else "NULL"
            value = f"({order['ProductID']}, {order['OrderQuantity']}, '{order['OrderDate']}', {arrival_date}, {order['SupplierID']}, '{order['Status']}')"
            values.append(value)

        f.write(',\n'.join(values) + ';\n')

if __name__ == "__main__":
    print("Generating restock order data...")
    restock_orders = generate_restock_orders(1000)
    save_to_sql(restock_orders)
    print(f"Successfully generated 1000 restock order data samples!")
