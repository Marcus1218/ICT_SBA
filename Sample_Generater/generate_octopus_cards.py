#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate 1000 sample Octopus card data
"""

import random
import datetime
from decimal import Decimal

def generate_card_number():
    """Generate a 16-digit card number"""
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])

def generate_octopus_cards(num_records=1000):
    """Generate Octopus card data"""
    octopus_cards = []

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2025, 6, 8)  # Current date
    days_range = (end_date - start_date).days

    for i in range(1, num_records + 1):
        card_number = generate_card_number()
        balance = round(Decimal(random.uniform(0, 500)), 2)  # Balance between 0 and 500

        # Random registration date
        random_days = random.randint(0, days_range)
        registration_date = start_date + datetime.timedelta(days=random_days)

        octopus_cards.append({
            'OctopusID': i,  # Auto-incrementing ID
            'CardNumber': card_number,
            'Balance': balance,
            'RegistrationDate': registration_date.strftime('%Y-%m-%d')
        })

    return octopus_cards

def save_to_sql(octopus_cards, output_file='octopus_cards_data.sql'):
    """Save as SQL insert statements"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("USE canteen_management;\n")
        f.write("-- Bulk insert Octopus card data\n")
        f.write("INSERT INTO OctopusCard (CardNumber, Balance, RegistrationDate) VALUES\n")

        values = []
        for card in octopus_cards:
            value = f"('{card['CardNumber']}', {card['Balance']}, '{card['RegistrationDate']}')"
            values.append(value)

        f.write(',\n'.join(values) + ';\n')

if __name__ == "__main__":
    octopus_cards = generate_octopus_cards(1000)
    save_to_sql(octopus_cards)
    print(f"Successfully generated 1000 Octopus card data samples!")
