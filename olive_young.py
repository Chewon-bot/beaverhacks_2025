# http://books.toscrape.com/

import scrapy

class BookSpider(scrapy.Spider): #def a class that inherits scrapy.Spider
    name = 'bookspider'
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response): #parse result of request , no result, get... (response: what we get back from http request)
        for article in response.css('article.product_pod'): #look for all articles w/ class product_pod
        # soup.select(".special"): will give all items w/ special class
            yield {
            #     use yield instead o return
                'price' : article.css(".price_color::text").extract_first(), # get the text
                'title' : article.css("h3 > a::attr(title)").extract_first() # anchor tag in h3 with the attribute title
            } #single dict w/ price
        # wanna do equiv o soup.find.get_text() = .extract_first() = [0].extract() = text/inner html of first item
        # here we have only 1 item
            next = response.css('.next > a::attr(href)').extract_first() #class of next, inside of that atag with class href
            if next:
                yield response.follow(next, self.parse) #parse again(recursion)
