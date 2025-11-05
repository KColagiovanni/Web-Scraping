from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

def search_cl(keyword):

    count = 0
    base_url = "https://sfbay.craigslist.org"
    search_url = f"{base_url}/search/cta?query={keyword}=2~gallery~0"
    # search_url = f'https://sfbay.craigslist.org/search/cta?query={keyword}#search=2~gallery~0'

    options = Options()
    options.add_argument("--headless")  # run in background
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.get(search_url)
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify()[:3000])
    json_script = soup.find('script', {'id': 'ld_searchpage_results', 'type': 'application/ld+json'})

    if json_script:
        data = json.loads(json_script.string)
        items = data.get('itemListElement', [])

        # Extract real listing links dynamically
        post_links = driver.execute_script("""
            const links = [];
            document.querySelectorAll('a[href*="/cto/d/"]').forEach(a => {
                if (a.href.startsWith("https://")) links.push(a.href);
            });
            return links;
        """)
        # post_links = [a["href"] for a in soup.select('li.cl-static-search-result a.titlestring')]

        print(f'\n{keyword} Results:')
        for i, entry in enumerate(items):
            item = entry.get("item", {})
            name = item.get("name", "N/A")
            price = item.get("offers", {}).get("price", "N/A")
            location = (
                item.get("offers", {})
                .get("availableAtOrFrom", {})
                .get("address", {})
                .get("addressLocality", "N/A")
            )
            link = post_links[i] if i < len(post_links) else "N/A"

            # if keyword in name:
            #     count += 1
            print(f"{count}. {name} | ${price} | {location} | {link}")

        # print(f'\n{keyword} Results:')
        # for i, li in enumerate(items, start=1):
        #     title_tag = li.select_one("a.cl-app-anchor") or li.select_one("a")
        #     price_tag = li.select_one("span.price")
        #     location_tag = li.select_one("span.nearby, span.location")
        #
        #     title = title_tag.get_text(strip=True) if title_tag else "N/A"
        #     href = title_tag.get("href") if title_tag and title_tag.has_attr("href") else None
        #     price = price_tag.get_text(strip=True) if price_tag else "N/A"
        #     location = location_tag.get_text(strip=True) if location_tag else "N/A"
        #
        #     link = urljoin(base_url, href) if href else "N/A"
        #
        #     print(f"{i}. {title} | {price} | {location} | {link}")

    else:
        print("Could not find JSON data.")

    driver.quit()

if '__main__' == __name__:

    keywords = {
        # Cars and Trucks
        'cta':{
            'MR2',
            'Nova',
            'Chevy II',
            'Vega',
            'Monte Carlo',
            'Camaro',
            'Valiant',
            'Dart'
        },
        # Sporting
        'sga':{
            'Squat Rack',
        }
    }
    # print(list(keywords.keys())[0])

    for kw in keywords['cta']:
        search_cl(kw)