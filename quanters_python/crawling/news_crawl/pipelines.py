# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from __future__ import unicode_literals
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter, CsvItemExporter
from scrapy.settings import Settings
from scrapy.exceptions import DropItem
from scrapy.logformatter import logging
from datetime import datetime
import os

# 현재 날짜와 시간을 가져옵니다.
now = datetime.now()

# 년, 월, 일을 가져옵니다.
yymm = now.strftime("%Y%m")
dd = now.strftime("%d")


class NewsCrawlPipeline:
    def process_item(self, item, spider):
        return item

# Json 파일로 저장
class JsomPipeline(object):
    def __init__(self):
        self.file = open('../../data/news/newsUrlCrawl.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# csv 파일로 저장
class CsvPipeline(object):
    def __init__(self, spider_name):
        self.spider_name = spider_name
        print('spider name : ', spider_name)
        if spider_name == 'newsUrlCrawler':
            # path가 없으면 생성
            print('Start url item to csv >>>>>>>>>>>>>>>>')
            path = f'/home/home/kdh/quanters/data/news/url_crawl/{yymm}'
            # path = f'../../data/news/url_crawl/{yymm}'
            if not os.path.exists(path):
                os.mkdir(path)
            self.file = open(f'{path}/url_{dd}.csv', 'wb')
            self.exporter = CsvItemExporter(self.file, encoding='utf-8')
            self.exporter.start_exporting()
        elif spider_name == 'newsCrawler':
            print('Start text item to csv >>>>>>>>>>>>>>>>')
            path = f'/home/home/kdh/quanters/data/news/text_crawl/{yymm}'
            if not os.path.exists(path):
                os.mkdir(path)

            self.file = open(f'{path}/text_{dd}.csv', 'wb')
            self.exporter = CsvItemExporter(self.file, encoding='utf-8')
            self.exporter.start_exporting()
    @classmethod
    def from_crawler(cls, crawler):
        return cls(spider_name=crawler.spider.name)
    
    def close_spider(self, spider):
        if spider.name == 'newsUrlCrawler':
            self.exporter.finish_exporting()
            self.file.close()
        elif spider.name == 'newsCrawler':
            self.exporter.finish_exporting()
            self.file.close()
    def process_item(self, item, spider):
        if spider.name == 'newsUrlCrawler':
            self.exporter.export_item(item)
            return item
        elif spider.name == 'newsCrawler':
            self.exporter.export_item(item)
            return item
    
# class NewsCsvPipeline(object):
#     def __init__(self):
#         print('Start text item to csv >>>>>>>>>>>>>>>>')
#         path = f'/Users/gimsan/Documents/GitHub/Quanters/quanters_python/data/news/text_crawl/{yymm}'
#         # path = f'./quanters_python/data/news/text_crawl/{yymm}'
#         # path가 없으면 생성
#         if not os.path.exists(path):
#             os.mkdir(path)

#         self.file = open(f'{path}/text_{dd}.csv', 'wb')
#         self.exporter = CsvItemExporter(self.file, encoding='utf-8')
#         self.exporter.start_exporting()
    
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item