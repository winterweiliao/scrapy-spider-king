# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MySpidersItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    market_name = scrapy.Field()
    market_hash_name = scrapy.Field()
    price = scrapy.Field()
    trade_time = scrapy.Field()
    app_code = scrapy.Field()
    pass


class OpSkinsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    market_hash_name = scrapy.Field()
    price = scrapy.Field()
    open_price = scrapy.Field()
    close_price = scrapy.Field()
    lowest_price = scrapy.Field()
    highest_price = scrapy.Field()
    trade_date = scrapy.Field()
    app_code = scrapy.Field()
    pass
