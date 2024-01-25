import sys
import datetime
from tqdm import tqdm
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from src.scraper import scrape_shallow_product_info
from src.utils import get_random_user_agent

def main():
    keyword = sys.argv[2] if len(sys.argv) > 1 else "mikrofon"
    pages = int(sys.argv[4]) if len(sys.argv) > 2 else 1

    print(f"Scraping {pages} pages under the keyword '{keyword}'")

    output = []
    pages_scraped = 0


    chrome_driver_path = ChromeDriverManager().install()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    driver = webdriver.Chrome(service=ChromeService(chrome_driver_path), options=chrome_options)

    bar = tqdm(total=pages, desc='Scraping')

    start_time = datetime.datetime.now()

    for i in range(0, pages):
        output.append(scrape_shallow_product_info(driver, keyword, i))
        pages_scraped = pages_scraped + 1
        bar.update(1)
    end_time = datetime.datetime.now()

    driver.quit()

    bar.close()

    metadata = {
        "keyword": keyword,
        "pages": pages,
        "total_listings": sum(len(sublist) for sublist in output),
        "scraped_data": [item for sublist in output for item in sublist]
    }

    output = json.dumps(metadata, indent=2)
    
    print(output)

    listings_per_second = output.count("uuid") / (end_time - start_time).total_seconds()
    
    print('\n')
    print(f'Pages scraped: {pages_scraped}')
    print(f'Listings scraped: {output.count("uuid")} ({listings_per_second:.2f} per second)')
    print(f'Time taken: {end_time - start_time}')

    with open(f'output/output-{keyword}-{datetime.datetime.now()}.txt', "w") as file:
        file.write(output)

if __name__ == "__main__":
    main()
