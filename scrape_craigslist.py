from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
from bs4 import BeautifulSoup
import time

mr2_search_url = 'https://sfbay.craigslist.org/search/cta?query=mr2#search=2~gallery~0'

options = Options()
options.add_argument("--headless")  # run in background
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/120.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

# driver.get("https://sfbay.craigslist.org/search/cta")
driver.get(mr2_search_url)
time.sleep(2)
print(f'Title is: {driver.title}')

html = driver.page_source
# print(f'\nHTML: {html[:5000]}')
soup = BeautifulSoup(html, 'html.parser')
json_script = soup.find('script', {'id': 'ld_searchpage_results', 'type': 'application/ld+json'})

# print(f'json_script is: {json_script}')

if json_script:
    data = json.loads(json_script.string)
    items = data.get('itemListElement', [])

    for entry in items:
        item = entry.get("item", {})
        name = item.get("name", "N/A")
        price = item.get("offers", {}).get("price", "N/A")
        currency = item.get("offers", {}).get("priceCurrency", "USD")
        location = item.get("offers", {}).get("availableAtOrFrom", {}).get("address", {}).get("addressLocality", "N/A")
        image_list = item.get("image", [])
        image = image_list[0] if image_list else "N/A"

        if 'mr2' in name.lower():
            print(f"{name} | {price} {currency} | {location} | {image}")
else:
    print("Could not find JSON data.")


# response = requests.get(mr2_search_url)
# data = response.json()
# print(json.dumps(data, indent=2))

driver.quit()
