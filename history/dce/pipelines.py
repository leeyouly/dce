# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from dce.items import DceDailyItem, DceCangdanItem
from dce.data import DceDailyStorage, DceCangdanStorage
from scrapy.utils.project import get_project_settings

class DcePipeline(object):
    def process_item(self, item, spider):
        return item

class DceDailySave(object):
    def __init__(self):
        self.storage = DceDailyStorage(get_project_settings().get('DATABASE'))
        
    def process_item(self, item, spider):
        if isinstance(item, DceDailyItem):
            if not self.storage.exist(item):
                self.storage.save(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')
        return item

class DceCangdanSave(object):
    def __init__(self):
        self.storage = DceCangdanStorage(get_project_settings().get('DATABASE'))
        
    def process_item(self, item, spider):
        if isinstance(item, DceCangdanItem):
            if not self.storage.exist(item):
                self.storage.save(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')
        return item
