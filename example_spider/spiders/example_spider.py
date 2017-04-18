from scrapy.spiders import Spider
from scrapy import Field, Item, Request

class QuotesSpiderItem(Item):
    text = Field()
    author = Field()
    tags = Field()

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = QuotesSpiderItem()
            item['text'] = quote.css('span.text::text').extract_first()
            item['author'] = quote.css('small.author::text').extract_first()
            item['tags'] = quote.css('div.tags a.tag::text').extract()
            yield item

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse)
