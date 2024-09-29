import pandas as pd
import random
from faker import Faker
from datetime import datetime

# Initialize Faker
fake = Faker('en_CA')

# Create a list of fixed cities and their postcodes in Ontario (removed "Ottawa" and "Brampton")
cities_and_postcodes = {
    "Toronto": ["M1B 0A1", "M2B 0A2", "M3B 0A3", "M4B 0A4", "M5B 0A5"],
    "Mississauga": ["L1A 0C1", "L1B 0C2", "L1C 0C3", "L1D 0C4", "L1E 0C5"],
    "Markham": ["L5A 0G1", "L5B 0G2", "L5C 0G3", "L5D 0G4", "L5E 0G5"],
    "Vaughan": ["L6A 0H1", "L6B 0H2", "L6C 0H3", "L6D 0H4", "L6E 0H5"]
}

# Define multipliers for each city
city_multipliers = {
    "Toronto": {"quantity_multiplier": 2, "price_multiplier": 1.7},
    "Markham": {"quantity_multiplier": 1.8, "price_multiplier": 1.6},
    "Vaughan": {"quantity_multiplier": 1.6, "price_multiplier": 1.5},
    "Mississauga": {"quantity_multiplier": 0.9, "price_multiplier": 0.7},
}

# For other cities, lower multipliers (default small sales)
default_quantity_multiplier = 0.7
default_price_multiplier = 0.4

# Create a list of fixed categories with associated price and quantity ranges
categories_with_details = {
    1: {"price_range": (3.00, 9.99), "quantity_range": (1, 3)},  # Bakery products
    2: {"price_range": (2.00, 9.00), "quantity_range": (1, 2)},   # Butter
    3: {"price_range": (1.99, 6.99), "quantity_range": (1, 3)},   # Canned vegetables and other vegetable preparations
    4: {"price_range": (2.00, 8.00), "quantity_range": (1, 3)},   # Cheese
    5: {"price_range": (1.99, 7.99), "quantity_range": (1, 3)},  # Coffee and tea
    6: {"price_range": (3.99, 10.99), "quantity_range": (1, 5)},  # Condiments, spices and vinegars
    7: {"price_range": (2.99, 7.99), "quantity_range": (1, 5)},  # Cookies and crackers
    8: {"price_range": (3.50, 12.99), "quantity_range": (1, 2)},  # Dairy products and eggs
    9: {"price_range": (3.79, 13.99), "quantity_range": (1, 2)},  # Eggs
    10: {"price_range": (5.00, 6.00), "quantity_range": (1, 3)},  # Flour and flour-based mixes
    11: {"price_range": (3.00, 8.99), "quantity_range": (1, 5)}, # Fresh fruit
    12: {"price_range": (5.99, 13.99), "quantity_range": (1, 5)}, # Fresh or frozen meat (excluding poultry)
    13: {"price_range": (1.99, 5.00), "quantity_range": (1, 5)}, # Fresh vegetables
    14: {"price_range": (5.99, 11.99), "quantity_range": (1, 5)}, # Frozen and dried vegetables
    15: {"price_range": (3.99, 7.99), "quantity_range": (1, 10)},# Fruit, fruit preparations and nuts
    16: {"price_range": (1.99, 6.99), "quantity_range": (1, 3)},  # Margarine
    17: {"price_range": (10.00, 30.99), "quantity_range": (1, 2)},# Meat
    18: {"price_range": (3.00, 15.99), "quantity_range": (1, 5)}, # Non-alcoholic beverages
    19: {"price_range": (2.20, 5.00), "quantity_range": (1, 5)},  # Nuts and seeds
    20: {"price_range": (2.99, 10.99), "quantity_range": (1, 8)}, # Other bakery products
    21: {"price_range": (2.50, 5.99), "quantity_range": (1, 5)},  # Other dairy products
    22: {"price_range": (2.99, 12.99), "quantity_range": (1, 3)}, # Other food preparations
    23: {"price_range": (2.99, 12.99), "quantity_range": (1, 3)}, # Other food products and non-alcoholic beverages
    24: {"price_range": (9.20, 12.00), "quantity_range": (1, 3)}, # Other fresh or frozen meat (excluding poultry)
    25: {"price_range": (2.99, 15.00), "quantity_range": (1, 5)}, # Other preserved fruit and fruit preparations
    26: {"price_range": (15.00, 20.00), "quantity_range": (1, 2)},# Other processed meat
    27: {"price_range": (5.50, 8.00), "quantity_range": (1, 3)},  # Pasta products
    28: {"price_range": (2.00, 15.00), "quantity_range": (1, 5)}, # Preserved fruit and fruit preparations
    29: {"price_range": (15.00, 20.00), "quantity_range": (1, 2)},# Processed meat
    30: {"price_range": (20.00, 30.00), "quantity_range": (1, 2)},# Seafood and other marine products
    31: {"price_range": (3.50, 7.00), "quantity_range": (1, 3)},  # Sugar and confectionery
    32: {"price_range": (1.99, 12.99), "quantity_range": (1, 3)}  # Vegetables and vegetable preparations
}

# Adjusted payment method proportions
payment_methods_weights = {
    "Credit Card": 0.5,  # 50% chance for Credit Card
    "Debit Card": 0.3,   # 30% chance for Debit Card
    "Cash": 0.2          # 20% chance for Cash
}

# Payment method price adjustment
payment_method_price_adjustments = {
    "Credit Card": 1.2,  # Increase price by 20% for Credit Card
    "Debit Card": 1.1,   # Increase price by 10% for Debit Card
    "Cash": 0.8          # Decrease price by 20% for Cash
}

# Set payment method proportions that change over time, with increasing credit card and debit card usage
def get_payment_method_weights(year):
    # Initial weights for 2014
    credit_card_weight = 0.3
    debit_card_weight = 0.2
    cash_weight = 0.5

    # Each year, decrease the cash usage and increase credit card and debit card usage
    year_diff = year - 2014
    # Every year, increase credit card and debit card by 2% and decrease cash by 4%
    credit_card_weight += 0.02 * year_diff
    debit_card_weight += 0.02 * year_diff
    cash_weight -= 0.04 * year_diff

    # Ensure the total weight doesn't exceed 1
    if credit_card_weight + debit_card_weight > 1:
        credit_card_weight = 0.5
        debit_card_weight = 0.4
        cash_weight = 0.1

    return [credit_card_weight, debit_card_weight, cash_weight]


# Generate data for the revised year range
years = list(range(2014, 2025))
months = list(range(1, 13))  # 1-12 for January to December

## Define a multiplier for the COVID-19 period (2020 to Jan 2023)
covid_transaction_multiplier = 1.5  # Increase transactions by 50%

# Gradual post-COVID drop for transactions (Feb 2023 onward), reducing by 1-3% per month
def get_post_covid_transaction_multiplier(year, month):
    if year == 2023 and month >= 2:
        # Gradual decrease post-COVID (1-3% decrease per month)
        months_after_covid = (year - 2023) * 12 + (month - 2)
        # Ensure we don't go below the pre-pandemic normal levels
        return max(1 - (months_after_covid * 0.03), 1)  # Decrease by up to 3% per month, but never below 1x normal
    return 1  # No adjustment before Feb 2023

# Generate mock data
dates_of_purchase = []
order_ids = []
branch_addresses = []
cities = []
postcodes = []
product_ids = []
product_categories = []
customer_ids = []
quantities = []
prices = []
payment_methods = []

price_cache = {}
existing_customer_ids = []

# Adjust the section where transactions are generated
for city, postcodes_list in cities_and_postcodes.items():
    for year in years:
        for month in months:
            for category_id in categories_with_details.keys():  # Ensure each product category is represented
                
                # Determine if the current year and month fall within the COVID period (Jan 2020 to Jan 2023)
                if (year == 2020 and month >= 1) or (year == 2021) or (year == 2022) or (year == 2023 and month == 1):
                    # Apply multiplier for COVID-19 period
                    num_transactions = int(random.randint(5, 10) * covid_transaction_multiplier)
                elif year == 2023 and month >= 2:
                    # Apply post-COVID gradual reduction with a 1-3% decrease per month
                    post_covid_multiplier = get_post_covid_transaction_multiplier(year, month)
                    num_transactions = int(random.randint(5, 10) * post_covid_multiplier)
                else:
                    # Stable range before COVID-19 (normal transaction volume)
                    num_transactions = random.randint(5, 10)  # Default number of transactions
                
                for _ in range(num_transactions):
                    # Create a random date
                    day = random.randint(1, 28)  # Restrict to 28 days to avoid February issues
                    hour = random.randint(10, 21)  # Hours between 10:00 and 21:00
                    minute = random.randint(0, 59)
                    second = random.randint(0, 59)

                    date_of_purchase = datetime(year, month, day, hour, minute, second)
                    dates_of_purchase.append(date_of_purchase)

                    # Unique order ID
                    order_id = f"{date_of_purchase.strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
                    order_ids.append(order_id)

                    # Select a random branch address and postcode
                    postcode = random.choice(postcodes_list)
                    address = f"{random.randint(1, 999)} {fake.street_name()}, {city}, ON, {postcode}"
                    branch_addresses.append(address)
                    cities.append(city)
                    postcodes.append(postcode)

                    # Product category and price range
                    details = categories_with_details[category_id]
                    price_range = details["price_range"]
                    quantity_range = details["quantity_range"]

                    # Calculate price increase factor based on year
                    year_diff = year - 2014
                    price_increase_factor = 1 + (0.02 * year_diff)

                    # City-specific price and quantity multipliers
                    city_multiplier = city_multipliers.get(city, {
                        "price_multiplier": default_price_multiplier,
                        "quantity_multiplier": default_quantity_multiplier
                    })

                    price_multiplier = city_multiplier["price_multiplier"]
                    quantity_multiplier = city_multiplier["quantity_multiplier"]

                    # Calculate base price
                    base_price = round(random.uniform(price_range[0], price_range[1]), 2)

                    # Adjust payment method proportions based on the year
                    payment_weights = get_payment_method_weights(year)
                    payment_method = random.choices(
                        population=["Credit Card", "Debit Card", "Cash"],
                        weights=payment_weights,
                        k=1
                    )[0]
                    payment_methods.append(payment_method)

                    # Apply price adjustment based on payment method
                    payment_adjustment_factor = payment_method_price_adjustments[payment_method]

                    # Calculate adjusted price
                    adjusted_price = round(base_price * price_increase_factor * price_multiplier * payment_adjustment_factor, 2)
                    adjusted_price = min(max(adjusted_price, price_range[0]), price_range[1])

                    # Adjust quantity based on city multiplier
                    quantity = random.randint(quantity_range[0], quantity_range[1])
                    adjusted_quantity = round(quantity * quantity_multiplier)

                    # Append data
                    product_ids.append(fake.uuid4())
                    product_categories.append(category_id)
                    quantities.append(adjusted_quantity)
                    prices.append(adjusted_price)

                    # Customer ID logic (unchanged)
                    if random.random() < 0.1:  # 10% chance of being None
                        customer_id = None
                    elif existing_customer_ids and random.random() < 0.3:  # 30% chance to reuse an existing customer ID
                        customer_id = random.choice(existing_customer_ids)
                    else:
                        customer_id = ''.join([str(random.randint(0, 9)) for _ in range(16)])
                        existing_customer_ids.append(customer_id)
                    customer_ids.append(customer_id)

# Create DataFrame
data = {
    "date": dates_of_purchase,
    "order_id": order_ids,
    "branch_address": branch_addresses,
    "city": cities,
    "province": ["Ontario"] * len(order_ids),
    "postcode": postcodes,
    "product_id": product_ids,
    "product_categories_id": product_categories,
    "customer_id": customer_ids,
    "quantities": quantities,
    "prices": prices,
    "payment_methods": payment_methods
}
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
file_path = r'C:\Users\Vincent\Desktop\Ontario Supermarket Purchases.xlsx'
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Supermarket_Detail', index=False)
file_path
