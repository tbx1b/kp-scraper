import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import uuid
import random
import re
import datetime
import sys

def scrape_shallow_product_info(search_keyword, page_number=1):
    chrome_driver_path = ChromeDriverManager().install()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=ChromeService(chrome_driver_path), options=chrome_options)

    url = f'https://www.kupujemprodajem.com/pretraga?keywords={search_keyword}&page={page_number}'
    driver.get(url)

    page_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')

    ad_holders = soup.find_all('article', class_=re.compile(r'AdItem_adHolder__'))

    scraped_data = []

    for ad_holder in ad_holders:
        name = ad_holder.find('div', class_=re.compile(r'AdItem_name__\w+'))
        description = ad_holder.find('p', class_='')
        price = ad_holder.find('div', class_=re.compile(r'AdItem_price__\w+'))
        watch_count = ad_holder.find('span', class_=re.compile(r'AdItem_count__\w+'))
        favorite_count = ad_holder.find('span', class_=re.compile(r'AdItem_count__\w+'))
        location = ad_holder.find('div', class_=re.compile(r'AdItem_originAndPromoLocation__\w+')).find('p')

        rd = random.Random()
        seed = name.text.strip()
        rd.seed(seed)

        if "din" in price.text.strip():
            currency = "rsd"
        else:
            currency = "eur"

        item_data = {
            "uuid": str(uuid.UUID(int=rd.getrandbits(128))),
            "gold": "false",
            "name": name.text.strip() if name else 'N/A',
            "description": description.text.strip() if description else 'N/A',
            "currency": currency,
            "price": price.text.strip().replace("din", "").replace(" ", "").replace(".", "").replace("\u20ac", "") if price else 'N/A',
            "watch_count": watch_count.text.strip() if watch_count else 'N/A',
            "location": location.text.strip() if location else 'N/A',
        }

        scraped_data.append(item_data)

    json_data = json.dumps(scraped_data, indent=2)

    return json_data

keyword = sys.argv[2] if len(sys.argv) > 1 else "mikrofon"
pages = int(sys.argv[4]) if len(sys.argv) > 2 else 1

print(f"Scraping {pages} pages under the keyword '{keyword}'")

output = ""

pages_scraped = 0

start_time = datetime.datetime.now()
for i in range(0, pages):
    output = output + scrape_shallow_product_info(keyword, i)
    pages_scraped = pages_scraped + 1
end_time = datetime.datetime.now()

print(output)

print("--------------------------------")
print(f'Pages scraped: {pages_scraped}')
print(f'Listings scraped: {output.count("uuid")}')
print(f'Time taken: {end_time - start_time}')

with open(f'output/output-{keyword}-{datetime.datetime.now()}.txt', "w") as file:
    file.write(output)