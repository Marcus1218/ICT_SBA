#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate 1000 sample supplier data
"""

import random
from faker import Faker

# Initialize Faker
fake = Faker('en_US')

def generate_suppliers(num_records=1000):
    """Generate supplier data"""
    suppliers = []

    # Business types for company name generation
    business_types = [
        "Foods", "Beverages", "Bakery", "Dairy", "Snacks", "Fruits",
        "Vegetables", "Grocery", "Confectionery", "Organic Products"
    ]

    # Business suffixes
    suffixes = [
        "Co., Ltd.", "Limited", "Inc.", "Group", "Corporation", "Enterprises",
        "Industries", "Company", "Wholesalers", "Distributors", "Suppliers"
    ]

    for i in range(1, num_records + 1):
        # Generate company name
        company_type = random.choice(business_types)
        company_suffix = random.choice(suffixes)
        company_name = f"{fake.last_name()} {company_type} {company_suffix}"

        # Generate contact person
        contact_person = fake.name()

        # Generate phone number
        phone = f"{random.choice(['2', '3'])}{random.randint(1000000, 9999999)}"

        # Generate email
        company_prefix = ''.join(company_name.lower().split()[:2])
        email = f"contact@{company_prefix.replace(' ', '')}.com"

        # Generate address
        address = fake.address().replace('\n', ', ')

        suppliers.append({
            'SupplierID': i,
            'CompanyName': company_name,
            'ContactPerson': contact_person,
            'Phone': phone,
            'Email': email,
            'Address': address
        })

    return suppliers

def save_to_sql(suppliers, output_file='suppliers_data.sql'):
    """Save as SQL insert statements"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("USE canteen_management;\n")
        f.write("-- Bulk insert supplier data\n")
        f.write("INSERT INTO Supplier (CompanyName, ContactPerson, Phone, Email, Address) VALUES\n")

        values = []
        for supplier in suppliers:
            # Escape single quotes in strings
            company_name = supplier['CompanyName'].replace("'", "''")
            contact_person = supplier['ContactPerson'].replace("'", "''")
            address = supplier['Address'].replace("'", "''")
            email = supplier['Email'].replace("'", "''")

            value = f"('{company_name}', '{contact_person}', '{supplier['Phone']}', '{email}', '{address}')"
            values.append(value)

        f.write(',\n'.join(values) + ';\n')

if __name__ == "__main__":
    print("Generating supplier data...")
    suppliers = generate_suppliers(1000)
    save_to_sql(suppliers)
    print(f"Successfully generated 1000 supplier data samples!")
