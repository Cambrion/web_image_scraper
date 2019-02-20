from selenium import webdriver
import json
import os
import uuid
from urllib.request import urlopen, Request

SAVE_DIRECTORY = '/Users/Cameron/Downloads/Images'
CHROME_DRIVER_PATH = "/Users/Cameron/Downloads/chromedriver"
REQUEST_HEADER = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
SCROLL_HEIGHT = 1080
SCROLL_COUNT = 100


def get_query_url(query):
    return "https://www.google.com/search?q=%s&source=lnms&tbm=isch" % query


def get_headless_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=options)


def save_image(raw_image, image_type, save_directory):
    extension = image_type if image_type else 'jpg'
    file_name = str(uuid.uuid4().hex) + "." + extension
    save_path = os.path.join(save_directory, file_name)
    with open(save_path, 'wb+') as image_file:
        image_file.write(raw_image)


def get_raw_image(url):
    request = Request(url, headers=REQUEST_HEADER)
    response = urlopen(request)
    return response.read()


def check_save_directory():
    if not os.path.exists(SAVE_DIRECTORY):
        os.mkdir(SAVE_DIRECTORY)


def scroll_browser(browser, scroll_count, scroll_height):
    for _ in range(scroll_count):
        browser.execute_script("window.scrollBy(0," + str(scroll_height) + ")")


def main():
    search_term = input("Please enter search term: ")
    url = get_query_url(search_term)
    browser = get_headless_browser()
    browser.get(url)
    check_save_directory()
    scroll_browser(browser, SCROLL_COUNT, SCROLL_HEIGHT)
    count = 0
    pass_count = 0
    elements = browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')

    for element in elements:
        count = count + 1
        print("Total Images Downloaded:", count)

        image = json.loads(element.get_attribute('innerHTML'))["ou"]
        image_type = json.loads(element.get_attribute('innerHTML'))["ity"]
        try:
            raw_image = get_raw_image(image)
            save_image(raw_image, image_type, SAVE_DIRECTORY)
            pass_count = pass_count + 1
        except Exception:
            print("Unable to retrieve image")

    print(pass_count, "pictures successfully downloaded")
    browser.close()


if __name__ == '__main__':
    main()

