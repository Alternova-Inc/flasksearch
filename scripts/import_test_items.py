#!/usr/bin/env python3
"""
Script to import test establishments into Elasticsearch using the API endpoint.
This script uses the items PUT endpoint to import all items from the test data.
"""

import json
import requests
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Load environment variables
load_dotenv()

def import_item(item, api_token, base_url):
    """Import a single item using the PUT endpoint."""
    headers = {
        'Content-Type': 'application/json',
        'X-API-Token': api_token
    }
    
    response = requests.put(
        f"{base_url}/api/v1/items",
        headers=headers,
        json=item
    )
    
    return {
        'id': item['id'],
        'status': response.status_code,
        'response': response.json() if response.content else None
    }

def main():
    """Main function to import all items."""
    # Load configuration
    api_token = os.getenv('API_TOKEN')
    base_url = os.getenv('API_URL', 'http://localhost:5001')
    
    if not api_token:
        print("Error: API_TOKEN not found in environment variables")
        return

    # Load test establishments
    try:
        with open('data/test_establishments.json', 'r') as f:
            items = json.load(f)
    except FileNotFoundError:
        print("Error: test_establishments.json not found in data directory")
        return
    
    print(f"Found {len(items)} items to import")
    
    # Import items using thread pool for parallel processing
    results = []
    failed = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(import_item, item, api_token, base_url)
            for item in items
        ]
        
        # Process results with progress bar
        for future in tqdm(futures, desc="Importing items"):
            result = future.result()
            results.append(result)
            if result['status'] != 200:
                failed.append(result)
    
    # Print summary
    success_count = len([r for r in results if r['status'] == 200])
    print(f"\nImport completed:")
    print(f"- Successfully imported: {success_count}/{len(items)} items")
    
    if failed:
        print("\nFailed imports:")
        for fail in failed:
            print(f"- Item {fail['id']}: Status {fail['status']}")
            if fail['response']:
                print(f"  Error: {fail['response'].get('error', 'Unknown error')}")

if __name__ == '__main__':
    main() 