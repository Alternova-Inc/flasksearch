#!/usr/bin/env python3
import random
import json
from datetime import datetime
from pathlib import Path

# Define cities with their states, zip codes, and abbreviations
cities = [
    {"name": "New York", "state": "NY", "zip": "10001", "abbreviations": ["NY", "NYC"]},
    {"name": "Los Angeles", "state": "CA", "zip": "90001", "abbreviations": ["LA"]},
    {"name": "Chicago", "state": "IL", "zip": "60601", "abbreviations": ["Chi"]},
    {"name": "Houston", "state": "TX", "zip": "77001", "abbreviations": ["Hou"]},
    {"name": "Miami", "state": "FL", "zip": "33101", "abbreviations": ["Mia"]}
]

# Define establishment types
types = ["Cafe", "Diner", "Bookstore", "Park", "Library", "Grocery", "Pharmacy", "Hardware", "Boutique", "Museum"]

# Define components for generating names
owners = ["John", "Maria", "Alex", "Sarah", "Mike", "Lisa", "David", "Emma", "Olivia", "James"]
adjectives = ["Sunny", "Cozy", "Friendly", "Classic", "Modern", "Vintage", "Green", "Blue", "Red", "Happy"]
streets = ["Main St", "Elm St", "Oak Ave", "Pine Rd", "Maple Ln", "Cedar Blvd", "Birch St", "Walnut Ave", "Chestnut Rd", "Spruce Ln"]

# Define description templates for each establishment type
description_templates = {
    "Cafe": ["A cozy spot for coffee and pastries.", "Serving artisanal coffee and fresh baked goods."],
    "Diner": ["Classic American dishes in a retro setting.", "A family-friendly place for breakfast and lunch."],
    "Bookstore": ["A wide selection of books for all ages.", "Discover your next favorite read here."],
    "Park": ["A green oasis in the city.", "Perfect for a picnic or a stroll."],
    "Library": ["A quiet place to read and learn.", "Borrow books, attend events, and more."],
    "Grocery": ["Fresh produce and everyday essentials.", "Your neighborhood market for quality goods."],
    "Pharmacy": ["Prescriptions and health products.", "Friendly service for all your pharmacy needs."],
    "Hardware": ["Tools and supplies for home improvement.", "Everything you need for DIY projects."],
    "Boutique": ["Unique clothing and accessories.", "Fashion-forward styles for every occasion."],
    "Museum": ["Exhibits on history and culture.", "Explore art and artifacts from around the world."]
}

# Initialize list to hold establishments
establishments = []
id_counter = 1

# Generate 10 establishments per city (5 cities x 10 = 50 total)
for city in cities:
    for _ in range(10):
        # Randomly select establishment type
        type_ = random.choice(types)

        # Randomly choose a name pattern
        pattern = random.choice(["adjective", "owner", "street", "city"])
        if pattern == "adjective":
            adj = random.choice(adjectives)
            name = f"{adj} {type_}"
        elif pattern == "owner":
            owner = random.choice(owners)
            name = f"{owner}'s {type_}"
        elif pattern == "street":
            street = random.choice(streets)
            name = f"{type_} on {street}"
        else:  # pattern == "city"
            name = f"{type_} in {city['name']}"

        # Generate address with random street number
        street_number = random.randint(1, 999)
        street_name = random.choice(streets)
        address = f"{street_number} {street_name}, {city['name']}, {city['state']} {city['zip']}"

        # Select a random description
        description = random.choice(description_templates[type_])

        # Set tags based on type
        tags = [type_.lower()]

        # Generate suggest_input for autocomplete, including abbreviations
        suggest_input = [name]
        if city['name'] in name:
            # If city name is in the establishment name, replace it with abbreviations
            for abbr in city['abbreviations']:
                abbreviated_name = name.replace(city['name'], abbr)
                suggest_input.append(abbreviated_name)
        else:
            # Otherwise, append abbreviations to the name
            for abbr in city['abbreviations']:
                suggest_input.append(name + " " + abbr)

        # Create establishment dictionary
        establishment = {
            "id": id_counter,
            "name": name,
            "address": address,
            "description": description,
            "tags": tags,
            "suggest_input": suggest_input
        }
        establishments.append(establishment)
        id_counter += 1

# Create data directory if it doesn't exist
data_dir = Path(__file__).parent.parent / 'data'
data_dir.mkdir(exist_ok=True)

# Generate filename with timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = data_dir / f'establishments_{timestamp}.json'

# Save the data to a JSON file
with open(output_file, "w") as f:
    json.dump(establishments, f, indent=4)

print(f"Generated 50 establishments and saved to '{output_file}'")