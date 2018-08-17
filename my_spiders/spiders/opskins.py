# -*- coding: utf-8 -*-
import json
import random
import datetime
import scrapy

from my_spiders.items import OpSkinsSpiderItem
from my_spiders.items import MySpidersItem


class OpSkinsSpider(scrapy.Spider):
    name = 'opskins'
    allowed_domains = ['opskins.com']
    app_code = 433850
    start_urls = [
        # 'https://api.opskins.com/IPricing/GetPriceList/v2/?appid=%s' % app_code,
        'http://steamcommunity.com/market/listings/730/Chroma%20Case',
        'http://steamcommunity.com/market/listings/730/Spectrum%20Case%20Key',
        # 'http://steamcommunity.com/market/listings/730/Operation%20Hydra%20Case',
    ]

    def parse(self, response):
        return self.parse_steam(response)

    def parse_steam(self, response):
        try:
            content = response.text
            product_info = self.get_product_info(content=content)
            start = content.index('var line1=')
            sub_content = content[start:]
            end = sub_content.index('g_timePriceHistoryEarliest')
            sub_content = str(sub_content[:end]).replace('\r', '').replace('\n', '').strip().rstrip(';')
            items = json.loads(sub_content.split('=')[1])
            for item in items:
                trade_time = datetime.datetime.strptime(item[0], '%b %d %Y %H: +0')
                if trade_time > datetime.datetime.now() + datetime.timedelta(days=-30):
                    trade_price = item[1] * 6.6899
                    name = product_info.get('name')
                    app_code = product_info.get('app_code')
                    yield MySpidersItem(name=name, price=trade_price, trade_time=trade_time, app_code=app_code)
        except BaseException as e:
            print '%s' % e

    def get_product_info(self, content):
        """

        :param content:
        :return:
        """
        try:
            start = content.index('var g_rgAssets = ')
            sub_content = content[start:]
            end = sub_content.index('var g_rgListingInfo = ')
            sub_content = str(sub_content[:end]).replace('\r', '').replace('\n', '').strip().rstrip(';')
            information = json.loads(sub_content.split('=')[1])
            for app_code, data in information.items():
                for k, v in data.items():
                    for key, value in v.items():
                        return {'name': value.get('name'), 'app_code': app_code}
        except BaseException as e:
            print '%s' % e

    def parse_opskins(self, response):
        try:
            result = json.loads(response.text)
            if result.get('status') == 1:
                for name, item in result.get('response').items():
                    for trade_date, obj in item.items():
                        prices = [obj.get('normalized_min'), obj.get('normalized_max'), obj.get('normalized_mean')]
                        lowest_price = obj.get('normalized_min')
                        highest_price = obj.get('normalized_max')
                        open_price = (random.choice(prices) + random.choice(prices)) / 2
                        prices.append(open_price)
                        close_price = (random.choice(prices) + random.choice(prices)) / 2
                        yield OpSkinsSpiderItem(
                            name=name, app_code=self.app_code,
                            price=close_price,
                            lowest_price=lowest_price,
                            highest_price=highest_price,
                            open_price=open_price,
                            close_price=close_price,
                            trade_date=trade_date)
        except BaseException as e:
            print '%s' % e
