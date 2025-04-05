# https://global.oliveyoung.com/display/page/best-seller?target=pillsTab1Nav2

import scrapy

class OliveYoung(scrapy.Spider): #def a class that inherits scrapy.Spider
    name = 'oliveyoung'
    start_urls = ['https://global.oliveyoung.com/display/page/best-seller?target=pillsTab1Nav2']

    def parse(self, response): #parse result of request , no result, get... (response: what we get back from http request)
        for article in response.css('li.order-best-product'): #look for all articles w/ class product_pod
            yield {
            #     use yield instead o return
                'discounted_price': article.css("div.price-info > span::text").extract_first(), # should filter out the usd
                'full_price' : article.css("div.price-info > strong::attr(point)").extract_first(), # should filter out the usd
                'name' : article.css("d1.brand-info > dd::text").extract_first(), # anchor tag in h3 with the attribute title
                'name_kor': article.css("input[name = 'korPrdtName']::attr(value)").extract_first(), #
                'brand' : article.css("d1.brand-info > dt::text").extract_first(), # anchor tag in h3 with the attribute title
                'ranking' : article.css("div.rank-badge > span::text").extract_first(), #
                'photo' : article.css("div.unit-thumb > img::attr(src)").extract_first(), #
                'link' : article.css("div.unit-thumb > a::attr(title)").extract_first() #
            } #single dict w/ price
        # wanna do equiv o soup.find.get_text() = .extract_first() = [0].extract() = text/inner html of first item
        # here we have only 1 item

#  scrapy runspider -o olive_young.csv olive_young.py
