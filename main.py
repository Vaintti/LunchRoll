import autopopulator
from bs4 import BeautifulSoup
from datetime import datetime
import random
import re
import requests
import sys


def get_random_url():
    f = open('lunch_urls.txt', 'r')
    urls = []
    for url in f:
        urls.append(url)
    if len(urls) == 0:
        raise Exception('lunch_urls.txt file is empty. Add www.lounaat.info urls to restaurants to that file.')
    index = random.randint(0, len(urls) - 1)
    return urls[index].strip()


def get_menu(url):
    page = requests.get(url)
    if not page.ok:
        raise Exception('Request failed')
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')

    # Parse restaurant's name and add it to output
    name = soup.find('h2', {'itemprop': 'name'}).text.strip()
    output = name
    underline = '-' * len(name)
    output += '\n' + underline

    menu = soup.select('div.item-body')
    menu_today = menu[datetime.today().weekday()]

    # Check for missing menu
    missing = menu_today.find('a', {'class': 'missing'})
    if missing is not None:
        output += '\n' + missing.text
        return output

    # Parse today's menu
    dish_content = menu_today.find_all('p')
    for content in dish_content:
        dishes = content.text
        # Clean output
        dishes = dishes.replace(' l ', '')
        dishes = dishes.replace(' G ', '')
        dishes = dishes.replace(' g ', '')
        dishes = dishes.replace(' m ', '')
        dishes = re.sub(r'\s\s+', '\n', dishes)
        dishes = dishes.strip()
        output += '\n' + dishes
    return output


def get_random_menu():
    try:
        url = get_random_url()
        print url.encode('utf-8').strip()
        menu = get_menu(url)
        print ('\n' + menu).encode('utf-8').strip()
    except Exception as e:
        print e


def lunch_urls_is_populated():
    try:
        f = open('lunch_urls.txt', 'r')
        count = len(f.readlines())
        f.close()
        return count != 0
    except IOError:
        return False


zip_code = sys.argv.pop()
if not lunch_urls_is_populated() and zip_code is not None:
    autopopulator.generate_lunch_urls(zip_code=zip_code)

if lunch_urls_is_populated():
    get_random_menu()
