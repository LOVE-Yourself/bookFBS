# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookobjectItem(scrapy.Item):

    book_name = scrapy.Field()
    book_img = scrapy.Field()
    author = scrapy.Field()
    book_info = scrapy.Field()


