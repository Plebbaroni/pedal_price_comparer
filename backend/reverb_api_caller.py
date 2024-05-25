import requests
import creds
import time
import csv

def get_reverb_listings(api_key, query, items_per_page, ships_to, item_region, conditions, product_type, sort, last_page, output_file):
    token = api_key

    headers = {
        'Accept-Version': '3.0',
        'Authorization': token,
        'X-Display-Currency':'PHP'
    }

    listings = []

    for page in range(1, last_page + 1):
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
                                            
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(response.text)
        else:
            data = response.json()
            listings.extend(data['listings'])
            if not getattr(response, 'from_cache', False):
                time.sleep(0.15)

    csv_columns = ["title", "price", "currency", "condition", "shipping", "region", "item_url"]

    listings.sort(key=lambda x: x.get("price", {}).get("amount", float('inf')))

    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
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

        print(f"Data has been written to {output_file}")
    except IOError as e:
        print(f"I/O error: {e}")

if __name__ == "__main__":
    get_reverb_listings(
        api_key=creds.api_key,
        query="Julia",
        items_per_page=50,
        ships_to="US_CON",
        item_region="US",
        conditions="new",
        product_type="effects-and-pedals",
        sort="price_with_sale|asc",
        last_page=10,
        output_file="reverb_listings.csv"
    )

def scrape_gcrock_pedal(url):
    pass