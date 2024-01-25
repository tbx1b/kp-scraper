from bs4 import BeautifulSoup
import uuid
import random
import re
from fake_useragent import UserAgent

def scrape_shallow_product_info(driver, search_keyword, page_number=1):
    url = f'https://www.kupujemprodajem.com/pretraga?keywords={search_keyword}&page={page_number}'

    driver.get(url)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    ad_holders = soup.find_all('article', class_=re.compile(r'AdItem_adHolder__'))

    scraped_data = []

    for ad_holder in ad_holders:
        name = ad_holder.find('div', class_=re.compile(r'AdItem_name__\w+'))
        description = ad_holder.find('p', class_='')
        price = ad_holder.find('div', class_=re.compile(r'AdItem_price__\w+'))
        watch_count = ad_holder.find('span', class_=re.compile(r'AdItem_count__\w+'))
        location = ad_holder.find('div', class_=re.compile(r'AdItem_originAndPromoLocation__\w+')).find('p')
        created_at_match = ad_holder.find('div', class_=re.compile(r'AdItem_postedStatus__\w+')).find_all('p')
        created_at = created_at_match[1].text.strip() if len(created_at_match) > 1 else 'N/A'
        url = ad_holder.find('a', class_=re.compile(r'Link_link__\w+')).get('href')

        rd = random.Random()
        seed = name.text.strip()
        rd.seed(seed)

        if "din" in price.text.strip():
            currency = "rsd"
        else:
            currency = "eur"

        item_data = {
            "uuid": str(uuid.UUID(int=rd.getrandbits(128))),
            "name": name.text.strip() if name else 'N/A',
            "description": description.text.strip() if description else 'N/A',
            "currency": currency,
            "price": price.text.strip().replace("din", "").replace(" ", "").replace(".", "").replace("\u20ac", "") if price else 'N/A',
            "watch_count": watch_count.text.strip() if watch_count else 'N/A',
            "location": location.text.strip() if location else 'N/A',
            "created_at": created_at,
            "url": f"https://www.kupujemprodajem.com{url.split('?')[0]}",
        }

        scraped_data.append(item_data)

    return scraped_data

