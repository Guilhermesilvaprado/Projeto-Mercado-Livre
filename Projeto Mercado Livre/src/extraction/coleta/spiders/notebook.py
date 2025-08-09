import scrapy

class NotebookSpider(scrapy.Spider):
    name = "notebook"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = [
        "https://lista.mercadolivre.com.br/informatica/portateis-acessorios/notebooks/notebook"
    ]

    max_pages = 10
    products_per_page = 50  # normalmente 48 ou 50, ajuste conforme necessário

    def parse(self, response):
        products = response.css('div.ui-search-result__wrapper')
        for product in products:
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            yield {
                'seller': product.css('span.poly-component__seller::text').get(),
                'nome': product.css('a.poly-component__title::text').get(),
                'reviews_rating': product.css('span.poly-reviews__rating::text').get(),
                'reviews_total': product.css('span.poly-reviews__total::text').get(),
                'old_money': prices[0] if len(prices) > 0 else None,
                'new_money': prices[1] if len(prices) > 1 else None
            }

        # Paginação manual
        current_offset = response.url.split('_Desde_')
        if len(current_offset) > 1:
            offset = int(current_offset[1].split('_')[0])
        else:
            offset = 1

        next_offset = offset + self.products_per_page
        page_number = (next_offset // self.products_per_page) + 1

        if page_number <= self.max_pages:
            next_page_url = f"https://lista.mercadolivre.com.br/informatica/portateis-acessorios/notebooks/notebook_Desde_{next_offset}_NoIndex_True"
            yield scrapy.Request(url=next_page_url, callback=self.parse)
