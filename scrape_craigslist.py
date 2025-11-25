from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from bs4 import BeautifulSoup
import time
import re

def search_cl(keyword, category):

    count = 0
    search_url = f'https://sfbay.craigslist.org/search/{category}?query={keyword}#search=2~gallery~0'
    link_info = {}
    post_desc_split = []
    post_link_list = []
    link = 'N/A'

    options = Options()
    options.add_argument("--headless")  # run in background
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.get(search_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    json_script = soup.find('script', {'id': 'ld_searchpage_results', 'type': 'application/ld+json'})

    if json_script:
        data = json.loads(json_script.string)
        items = data.get('itemListElement', [])

        # print(f'items is: {items}')
        categories = [
            'a[href*="/cto/d/"]',  # Car and Trucks
            'a[href*="/ctd/d/"]',  # Car and Trucks
            'a[href*="/spo/d/"]',  # Sporting Goods
            'a[href*="/sgd/d/"]',  # Sporting Goods
        ]
        # Extract real listing links dynamically
        post_links = driver.execute_script("""
            const links = [];
            var data = arguments[0];
            document.querySelectorAll(data).forEach(a => {
                if (a.href.startsWith("https://") && !links.includes(a.href)) links.push(a.href);
            });
            return links;
        """, categories)

        print('\n####################################################################################################')
        # print(f'{keyword} post_links are:')
        for link_num in range(len(post_links)):
            # print(f'\n{link}')
            # link_info[link] = {}

            link = post_links[link_num]
            # print(f'\npost link is: {link}')

            post_id = link.split('/')[-1].split('.')[0]
            # print(f'  - post_id is: {post_id}')

            post_desc = link.split('/')[-2]#replace('-', ' ')
            post_desc_split = post_desc.split('-')
            # print(f'  - post_desc is: {post_desc}')
            # print(f'  - post_desc_list is: {post_desc_split}')

            region = link.split('/')[-5]
            # print(f'  - region is: {region}')

            link_info[link_num] = {
                'post_id':post_id,
                'post_desc':post_desc,
                'post_desc_split':post_desc_split,
                'region':region,
                'link':link
            }


        # print(f'\nlink_info is: {link_info}')
        # for entry in link_info:
        #     # print(f'\nentry is: {entry}')
        #     if ' ' in keyword:
        #         # print(f'{keyword} is multiple words')
        #         keyword_split = keyword.split(' ')
        #         for index in range(len(keyword_split)):
        #             # print(f'keyword_split[index].lower() is: {keyword_split[index].lower()}')
        #             # print(f'post_desc_split is: {post_desc_split}')
        #             if keyword_split[index].lower() in link_info[entry]['post_desc_split']:
        #                 print(f'link_info[{entry}] is: {link_info[entry]}')

            # else:
                # print(f"link_info[entry]['post_desc'] is {link_info[entry]['post_desc']}")
                # print(f'{keyword} is a single word')
                # print(f'keyword_lower() is: {keyword.lower()}')
                # print(f'post_desc_split is: {post_desc_split}')

                # if keyword.lower() in link_info[entry]['post_desc_split']:
                #     print(f'link_info[entry] is: {link_info[entry]}')

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



            # link = post_links[i] if i < len(post_links) else "N/A"
            # print(f'\nname is: {name}')
            # print('modified name is: ' + re.sub("[^a-zA-Z0-9\s]", "", name))
            new_name = re.sub("[^a-zA-Z0-9\s]", "", name)
            location_and_description = f'{location.replace(" ", "-").lower()}-{new_name.replace(" ", "-").lower()}'
            # print(f'\nlength of location_and_description is: {len(location_and_description)}')
            # print(f'location_and_description is: {location_and_description}')
            for post_link in post_links:
                post_link_list.append(len(post_link.split("/")[-2]))
                # print(f'post_link description length is: {len(post_link.split("/")[-2])}')
                # print(f'location_and_description[:len(location_and_description) - 2] is {location_and_description[:len(location_and_description) - 2]}')
                if location_and_description[:len(post_link.split("/")[-2])] in post_link:
                    print(f'{location_and_description[:len(post_link.split("/")[-2])]} is in {post_link}')
                    # print(f'location_and_description[:20] is: {location_and_description[:20]}')
                    # print(f'post_link is: {post_link}')
                    link = post_link
                    break

            # print(f'name is: {name}')
            # print(f'keyword is: {keyword}')
            # print(f'price is: {price}')
            if keyword.lower() in name.lower():
                count += 1
                print(f"{count}. {name} | ${price} | {location} | {link}")
        if count == 0:
            print(f'No {keyword} results were found.')
    else:
        print("Could not find JSON data.")

    # print(f'AVERAGE post_link_list length is: {sum(post_link_list)/len(post_link_list)}')
    # print(f'MAX post_link_list length is: {max(post_link_list)}')
    # print(f'MIX post_link_list length is: {min(post_link_list)}')
    driver.quit()

if '__main__' == __name__:

    keywords = {
        # Cars and Trucks
        'cta':{
            'MR2',
            'Nova',
            'Bel Air',
            'Belair',
            'Vega',
            'Monte Carlo',
            'Cobalt',
            # 'Camaro',
            # 'Corvette',
            'Valiant',
            'Dart'
        },
        # Sporting
        'sga':{
            'Squat Rack',
        }
    }

    for key in keywords.keys():
        for kw in keywords[key]:
            search_cl(kw, key)
    # for kw in keywords['sga']:
    #     search_cl(kw)