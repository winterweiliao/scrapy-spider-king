# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests


class MySpidersPipeline(object):
    def process_item123(self, item, spider):
        params = ["%s=%s" % (k, v) for k, v in dict(item).items()]
        print item
        url = 'http://localhost:8001/product/spider_write_day_line?' + '&'.join(params)
        response = requests.get(url)
        return response.text

    def process_item(self, item, spider):
        params = ["%s=%s" % (k, v) for k, v in dict(item).items()]
        # print item
        url = 'http://118.89.160.140/product/spider_write_trade_flow?' + '&'.join(params)
        response = requests.get(url)
        return response.text

    def process_item1(self, item, spider):
        params = ["%s=%s" % (k, v) for k, v in dict(item).items()]
        url = 'http://localhost:8001/product/spider_write?' + '&'.join(params)
        response = requests.get(url)
        return response.status_code == 200
