from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def generate_lunch_urls(zip_code):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.set_window_size(1920, 1080)

    try:
        driver.get('https://www.lounaat.info/haku?etsi=' + zip_code)
        # Navigate to location search
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Sijainti')))
        driver.find_elements_by_partial_link_text('Sijainti')[1].click()
        # Wait for search results to appear
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'item-body')))
        # Parse urls
        urls = []
        for link in driver.find_elements_by_tag_name('a'):
            href = link.get_property('href')
            if 'https://www.lounaat.info/lounas/' in href:
                urls.append(href)
        f = open('lunch_urls.txt', 'w+')
        f.write('\n'.join(urls))
        f.close()
    except Exception as e:
        print e

    driver.quit()
