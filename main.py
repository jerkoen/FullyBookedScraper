import math
import time
import requests
from requests.exceptions import ChunkedEncodingError, ConnectionError
from rich import print
from pymongo import MongoClient

def safe_request(url, headers, params, retries=3, delay=5):
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            return response
        except(ChunkedEncodingError, ConnectionError) as e:
            print(f"[red]Retry {i+1}/{retries} after error: {e}[/red]")
            time.sleep(delay)
    raise Exception("Failed after retries")

client = MongoClient("mongodb://localhost:27017/")
db = client["fullybooked"]
collection = db["fave_reads"]

url = "https://fullybookedonline.com/graphql"

headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Authorization': '',
    'Referer': 'https://fullybookedonline.com/collections/featured-collections/fave-reads-under-php800.html',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'Application-Model': 'ProductList_1756123570111',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

params = {
    "hash": "1142935139",
    "sort_1": '{"bestseller_rank":"ASC"}',
    "filter_1": '{"price":{},"category_id":{"eq":27202},"customer_group_id":{"eq":"0"}}',
    "pageSize_1": "24",
    "currentPage_1": "1",
    "_currency": '""'
}

response = safe_request(url, headers, params)

data = response.json()
print(data)

total_count = data["data"]["products"]["total_count"]
page_size = int(params["pageSize_1"])
total_pages = math.ceil(total_count/page_size)

for page in range(1, total_pages + 1):
    params["currentPage_1"] = str(page)
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    for item in data["data"]["products"]["items"]:
        name = item.get("name")
        description = item.get("short_description", {}).get("html", "")
        price = item.get("price_range", {}).get("minimum_price", {}).get("final_price", {}).get("value")

        author = None
        for attr in item.get("attributes", []):
            if attr.get("attribute_code") == "author":
                author = attr.get("attribute_value")
                break
        
        book = {
            "name" : name,
            "author" : author,
            "price" : price, 
            "description" : description
        }

        print(book)
        collection.insert_one(book)

print(f"Inserted all {total_count} books into MongoDB 🎉")