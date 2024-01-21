import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import uuid
import random
import re

def scrape_product_info_selenium(url):
    chrome_driver_path = ChromeDriverManager().install()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=ChromeService(chrome_driver_path), options=chrome_options)

    driver.get(url)

    page_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')

    ad_holders = soup.find_all('article', class_=re.compile(r'AdItem_adHolder__'))

    scraped_data = []

    for ad_holder in ad_holders:

        # Get the actual data from the webpage
        name = ad_holder.find('div', class_=re.compile(r'AdItem_name__\w+'))
        description = ad_holder.find('p', class_='')
        price = ad_holder.find('div', class_=re.compile(r'AdItem_price__\w+'))
        watch_count = ad_holder.find('span', class_=re.compile(r'AdItem_count__\w+'))
        location = ad_holder.find('div', class_=re.compile(r'AdItem_originAndPromoLocation__\w+')).find('p')

        # So each listing can have our own unique identifier
        rd = random.Random()
        seed = name.text.strip()

        rd.seed(seed)

        item_data = {
            "uuid": str(uuid.UUID(int=rd.getrandbits(128))),
            "gold": "false",
            "name": name.text.strip() if name else 'N/A',
            "description": description.text.strip() if description else 'N/A',
            "price": price.text.strip() if price else 'N/A',
            "watch_count": watch_count.text.strip() if watch_count else 'N/A',
            # "favorite_count": favorite_count.text.strip() if favorite_count else 'N/A',
            "location": location.text.strip() if location else 'N/A',
        }

        scraped_data.append(item_data)

    json_data = json.dumps(scraped_data, indent=2)

    print(json_data)

kp = 'https://www.kupujemprodajem.com/pretraga?keywords=zvucnjak&page=1'
scrape_product_info_selenium(kp)
