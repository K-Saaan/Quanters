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


class NewsCrawlPipeline:
    def process_item(self, item, spider):
        return item



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

class CsvPipeline(object):
    def __init__(self):
        self.file = open('../../data/news/newsUrlCrawl3.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    
class NewsCsvPipeline(object):
    def __init__(self):
        self.file = open('../../data/news/kakaoNewsCrawl2.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item