import scrapy

class SokoglamSpider(scrapy.Spider):
    name = "sokoglam_awards"
    allowed_domains = ["sokoglam.com"]
    start_urls = ["https://sokoglam.com/collections/soko-glam-best-of-beauty-awards"]

    def parse(self, response):
        products = response.css('div.card-information')  # Updated to match actual structure
        for idx, product in enumerate(products, start=1):
            product_data = {
                'ranking': idx,
                'name': product.css('p.product-title::text').get(default='').strip(),
                'brand': product.css('span.vendor::text').get(default='').strip(),
                'price': product.css('span.price::text').get(default='').strip(),
                'link': response.urljoin(product.css('a.full-unstyled-link::attr(href)').get()),
                'photo': product.css('img.motion-reduce::attr(src)').get(default=''),
            }

            print(product_data)
            yield product_data

        # Pagination (if needed)
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
