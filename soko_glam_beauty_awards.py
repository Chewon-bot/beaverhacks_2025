import scrapy


class SokoglamSpider(scrapy.Spider):
    name = "sokoglam_awards"
    allowed_domains = ["sokoglam.com"]
    start_urls = ["https://sokoglam.com/collections/soko-glam-best-of-beauty-awards"]

    def parse(self, response):
        products = response.css('div.grid-product')  # Adjust the selector if needed
        for idx, product in enumerate(products, start=1):
            product_data = {
                'ranking': idx,
                'name': product.css('div.grid-product__title::text').get(default='').strip(),
                'price': product.css('span.price::text').get(default='').strip(),
                'brand': product.css('div.grid-product__vendor::text').get(default='').strip(),
                'link': response.urljoin(product.css('a.grid-product__link::attr(href)').get()),
                'photo': product.css('img::attr(src)').get(default=''),
            }

            # Print the result for each product
            print(product_data)

            # Yield the product data to continue scraping and store it
            yield product_data

        # Handle pagination (if any)
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
