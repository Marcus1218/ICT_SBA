#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate 1000 sample staff data
"""

import random
import hashlib
from faker import Faker

# Initialize Faker
fake = Faker('en_US')

def generate_staff(num_records=1000):
    """Generate staff data"""
    staff = []

    # List of possible positions
    positions = [
        "Manager", "Cashier", "Stock Keeper", "Assistant", "Supervisor",
        "Kitchen Helper", "Cleaner", "Cook", "Security", "Administrative Staff"
    ]

    for i in range(1, num_records + 1):
        name = fake.name()
        position = random.choice(positions)

        # Phone number
        contact_number = f"{random.choice(['6', '9'])}{random.randint(1000000, 9999999)}"

        # Simple password hashing for demonstration
        password = hashlib.sha256(f"password{i}".encode()).hexdigest()

        staff.append({
            'StaffID': i,
            'Name': name,
            'Position': position,
            'ContactNumber': contact_number,
            'Password': password
        })

    return staff

def save_to_sql(staff, output_file='staff_data.sql'):
    """Save as SQL insert statements"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("USE canteen_management;\n")
        f.write("-- Bulk insert staff data\n")
        f.write("INSERT INTO Staff (Name, Position, ContactNumber, Password) VALUES\n")

        values = []
        for member in staff:
            value = f"('{member['Name']}', '{member['Position']}', '{member['ContactNumber']}', '{member['Password']}')"
            values.append(value)

        f.write(',\n'.join(values) + ';\n')

if __name__ == "__main__":
    print("Generating staff data...")
    staff = generate_staff(1000)
    save_to_sql(staff)
    print(f"Successfully generated 1000 staff data samples!")
