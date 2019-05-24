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
        else:
            print('Please set an author parameter. For example try: scrapy crawl dr_sp -a author=1244.Mark_Twain -s LOG_FILE=quotes.log -t csv -o - > quotes.csv')

    def parse(self, response):
        selector_list = response.xpath('//div[@class="quotes"]/div[@class="quote"]/div[@class="quoteDetails"]')

        for selector_item in selector_list:
            q = ''.join(selector_item.xpath('div[@class="quoteText"]/text()[following-sibling::br]').getall()).strip()
            b = selector_item.xpath('div[@class="quoteText"]/span[contains(@id, "quote_book")]/a/text()').get(default='').strip()
            tags = ' '.join(selector_item.xpath('div[@class="quoteFooter"]/div[@class="greyText smallText left"]/a/text()').getall()).strip()

            yield DrItem(quote = q,
                         author = response.meta.get('author'),
                         book = b,
                         tags = tags,
                         url = response.url)

        next_page = response.xpath('//div/div/a[@class="next_page"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse, meta=response.meta)