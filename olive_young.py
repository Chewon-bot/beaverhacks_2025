# https://global.oliveyoung.com/display/page/best-seller?target=pillsTab1Nav2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from time import sleep

from random import choice
from csv import DictWriter


def scrape_products():
    all_products = []
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)

    BASE_URL = "https://global.oliveyoung.com/display/page/best-seller?target=pillsTab1Nav2"
    print(f"Now scraping {BASE_URL}...")  # have idea of what's happening
    driver.get(BASE_URL)
    sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")  # indeed parsing html

    products = soup.select("li.order-best-product")
    for product in products:
        sleep(3)
            # inside of a span, just find by class
        # full_price_tag = product.select_one("div.price-info > span")
        # kor_name_tag = product.select_one("input.korPrdtName")
        # photo_tag = product.select_one("div.unit-thumb img")
        # link_tag = product.select_one("div.unit-thumb a")
        # all_products.append({
        #     'full_price': full_price_tag.get_text(strip=True) if full_price_tag else "",
        #         # should filter out the usd
        #     'discounted_price': product.select_one("strong.point").get_text(strip=True),
        #         # should filter out the usd
        #     'name': product.select_one("dl.brand-info > dd").get_text(strip=True),  #
        #     'name_kor': kor_name_tag.get("value","") if kor_name_tag else "",  #
        #     'brand': product.select_one("dl.brand-info > dt").get_text(strip=True),  #
        #     'ranking': product.select_one("div.rank-badge > span").get_text(strip=True),  #
        #     'photo': product.select_one("src","") if photo_tag else "",  #
        #     'link': product.select_one("title","") if photo_tag else "" #
        # })

        full_price_tag = product.select_one("div.price-info > span")
        discounted_price_tag = product.select_one("strong.point")
        name_tag = product.select_one("dl.brand-info > dd")
        brand_tag = product.select_one("dl.brand-info > dt")
        ranking_tag = product.select_one("div.rank-badge > span")
        photo_tag = product.select_one("div.unit-thumb img")
        link_tag = product.select_one("div.unit-thumb a")
        kor_name_tag = product.select_one("input.korPrdtName")

        all_products.append({
            'full_price': full_price_tag.get_text(strip=True) if full_price_tag else "",
            'discounted_price': discounted_price_tag.get_text(strip=True) if discounted_price_tag else "",
            'name': name_tag.get_text(strip=True) if name_tag else "",
            'name_kor': kor_name_tag.get("value", "") if kor_name_tag else "",
            'brand': brand_tag.get_text(strip=True) if brand_tag else "",
            'ranking': ranking_tag.get_text(strip=True) if ranking_tag else "",
            'photo': photo_tag.get("src", "") if photo_tag else "",
            'link': link_tag.get("href", "") if link_tag else ""
        })

            # print(quote.find(class_ = "text").get_text())  # grab txt out o them

            # wanna get attribute(href) => use square bracket syntax.

            #  how happen on every page? use next link =>grab url and scrape that url =>extract the url and scrape that url=>....
            # li w/ class="next" , find a tag w/ class="next"
    driver.quit()
    return all_products


def write_products(products):
    with open("products.csv", "w", encoding="utf-8") as file:
        headers = ['discounted_price', 'full_price', 'name', 'name_kor', 'brand', 'ranking', 'photo', 'link']
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for product in products:
            csv_writer.writerow(product)


products = scrape_products()
write_products(products)
