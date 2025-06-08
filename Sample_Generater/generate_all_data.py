#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Master script to generate 1000 sample data rows for all tables in the canteen management database.
This script runs all individual data generation scripts in the correct order to maintain referential integrity.
"""

import os
import subprocess
import sys
import time

def run_script(script_name, description):
    """Run a Python script and display its output"""
    print(f"\n{'=' * 80}")
    print(f"Running: {script_name} - {description}")
    print(f"{'=' * 80}")

    # Check if the script exists
    if not os.path.exists(script_name):
        print(f"Error: Script {script_name} not found!")
        return False

    # Run the script and capture output
    try:
        result = subprocess.run([sys.executable, script_name],
                               capture_output=True,
                               text=True,
                               check=True)
        print(result.stdout)
        if result.stderr:
            print(f"Warnings/Errors: {result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}:")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    """Main function to run all data generation scripts in the correct order"""
    start_time = time.time()

    # Define scripts to run in order (to maintain referential integrity)
    # The order is critical to avoid foreign key constraint failures
    scripts = [
        ("generate_octopus_cards.py", "Generate Octopus Cards"),
        ("generate_suppliers.py", "Generate Suppliers"),
        ("generate_staff.py", "Generate Staff"),
        ("generate_users.py", "Generate Users"),
        ("generate_products.py", "Generate Products"),
        ("generate_promotions.py", "Generate Promotions"),
        ("generate_promotion_products.py", "Generate Promotion-Product Relationships"),
        ("generate_transactions.py", "Generate Transactions"),
        ("generate_transaction_details.py", "Generate Transaction Details"),
        ("generate_restock_orders.py", "Generate Restock Orders")
    ]

    # Track successful and failed scripts
    successful = []
    failed = []

    # Run each script
    for script_name, description in scripts:
        if run_script(script_name, description):
            successful.append(script_name)
        else:
            failed.append(script_name)
            # If a script fails, stop execution as subsequent scripts may depend on its data
            print(f"Script {script_name} failed. Stopping execution to prevent cascade failures.")
            break

    # Display summary
    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n{'=' * 80}")
    print(f"DATA GENERATION SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Scripts executed: {len(successful) + len(failed)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")

    if failed:
        print("\nFailed scripts:")
        for script in failed:
            print(f"  - {script}")

    print("\nTo use the generated SQL files, you must run them in this order:")
    for i, (script, _) in enumerate(scripts):
        sql_file = script.replace('.py', '_data.sql')
        print(f"{i+1}. {sql_file}")

    print("\nThis ensures that foreign key constraints are respected.")

if __name__ == "__main__":
    main()
