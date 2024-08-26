import pandas as pd
import random
from faker import Faker
from datetime import datetime

# Initialize Faker
fake = Faker('en_CA')

# Create a list of fixed cities and their postcodes in Ontario
cities_and_postcodes = {
    "Toronto": ["M1B 0A1", "M2B 0A2", "M3B 0A3", "M4B 0A4", "M5B 0A5"],
    "Ottawa": ["K1A 0B1", "K1B 0B2", "K1C 0B3", "K1D 0B4", "K1E 0B5"],
    "Mississauga": ["L1A 0C1", "L1B 0C2", "L1C 0C3", "L1D 0C4", "L1E 0C5"],
    "Brampton": ["L2A 0D1", "L2B 0D2", "L2C 0D3", "L2D 0D4", "L2E 0D5"],
    "Hamilton": ["L3A 0E1", "L3B 0E2", "L3C 0E3", "L3D 0E4", "L3E 0E5"],
    "London": ["N4A 0F1", "N4B 0F2", "N4C 0F3", "N4D 0F4", "N4E 0F5"],
    "Markham": ["L5A 0G1", "L5B 0G2", "L5C 0G3", "L5D 0G4", "L5E 0G5"],
    "Vaughan": ["L6A 0H1", "L6B 0H2", "L6C 0H3", "L6D 0H4", "L6E 0H5"],
    "Kitchener": ["N2A 0I1", "N2B 0I2", "N2C 0I3", "N2D 0I4", "N2E 0I5"],
    "Windsor": ["N8A 0J1", "N8B 0J2", "N8C 0J3", "N8D 0J4", "N8E 0J5"]
}

# Create a list of fixed categories with associated price and quantity ranges
categories_with_details = {
    1: {"price_range": (2.99, 10.99), "quantity_range": (1, 3)},  # Bakery products
    2: {"price_range": (3.99, 6.99), "quantity_range": (1, 2)},   # Butter
    3: {"price_range": (1.99, 6.99), "quantity_range": (1, 3)},   # Canned vegetables and other vegetable preparations
    4: {"price_range": (4.99, 9.99), "quantity_range": (1, 3)},   # Cheese
    5: {"price_range": (2.99, 10.99), "quantity_range": (1, 3)},  # Coffee and tea
    6: {"price_range": (3.99, 12.99), "quantity_range": (1, 5)},  # Condiments, spices and vinegars
    7: {"price_range": (2.99, 13.99), "quantity_range": (1, 5)},  # Cookies and crackers
    8: {"price_range": (5.89, 12.99), "quantity_range": (1, 2)},  # Dairy products and eggs
    9: {"price_range": (3.79, 13.99), "quantity_range": (1, 2)},  # Eggs
    10: {"price_range": (5.00, 6.00), "quantity_range": (1, 3)},  # Flour and flour-based mixes
    11: {"price_range": (3.00, 15.99), "quantity_range": (1, 5)}, # Fresh fruit
    12: {"price_range": (5.99, 11.99), "quantity_range": (1, 5)}, # Fresh or frozen meat (excluding poultry)
    13: {"price_range": (1.99, 13.00), "quantity_range": (1, 5)}, # Fresh vegetables
    14: {"price_range": (5.99, 11.99), "quantity_range": (1, 5)}, # Frozen and dried vegetables
    15: {"price_range": (3.99, 12.99), "quantity_range": (1, 10)},# Fruit, fruit preparations and nuts
    16: {"price_range": (1.99, 6.99), "quantity_range": (1, 3)},  # Margarine
    17: {"price_range": (10.00, 45.99), "quantity_range": (1, 2)},# Meat
    18: {"price_range": (3.00, 15.99), "quantity_range": (1, 5)}, # Non-alcoholic beverages
    19: {"price_range": (2.20, 5.00), "quantity_range": (1, 5)},  # Nuts and seeds
    20: {"price_range": (2.99, 11.99), "quantity_range": (1, 8)}, # Other bakery products
    21: {"price_range": (2.50, 5.99), "quantity_range": (1, 5)},  # Other dairy products
    22: {"price_range": (2.99, 12.99), "quantity_range": (1, 3)}, # Other food preparations
    23: {"price_range": (2.99, 12.99), "quantity_range": (1, 3)}, # Other food products and non-alcoholic beverages
    24: {"price_range": (9.20, 12.00), "quantity_range": (1, 3)}, # Other fresh or frozen meat (excluding poultry)
    25: {"price_range": (2.99, 15.00), "quantity_range": (1, 5)}, # Other preserved fruit and fruit preparations
    26: {"price_range": (15.00, 20.00), "quantity_range": (1, 2)},# Other processed meat
    27: {"price_range": (5.50, 8.00), "quantity_range": (1, 3)},  # Pasta products
    28: {"price_range": (2.00, 15.00), "quantity_range": (1, 5)}, # Preserved fruit and fruit preparations
    29: {"price_range": (15.00, 20.00), "quantity_range": (1, 2)},# Processed meat
    30: {"price_range": (20.00, 40.00), "quantity_range": (1, 2)},# Seafood and other marine products
    31: {"price_range": (3.50, 7.00), "quantity_range": (1, 3)},  # Sugar and confectionery
    32: {"price_range": (1.99, 12.99), "quantity_range": (1, 3)}  # Vegetables and vegetable preparations
}

# Date range for purchases
date_range = pd.date_range(start='2011-01-01', end='2021-12-31')

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

for _ in range(6000):
    # Random date of purchase
    date_of_purchase = random.choice(date_range)
    
    # Random time of purchase between 10:00 and 22:00
    hour = random.randint(10, 21)  # Random hour between 10 and 21 (inclusive)
    minute = random.randint(0, 59)  # Random minute between 0 and 59 (inclusive)
    second = random.randint(0, 59)  # Random second between 0 and 59 (inclusive)
    
    # Set the time on the date
    date_of_purchase = date_of_purchase.replace(hour=hour, minute=minute, second=second)
    
    dates_of_purchase.append(date_of_purchase)

    # Unique Order ID based on date of purchase and a random unique identifier
    order_id = f"{date_of_purchase.strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
    order_ids.append(order_id)

    # Choose a random city
    city = random.choice(list(cities_and_postcodes.keys()))
    # Select a random postcode for the chosen city
    postcode = random.choice(cities_and_postcodes[city])  
    
    # Random branch address
    address = f"{random.randint(1, 999)} {fake.street_name()}, {city}, ON, {postcode}"
    branch_addresses.append(address)
    cities.append(city)
    postcodes.append(postcode)
    
    # Product category, price range, and quantity range
    category_id = random.choice(list(categories_with_details.keys()))
    details = categories_with_details[category_id]
    price_range = details["price_range"]
    quantity_range = details["quantity_range"]
    
    # Calculate the year difference from 2011 and apply price increase
    year_diff = date_of_purchase.year - 2011
    price_increase_factor = 1 + (0.02 * year_diff)  # 2% increase per year
    
    if (category_id, date_of_purchase.date()) not in price_cache:
        base_price = round(random.uniform(price_range[0], price_range[1]), 2)
        adjusted_price = round(base_price * price_increase_factor, 2)
        price_cache[(category_id, date_of_purchase.date())] = adjusted_price
    else:
        adjusted_price = price_cache[(category_id, date_of_purchase.date())]
    
    product_ids.append(fake.uuid4())
    product_categories.append(category_id)
    quantities.append(random.randint(quantity_range[0], quantity_range[1]))
    prices.append(adjusted_price)
    payment_methods.append(random.choice(["Cash", "Credit Card", "Debit Card"]))
    
    # Generate a 16-digit Customer ID that may duplicate across different dates of purchase or be null
    if random.random() < 0.1:  # 10% chance of a null Customer ID
        customer_id = None
    elif existing_customer_ids and random.random() < 0.3:  # 30% chance to reuse an existing customer ID
        customer_id = random.choice(existing_customer_ids)
    else:
        customer_id = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        existing_customer_ids.append(customer_id)
    customer_ids.append(customer_id)

# Create the DataFrame
data = {
    "date": dates_of_purchase,
    "order_id": order_ids,
    "branch_address": branch_addresses,
    "city": cities,
    "province": ["Ontario"] * 6000,
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
df.to_excel(file_path, index=False)
file_path
