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
conditions = ["mint", "new"]
sort = "price_with_sale%7Casc"

url = url = 'https://api.reverb.com/api/listings/?'\
                'query={}&'\
                'per_page={}&'\
                'ships_to={}&'\
                'condition={}&'\
                'condition={}&'\
                'item_region={}'.format(query, items_per_page, ships_to,
                                      conditions[1], conditions[0], item_region)
response = requests.get(url, headers=headers);

if response.status_code != 200:
    print(response.text)
else:
    data = response.json();
    if not getattr(response, 'from_cache', False):
        time.sleep(0.15)

    # Define the CSV file structure
    csv_file = "reverb_listings.csv"
    csv_columns = ["title", "price", "currency", "condition", "shipping", "region", "item_url"]

    # Open the CSV file and write the data
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writeheader()

            for item in data['listings']:
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