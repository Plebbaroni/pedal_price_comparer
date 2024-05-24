import requests
import creds
import time
import csv

token = creds.api_key;

headers = {
    'Accept-Version': '3.0',
    'Authorization': token,
    'X-Display-Currency':'PHP'
}

query = "Julia"
items_per_page = 50
ships_to = "US_CON"
item_region = "US"
conditions = "new"
product_type = "effects-and-pedals"
sort = "price_with_sale|asc"
page = 1
last_page = 10

listings = []

for page in range (1, last_page + 1):
    url = 'https://api.reverb.com/api/listings/?'\
                    'query={}&'\
                    'per_page={}&'\
                    'ships_to={}&'\
                    'product_type={}&'\
                    'condition={}&'\
                    'item_region={}&'\
                    'sort={}&'\
                    'page={}'.format(query, items_per_page, ships_to, product_type,
                                        conditions, item_region, sort, page)
                                        
    response = requests.get(url, headers=headers);

    if response.status_code != 200:
        print(response.text)
    else:
        data = response.json();
        listings.extend(data['listings'])
        if not getattr(response, 'from_cache', False):
            time.sleep(0.15)

# Define the CSV file structure
csv_file = "reverb_listings.csv"
csv_columns = ["title", "price", "currency", "condition", "shipping", "region", "item_url"]

# Open the CSV file and write the data
listings.sort(key=lambda x: x.get("price", {}).get("amount", float('inf')))

try:
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()

        for item in listings:
            writer.writerow({
                "title": item.get("title"),
                "price": item.get("price", {}).get("amount"),
                "currency": item.get("price", {}).get("currency"),
                "condition": item.get("condition"),
                "shipping": item.get("shipping", {}).get("cost", {}).get("amount"),
                "region": item.get("item_region"),
                "item_url": item.get("_links", {}).get("web", {}).get("href")
            })

    print(f"Data has been written to {csv_file}")
except IOError as e:
    print(f"I/O error: {e}")