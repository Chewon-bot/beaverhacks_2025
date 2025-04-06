# https://sokoglam.com/products/neogen-dermalogy-real-niacinamide-glow-up-daily-mask?_pos=4&_sid=a5c6d5f5d&_ss=r
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from time import sleep

from random import choice
from csv import DictWriter
from csv import DictReader

def scrape_products():
    all_products = []
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)

    BASE_URL = "https://sokoglam.com/products/neogen-dermalogy-real-niacinamide-glow-up-daily-mask?_pos=4&_sid=a5c6d5f5d&_ss=r"
    print(f"Now scraping {BASE_URL}...")  # have idea of what's happening
    driver.get(BASE_URL)
    sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")  # indeed parsing html

    products = soup.select("section.pdp-main")
    for product in products:
        sleep(10)

        # products = soup.select(".order-best-product")
        #         for product in products:
        #             # inside of a span, just find by class
        #             all_products.append({
        #                 'discounted_price': product.select("product.price-info > span").get_text(strip=True),
        #                 # should filter out the usd
        #                 'full_price': product.select("div.price-info > strong").attrs['point'],
        #                 # should filter out the usd
        #                 'name': product.select("dl.brand-info > dd").get_text(strip=True), #
        #                 'name_kor': product.select("input.korPrdtName").attrs['value'],  #
        #                 'brand': product.select("dl.brand-info > dt").get_text(strip=True), #
        #                 'ranking': product.select("div.rank-badge > span").get_text(strip=True),  #
        #                 'photo': product.select("div.unit-thumb > img").attrs['src'],  #
        #                 'link': product.select("div.unit-thumb > a").attrs['title'] #
        #             })
        #             # print(quote.find(class_ = "text").get_text())  # grab txt out o them
        #
        #             # wanna get attribute(href) => use square bracket syntax.
        #
        #             #  how happen on every page? use next link =>grab url and scrape that url =>extract the url and scrape that url=>....
        #             # li w/ class="next" , find a tag w/ class="next"
        full_price_tag = product.select_one("span.pdp__product-price > span")
        name_tag = product.select_one("h1.pdp__product-title") #
        brand_tag = product.select_one("h3.pdp__product-vendor > a") #
        photo_tag = product.select_one("div.unit-thumb > img")

        all_products.append({
            'full_price': full_price_tag.get_text(strip=True) if full_price_tag else "",
            'name': name_tag.get_text(strip=True) if name_tag else "", #
            'brand': brand_tag.get_text(strip=True) if brand_tag else "",
            'photo': photo_tag.get("src", "") if photo_tag else "",
        })

            # print(quote.find(class_ = "text").get_text())  # grab txt out o them

            # wanna get attribute(href) => use square bracket syntax.

            #  how happen on every page? use next link =>grab url and scrape that url =>extract the url and scrape that url=>....
            # li w/ class="next" , find a tag w/ class="next"
    driver.quit()
    return all_products


def read_products(filename):
    with open(filename, "r", encoding="utf-8") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)
        # for thing in csv_reader:
        #     print(thing)


def write_products(products):
    with open("soko_glam.csv", "w", encoding="utf-8") as file:
        headers = ['full_price', 'name', 'brand', 'photo']
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for product in products:
            csv_writer.writerow(product)

read_products("products.csv")
products = scrape_products()
write_products(products)