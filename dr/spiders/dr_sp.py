# -*- coding: utf-8 -*-
import scrapy
import os
from dr.items import DrItem
from scrapy.utils.project import data_path
import ast

class DrSpSpider(scrapy.Spider):
    name = 'dr_sp'
    allowed_domains = ['www.goodreads.com']

    def start_requests(self):
        cookies_to_send = ''
        filename = 'data.txt'
        mydata_path = data_path(filename)
        if os.path.exists(mydata_path) and os.path.getsize(mydata_path) > 0:
            with open(mydata_path, 'r') as f:
                canned_cookie_jar = f.read()
                cookies_to_send = ast.literal_eval(canned_cookie_jar)

        url = 'https://www.goodreads.com/author/quotes/'
        auth = getattr(self, 'author', None)

        if auth is not None:
            url = url + auth + '?page=1'
            self.log('>>>')
            self.log(cookies_to_send)
            yield scrapy.Request(url, self.parse, meta={'author': auth, 'cookies': cookies_to_send})
        else:
            print('Please set an author parameter. For example try: scrapy crawl dr_sp -a author=1244.Mark_Twain -s LOG_FILE=quotes.log -t csv -o - > quotes.csv')

    def parse(self, response):
        selector_list = response.xpath('//div[@class="quotes"]/div[@class="quote"]/div[@class="quoteDetails"]')

        for selector_item in selector_list:
            q = '<br>'.join(selector_item.xpath('div[@class="quoteText"]/text()[following-sibling::br] | div[@class="quoteText"]/i/text()').getall()).strip()
            b = selector_item.xpath('div[@class="quoteText"]/span[contains(@id, "quote_book")]/a/text()').get(default='').strip()
            tags = ' '.join(selector_item.xpath('div[@class="quoteFooter"]/div[@class="greyText smallText left"]/a/text()').getall()).strip()

            self.log('>>>')
            self.log(response.meta.get('cookies'))
            yield DrItem(quote = q,
                         author = response.meta.get('author'),
                         book = b,
                         tags = tags,
                         url = response.url)

        next_page = response.xpath('//div/div/a[@class="next_page"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse, meta=response.meta)