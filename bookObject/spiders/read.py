# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bookObject.items import BookobjectItem
from scrapy_redis.spiders import RedisCrawlSpider
import errno
class ReadSpider(RedisCrawlSpider):
    name = 'read'
    allowed_domains = ['www.dushu.com']
    #start_urls = ['https://www.dushu.com/']
    redis_key = 'read:start_urls'
    rules = (
        Rule(LinkExtractor(allow=r'/book/\d{4}\.html'),follow=True,callback='parse_page'),#设为true才能继续提取
        Rule(LinkExtractor(allow=r'/book/\d+_\d+\.html'),follow=True,callback='parse_page'),
    )

    def parse_item(self, response):

        bookitem = BookobjectItem()

        bookitem['book_name'] = response.xpath('//div[@class="bookslist"]/ul/li[1]/div/h3/a//text()').extract_first()
        bookitem['book_img'] = response.xpath('//div[@class="bookslist"]/ul/li[1]/div/div/a/img/@src').extract_first()

        book_info = response.xpath('//div[@class="bookslist"]/ul/li[1]/div/p[2]')
        bookitem['book_info'] = book_info.xpath("string(.)").extract_first()
        bookitem['author'] =response.xpath('//div[@class="bookslist"]/ul/li[1]/div/p[1]//text()').extract_first()
        yield bookitem

    def parse_page(self, response):

        bookitem = BookobjectItem()

        bookitem['book_name'] = response.xpath('//div[@class="bookslist"]/ul/li[1]/div/h3/a//text()').extract_first()
        url_info = response.xpath('//div[@class="bookslist"]/ul/li[1]/div/h3/a/@href').extract_first()

        new_url = 'http://www.dushu.com'+url_info
        print('----------->', new_url)
        bookitem['book_img'] = response.xpath('//div[@class="bookslist"]/ul/li[1]/div/div/a/img/@src').extract_first()

        book_info = response.xpath('//div[@class="bookslist"]/ul/li[1]/div/p[2]')
        #bookitem['book_info'] = book_info.xpath("string(.)").extract_first()
        bookitem['author'] =response.xpath('//div[@class="bookslist"]/ul/li[1]/div/p[1]//text()').extract_first()
        #try :
        yield scrapy.Request(url=new_url,meta={'item':bookitem},callback=self.parser_info)
        # except:
        #     print('该网址失效了！！！')

    def parser_info(self,response):

        item = response.meta['item']
        item['book_info'] = response.xpath('//div[@class="book-summary"][1]/div[@class="border margin-top padding-large"]/div[@class="text txtsummary"]//text()').extract_first()
        print('------>',item['book_info'])
        yield item


