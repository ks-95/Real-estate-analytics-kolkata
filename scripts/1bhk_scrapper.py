import requests
import json
import time
from pathlib import Path
from config import BRONZE_DIR
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=1&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName=Kolkata"

def auto_scroll_and_scrape(url, max_scrolls=10):
    all_cards_data = []

    with sync_playwright() as p:
        # Launch browser (headless=True means no visible UI window)
        browser = p.chromium.launch(headless=True, args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",  # Crucial for Docker (uses /tmp instead of small /dev/shm)
            "--disable-gpu",
            "--disable-software-rasterizer",
        ])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        print("Navigating to page...")
        page.goto(url, timeout=60000)

        # Perform incremental scrolling to trigger dynamic loading
        for scroll_count in range(max_scrolls):
            print(f"Scrolling down... (Scroll {scroll_count + 1}/{max_scrolls})")
            
            # Scroll to bottom
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for dynamic content to fetch and render
            time.sleep(3)

        # Get final HTML content after scrolling
        content = page.content()
        browser.close()
    soup = BeautifulSoup(content, 'html.parser')
    cards = soup.select('.mb-srp__card')
    for card in cards:
        title_element = card.select_one('.mb-srp__card--title')
        price_element = card.select_one('.mb-srp__card__price--amount')
        price_per_sqft_element = card.select_one('.mb-srp__card__price--size')
        area_elemnet = card.select_one('.mb-srp__card__summary--value')

        title = title_element.get_text(strip=True) if title_element else ""
        price = price_element.get_text(strip=True) if price_element else ""
        price_per_sqft = price_per_sqft_element.get_text(strip=True) if price_per_sqft_element else ""
        carpet_area = area_elemnet.get_text(strip=True) if area_elemnet else ""
        dictionary = {
            "title": title,
            "price": price,
            "price_per_sqft": price_per_sqft,
            "carpet_area": carpet_area,
        }
        # json.dumps(dictionary, indent=4)
        # print(dictionary)
        all_cards_data.append(dictionary)

    return all_cards_data


#scraped_data = get_details()
scraped_data = auto_scroll_and_scrape(url, max_scrolls=5)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Create bronze directory
#bronze_path = Path(r"C:\Users\KANAK\scraping\data\bronze\one_bhk_data")
#bronze_path.mkdir(parents=True, exist_ok=True)


# Save raw JSON
#file_path = bronze_path / f"real_estate_raw_{timestamp}.json"
##output_file = BRONZE_DIR / "one_bhk_data" / f"real_estate_raw_{timestamp}.json"
output_dir_1bhk = Path("/app/data/bronze/one_bhk_data")
output_dir_1bhk.mkdir(parents=True, exist_ok=True)

output_file = output_dir_1bhk / f"real_estate_raw_{timestamp}.json"


with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(scraped_data, json_file, indent=4, ensure_ascii=False)

print("Data successfully saved to properties.json!")

