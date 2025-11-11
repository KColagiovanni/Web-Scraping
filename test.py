from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import quote

def search_cl(keyword):

    print('\n#########################################################################################################')
    count = 0
    # search_url = f'https://sfbay.craigslist.org/search/cta?query={keyword}#search=2~gallery~0'

    base_url = "https://sfbay.craigslist.org"
    search_url = f"{base_url}/search/cta?query={quote(keyword)}#search=2~gallery~0"

    options = Options()
    # options.add_argument("--headless")  # run in background
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Trick headless Chrome into pretending it’s normal Chrome
    options.add_argument("--headless=new")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.navigator.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        """
    })
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options)
    driver.get(search_url)
    # print(driver.page_source[:2000])  # Print first 2KB of HTML
    time.sleep(3)  # give time for JS to load

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    json_script = soup.find('script', {'id': 'ld_searchpage_results', 'type': 'application/ld+json'})

    # # ✅ FIX 1: move driver.quit() to the very end, after collecting everything
    # post_links = driver.execute_script("""
    #     const seen = new Set();
    #     const links = [];
    #
    #     document.querySelectorAll('li.cl-static-search-result a').forEach(a => {
    #         const href = a.href;
    #
    #         // filter out duplicates, empty, or irrelevant links
    #         if (href && href.includes('/cto/d/') && !seen.has(href)) {
    #             seen.add(href);
    #             links.push(href);
    #         }
    #     });
    #     return links;
    # """)

    # # Wait for <search-page> custom element to load
    # WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "search-page"))
    # )

    # print("✅ search-page present:", bool(driver.find_elements(By.CSS_SELECTOR, "search-page")))
    # time.sleep(5)
    #
    # # Wait longer for the <search-page> to appear
    # try:
    #     WebDriverWait(driver, 20).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, "search-page"))
    #     )
    # except:
    #     print("⚠️ Timed out waiting for search-page to load.")
    #     post_links = []
    # else:
    #     # Extract links from nested shadow DOMs
    #     post_links = driver.execute_script("""
    #         function getShadowRoot(el) {
    #             return el && el.shadowRoot ? el.shadowRoot : null;
    #         }
    #
    #         const links = new Set();
    #         const searchPage = document.querySelector('search-page');
    #         if (!searchPage) return Array.from(links);
    #
    #         const spRoot = getShadowRoot(searchPage);
    #         if (!spRoot) return Array.from(links);
    #
    #         // "cl-search-results" custom element inside the shadow root
    #         const results = spRoot.querySelector('cl-search-results');
    #         const resultsRoot = getShadowRoot(results);
    #         if (!resultsRoot) return Array.from(links);
    #
    #         // Each post is a <cl-search-result> custom element with its own shadow DOM
    #         const items = resultsRoot.querySelectorAll('cl-search-result');
    #         items.forEach(item => {
    #             const itemRoot = getShadowRoot(item);
    #             if (!itemRoot) return;
    #             const a = itemRoot.querySelector('a.titles
    #     """)
    #
    # print(f"\npost_links for {keyword}: {post_links}")

    # # Wait a bit longer for JS-rendered content to appear
    # time.sleep(5)
    #
    # # ✅ Run JS directly to look for <search-page> dynamically
    # is_present = driver.execute_script("return !!document.querySelector('search-page');")
    # print("✅ search-page present (via JS):", is_present)
    #
    # if not is_present:
    #     print("⚠️ search-page not yet visible, trying fallback delay...")
    #     time.sleep(5)
    #     is_present = driver.execute_script("return !!document.querySelector('search-page');")
    #
    # if not is_present:
    #     print("❌ Still no <search-page> found — Craigslist likely throttled JS access.")
    #     post_links = []
    # else:
    #     # ✅ Use JS traversal of nested shadow DOMs (works even if Selenium can’t see it)
    #     post_links = driver.execute_script("""
    #         function getShadowRoot(el) {
    #             return el && el.shadowRoot ? el.shadowRoot : null;
    #         }
    #         const links = new Set();
    #         const searchPage = document.querySelector('search-page');
    #         if (!searchPage) return Array.from(links);
    #
    #         const spRoot = getShadowRoot(searchPage);
    #         if (!spRoot) return Array.from(links);
    #
    #         const clResults = spRoot.querySelector('cl-search-results');
    #         const clRoot = getShadowRoot(clResults);
    #         if (!clRoot) return Array.from(links);
    #
    #         const items = clRoot.querySelectorAll('cl-search-result');
    #         items.forEach(it => {
    #             const itRoot = getShadowRoot(it);
    #             if (!itRoot) return;
    #             const a = itRoot.querySelector('a[href]');
    #             if (a && a.href.startsWith("https")) links.add(a.href);
    #         });
    #
    #         return Array.from(links);
    #     """)
    #
    # print(f"\npost_links for {keyword}: {post_links}")

    time.sleep(5)
    # print(driver.page_source[:5000])
    # post_links = driver.execute_script("""
    #     const anchors = Array.from(document.querySelectorAll('a.titlestring'));
    #     return anchors.map(a => a.href).filter(h => h && h.startsWith('https'));
    # """)
    # print(f"\nFound {len(post_links)} post links for {keyword}:")
    # print(post_links)

    if json_script:
        data = json.loads(json_script.string)
        items = data.get('itemListElement', [])
        print("\n🧩 RAW JSON (first 3000 chars):\n", json_script.string[:3000])
        print(f'\n{keyword} Results:')
        # for i, entry in enumerate(items):
        #     item = entry.get("item", {})
        #     name = item.get("name", "N/A")
        #     price = item.get("offers", {}).get("price", "N/A")
        #     location = (
        #         item.get("offers", {})
        #         .get("availableAtOrFrom", {})
        #         .get("address", {})
        #         .get("addressLocality", "N/A")
        #     )
        #
        #     # # ✅ FIX 2: safely match link index or fallback to "N/A"
        #     # link = post_links[i] if i < len(post_links) else "N/A"
        #
        #     # 🔍 Try to extract the posting ID
        #     post_id = None
        #     images = item.get("image", [])
        #     if images:
        #         for img_url in images:
        #             match = re.search(r'/(\d{9,})_', img_url)
        #             # print(f'match is: {match}')
        #             if match:
        #                 post_id = match.group(1)
        #                 break
        #
        #     # Slugify the title to form a URL-safe path
        #     slug = re.sub(r'[^a-zA-Z0-9]+', '-', name.lower()).strip('-')
        #
        #     print(f'post link is: {f"{base_url}/cto/d/{slug}/{post_id}.html"}')
        #
        #     link = f"{base_url}/cto/d/{slug}/{post_id}.html" if post_id else "N/A"
        #
        #     if keyword.lower() in name.lower():
        #         count += 1
        #         print(f"{count}. {name} | ${price} | {location} | {link}")

        for i, entry in enumerate(items):
            item = entry.get("item", {})
            # print(f'item is: {item}')
            name = item.get("name", "N/A")
            price = item.get("offers", {}).get("price", "N/A")
            location = (
                item.get("offers", {})
                .get("availableAtOrFrom", {})
                .get("address", {})
                .get("addressLocality", "N/A")
            )

            # ✅ Craigslist now includes the canonical listing link right here:
            link = item.get("url") or item.get("@id")

            print(f'original link is: {link}')

            # ✅ If "url" is missing, fallback to old image-ID or slug logic
            if not link:
                post_id = None
                images = item.get("image", [])
                if images:
                    for img_url in images:
                        match = re.search(r'/(\d{9,})_', img_url)
                        if match:
                            post_id = match.group(1)
                            break
                slug = re.sub(r'[^a-zA-Z0-9]+', '-', name.lower()).strip('-')
                print('\n---------------------------------------------')
                print(f'base_url is: {base_url}')
                print(f'slug is: {slug}')
                print(f'post_id is: {post_id}')
                link = f"{base_url}/cto/d/{slug}/{post_id}.html" if post_id else "N/A"
                print(f'last link is: {link}')

            # print(f"post link is: {link}")

            if keyword.lower() in name.lower():
                count += 1
                print(f"{count}. {name} | ${price} | {location} | {link}")

        if count == 0:
            print(f'No {keyword} results were found.')

    else:
        print("Could not find JSON data.")

    driver.save_screenshot(f"debug_{keyword}.png")

    # ✅ Now we close the browser
    driver.quit()


if __name__ == '__main__':
    keywords = {
        'cta': {
            'MR2',
            'Nova',
            'Chevy II',
            'Vega',
            'Monte Carlo',
            'Valiant',
            'Dart'
        }
    }

    for kw in keywords['cta']:
        search_cl(kw)
