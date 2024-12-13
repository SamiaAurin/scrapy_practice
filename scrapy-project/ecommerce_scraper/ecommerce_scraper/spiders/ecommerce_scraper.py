import scrapy

class EcommerceSpider(scrapy.Spider):
    name = "ecommerce_scraper"
    start_urls = ["https://www.scrapingcourse.com/ecommerce/"]

    def parse(self, response):
        # Select all product cards
        product_cards = response.css("li[data-products='item']")
        for card in product_cards:
            # Extract product details
            title = card.css("h2.product-name::text").get()
            price = card.css("span.price bdi::text").get().replace("$", "").strip()
            image_url = card.css("img::attr(src)").get()

            # Yield item to the pipeline
            yield {
                'title': title,
                'price': price,
                'image_url': image_url,
            }
