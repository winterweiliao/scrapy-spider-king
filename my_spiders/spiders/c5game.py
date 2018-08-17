# -*- coding: utf-8 -*-
import json
import time
import datetime
import scrapy

from my_spiders.items import MySpidersItem


class C5GameSpider(scrapy.Spider):
    name = 'c5game'
    allowed_domains = ['c5game.com']
    start_urls = [
        # 'https://www.c5game.com/market/item/history.html?item_id=553431913',
        # 'https://www.c5game.com/dota/history/523.html',
        # 'https://www.c5game.com/dota/history/1.html',
        # 'https://www.c5game.com/dota/history/3.html',
        # 'https://www.c5game.com/dota/history/56.html',
        # 'https://www.c5game.com/dota/history/14897036.html',
        # 'https://www.c5game.com/dota/history/857.html',
        # 'https://www.c5game.com/dota/history/20312.html',
        # 'https://www.c5game.com/market/item/index.html?type=S&item_id=553371363',
        # 'https://www.c5game.com/market/item/index.html?type=S&item_id=553431635',
        # 'https://www.c5game.com/market/item/index.html?type=S&item_id=553371286',
        # 'https://www.c5game.com/market/item/index.html?type=S&item_id=553431640',
        # 'https://www.c5game.com/market/item/index.html?type=S&item_id=553371086',
        # 'https://www.igxe.cn/product/get_product_sales_history/578080/602958',
        # 'https://www.igxe.cn/product/get_product_sales_history/440/573038',
        # 'https://www.igxe.cn/product/get_product_sales_history/440/573073',
        # 'https://www.igxe.cn/product/get_product_sales_history/440/573372',
        # 'https://www.igxe.cn/product/get_product_sales_history/570/587108',
        # 'https://www.igxe.cn/product/get_product_sales_history/570/587351',
        # 'https://www.igxe.cn/product/get_product_sales_history/570/587106',
        # 'https://www.igxe.cn/product/get_product_sales_history/570/587105',
        # 'https://www.igxe.cn/product/get_product_sales_history/570/587070',
        # 'https://www.igxe.cn/product/get_product_sales_history/570/591616',
        'https://csgo.igv.cn',
    ]

    def __init__(self):
        super(scrapy.Spider, self).__init__()
        for x in range(10):
            self.start_urls.extend(C5GameSpider.start_urls)

    def parse(self, response):
        return self.parse_igv_csgo_index(response)

    def parse_igv_csgo_index(self, response):
        """
        爬取igv.cn首页交易记录
        :param response:
        :return:
        """
        for sel in response.xpath('.//dl'):
            if 'clearfix' in sel.extract() and '/product/detail' in sel.extract():
                name = sel.xpath('.//p[@class="clc"]/text()').extract()[0]
                price = sel.xpath('.//p[@class="cly"]/text()').extract()[0][2:]
                if 'style' not in sel.xpath('.//p[@class="clc4"]//b').extract()[0]:
                    exterior = sel.xpath('.//p[@class="clc4"]//b/text()')[0].extract()
                    market_name = '%s(%s)' % (name, exterior)
                else:
                    market_name = name
                # trade_time = '20' + sel.re('\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')[0]
                # trade_time = sel.xpath('.//p[@class="clc4"]/text()').extract()[0]
                trade_time = sel.re('\d{2}:\d{2}:\d{2} \d{2}/\d{2}/\d{4}')[0]
                trade_time = datetime.datetime.strptime(trade_time, '%H:%M:%S %d/%m/%Y') + datetime.timedelta(hours=8)

                yield MySpidersItem(name=name, market_name=market_name,
                                    price=price, trade_time=trade_time, app_code=730)

    def parse_test(self, response):
        try:
            result = json.loads(response.text)
            if result.get('succ'):
                for item in result.get('data'):
                    name = item.get('name')
                    trade_price = item.get('unit_price')
                    trade_time = item.get('last_updated').replace(u'年', '-').replace(u'月', '-').replace(u'日', '')
                    app_code = item.get('app_id')
                    time.sleep(1)
                    yield MySpidersItem(name=name, price=trade_price, trade_time=trade_time, app_code=app_code)
        except BaseException as e:
            print '%s' % e

    def parse_c5game(self, response):
        for sel in response.xpath('.//tr'):
            if 'ft-gold' in sel.extract():
                name = sel.xpath('.//div[@class="name-ellipsis"]/text()').extract()[0]
                trade_price = sel.xpath('.//span[@class="ft-gold"]/text()').extract()[0][1:]
                trade_time = '20' + sel.re('\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')[0]
                app_code = 570
                yield MySpidersItem(name=name, price=trade_price, trade_time=trade_time, app_code=app_code)

    def parse1(self, response):
        for sel in response.xpath('//tbody'):
            url = 'https://www.c5game.com' + sel.root.attrib.get('data-url')
            yield scrapy.Request(url, callback=self.parse)

        try:
            result = json.loads(response.text)
            if result.get('status') == 200:
                for item in result.get('body').get('items'):
                    yield MySpidersItem(market_hash_name=item.get('name'), price=item.get('price'))
        except BaseException as e:
            print '%s' % e
