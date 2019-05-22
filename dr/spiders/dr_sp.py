# -*- coding: utf-8 -*-
import scrapy
from dr.items import DrItem

class DrSpSpider(scrapy.Spider):
    name = 'dr_sp'
    allowed_domains = ['www.goodreads.com']

    def start_requests(self):
        url = 'https://www.goodreads.com/author/quotes/'
        auth = getattr(self, 'author', None)

        if auth is not None:
            url = url + auth + '?page=1'
        yield scrapy.Request(url, self.parse, meta={'author': auth})

    def parse(self, response):
        quotes = response.xpath('//div[@class="quotes"]/div[@class="quote"]/div[@class="quoteDetails"]/div[@class="quoteText"]/text()[1]').getall()
        
        for q in quotes:
            yield DrItem(quote = q.strip() if q is not None else q,
                         author = response.meta.get('author'),
                         url = response.url)

        next_page = response.xpath('//div/div/a[@class="next_page"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse, meta=response.meta)