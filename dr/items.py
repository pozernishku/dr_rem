# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DrItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()
    book = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
