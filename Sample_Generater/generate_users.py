#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate 1000 sample user data
"""

import random
import datetime
from faker import Faker

# Initialize Faker, using English names
fake = Faker('en_US')

def generate_users(num_records=1000, octopus_count=1000):
    """Generate user data"""
    users = []

    # User roles and their distribution
    roles = ['Student', 'Teacher', 'Staff']
    role_weights = [0.8, 0.15, 0.05]  # 80% students, 15% teachers, 5% staff

    # Student grades
    grades = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2025, 6, 8)  # Current date
    days_range = (end_date - start_date).days

    # Create a set of already assigned OctopusIDs
    assigned_octopus_ids = set()

    for i in range(1, num_records + 1):
        name = fake.name()
        role = random.choices(roles, weights=role_weights)[0]

        # Phone number
        contact_number = f"9{random.randint(1000000, 9999999)}"

        # Email address
        email = f"{fake.user_name()}@{'school' if role in ['Student', 'Teacher'] else 'staff'}.edu.hk"

        # Grade - only applicable to students
        grade = random.choice(grades) if role == 'Student' else None

        # Assign Octopus ID - ensure no duplicates
        while True:
            octopus_id = random.randint(1, octopus_count)
            if octopus_id not in assigned_octopus_ids:
                assigned_octopus_ids.add(octopus_id)
                break

        # Random join date
        random_days = random.randint(0, days_range)
        join_date = start_date + datetime.timedelta(days=random_days)

        users.append({
            'UserID': i,  # Auto-incrementing ID
            'Name': name,
            'Role': role,
            'ContactNumber': contact_number,
            'Email': email,
            'Grade': grade,
            'OctopusID': octopus_id,
            'JoinDate': join_date.strftime('%Y-%m-%d')
        })

    return users

def save_to_sql(users, output_file='users_data.sql'):
    """Save as SQL insert statements"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("USE canteen_management;\n")
        f.write("-- Bulk insert user data\n")
        f.write("INSERT INTO User (Name, Role, ContactNumber, Email, Grade, OctopusID, JoinDate) VALUES\n")

        values = []
        for user in users:
            grade_value = f"'{user['Grade']}'" if user['Grade'] else "NULL"
            value = f"('{user['Name']}', '{user['Role']}', '{user['ContactNumber']}', '{user['Email']}', {grade_value}, {user['OctopusID']}, '{user['JoinDate']}')"
            values.append(value)

        f.write(',\n'.join(values) + ';\n')

if __name__ == "__main__":
    print("Generating user data...")
    users = generate_users(1000)
    save_to_sql(users)
    print(f"Successfully generated 1000 user data samples!")
