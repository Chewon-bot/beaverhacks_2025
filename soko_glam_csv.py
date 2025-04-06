
# https://sokoglam.com/products/neogen-dermalogy-real-niacinamide-glow-up-daily-mask?_pos=4&_sid=a5c6d5f5d&_ss=r
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from time import sleep

from random import choice
from csv import DictWriter
from csv import DictReader

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

read_product = read_products("products.csv")
print(read_product)
read_product["name"]