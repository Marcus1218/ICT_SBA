#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate 1000 sample transaction data
"""

import random
import datetime
from decimal import Decimal

def generate_transactions(num_records=1000, num_users=1000, num_octopus=1000,
                         num_staff=1000, num_promotions=1000):
    """Generate transaction data"""
    transactions = []

    # Define date range for transactions
    start_date = datetime.datetime(2023, 1, 1, 7, 0, 0)  # Start from Jan 1, 2023, 7:00 AM
    end_date = datetime.datetime(2025, 6, 8, 17, 0, 0)   # Until June 8, 2025, 5:00 PM
    date_range = (end_date - start_date).total_seconds()

    # Payment status distribution (mostly paid)
    payment_statuses = ['Paid', 'Failed', 'Refunded']
    payment_weights = [0.97, 0.02, 0.01]  # 97% paid, 2% failed, 1% refunded

    for i in range(1, num_records + 1):
        # Random user ID (some transactions might not have user record - visitors)
        user_id = random.randint(1, num_users) if random.random() < 0.8 else None

        # All transactions must have an Octopus card
        octopus_id = random.randint(1, num_octopus)

        # Most transactions processed by staff
        staff_id = random.randint(1, num_staff) if random.random() < 0.95 else None

        # Some transactions have promotions applied
        promotion_id = random.randint(1, num_promotions) if random.random() < 0.2 else None

        # Random transaction time
        random_seconds = random.randint(0, int(date_range))
        transaction_time = start_date + datetime.timedelta(seconds=random_seconds)

        # Business hours: 7:00 AM to 5:00 PM
        # If outside business hours, adjust to a random time within business hours on the same day
        if transaction_time.hour < 7 or transaction_time.hour >= 17:
            hour = random.randint(7, 16)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            transaction_time = transaction_time.replace(hour=hour, minute=minute, second=second)

        # More transactions during peak hours (lunch time: 11:30 AM to 1:30 PM)
        # If we're not already in lunch time, 60% chance to move to lunch time
        if (transaction_time.hour < 11 or transaction_time.hour > 13) and random.random() < 0.6:
            hour = random.randint(11, 13)
            transaction_time = transaction_time.replace(hour=hour)
            if hour == 13 and transaction_time.minute > 30:
                transaction_time = transaction_time.replace(minute=random.randint(0, 30))

        # Random total amount (most transactions between HK$10 and HK$100)
        if random.random() < 0.8:
            total_amount = round(Decimal(random.uniform(10.0, 100.0)), 2)
        else:
            total_amount = round(Decimal(random.uniform(5.0, 150.0)), 2)

        # Payment status
        payment_status = random.choices(payment_statuses, weights=payment_weights)[0]

        transactions.append({
            'TransactionID': i,
            'UserID': user_id,
            'OctopusID': octopus_id,
            'StaffID': staff_id,
            'PromotionID': promotion_id,
            'TransactionTime': transaction_time.strftime('%Y-%m-%d %H:%M:%S'),
            'TotalAmount': total_amount,
            'PaymentStatus': payment_status
        })

    return transactions

def save_to_sql(transactions, output_file='transactions_data.sql'):
    """Save as SQL insert statements"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("USE canteen_management;\n")
        f.write("-- Bulk insert transaction data\n")
        f.write("INSERT INTO Transaction (UserID, OctopusID, StaffID, PromotionID, TransactionTime, TotalAmount, PaymentStatus) VALUES\n")

        values = []
        for transaction in transactions:
            user_id = str(transaction['UserID']) if transaction['UserID'] else "NULL"
            staff_id = str(transaction['StaffID']) if transaction['StaffID'] else "NULL"
            promotion_id = str(transaction['PromotionID']) if transaction['PromotionID'] else "NULL"

            value = f"({user_id}, {transaction['OctopusID']}, {staff_id}, {promotion_id}, '{transaction['TransactionTime']}', {transaction['TotalAmount']}, '{transaction['PaymentStatus']}')"
            values.append(value)

        f.write(',\n'.join(values) + ';\n')

if __name__ == "__main__":
    print("Generating transaction data...")
    transactions = generate_transactions(1000)
    save_to_sql(transactions)
    print(f"Successfully generated 1000 transaction data samples!")
