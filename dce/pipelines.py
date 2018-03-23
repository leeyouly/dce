# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from dce.items import DceDailyItem, DceCangdanItem, DceChicangItem, DcePinzhongChicangItem, DceMemberItem
from dce.data import DceDailyStorage, DceCangdanStorage, DceChicangStorage, DcePinzhongChicangStorage, DceMemberStorage
from scrapy.utils.project import get_project_settings
from scrapy.contrib.exporter import JsonItemExporter
from scrapy import signals
import sys, os
import datetime
from dce.ftpFactory import uploadfile


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
                self.storage.save_or_update(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')
        return item


class DceChicangSave(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        print(get_project_settings().get('JASONFILE_PATH') + 'items.json')
        self.file = open('items' + datetime.datetime.today().strftime('%Y-%m-%d') + '.json', 'wb')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        #         print(get_project_settings().get('JASONFILE_PATH') +'items.json')
        #         datestampStr=datetime.datetime.today().strftime('%Y-%m-%d')
        #         if os.path.exists(get_project_settings().get('JASONFILE_PATH')+'items_end'+datestampStr+'.json'):
        #             os.remove(get_project_settings().get('JASONFILE_PATH')+'items_end'+datestampStr+'.json')
        #         print(get_project_settings().get('JASONFILE_PATH')+ 'items_end.json')
        #         os.rename(get_project_settings().get('JASONFILE_PATH')+'items.json',get_project_settings().get('JASONFILE_PATH')+ 'items_end'+datestampStr+'.json')
        #
        # 读取配置
        settings = get_project_settings()
        ftp_host = settings.get('FTP_HOST')
        ftp_username = settings.get('FTP_USER')
        ftp_password = settings.get('FTP_PASSWORD')
        ftp_path = settings.get('FTP_PATH')

        filenametosave = 'items' + datetime.datetime.today().strftime('%Y-%m-%d') + '.json'


        # 1成功0失败
        # result=uploadfile(ftp_host, ftp_username, ftp_password,ftp_path, filenametosave, os.getcwd())
        # print result

    def process_item(self, item, spider):
        if isinstance(item, DceChicangItem):
            self.exporter.export_item(item)
        return item


class DcePinzhongChicangSave(object):
    def __init__(self):
        self.storage = DcePinzhongChicangStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, DcePinzhongChicangItem):
            if not self.storage.exist(item):
                self.storage.save(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')
        return item


class DceMemberSave(object):
    def __init__(self):
        self.storage = DceMemberStorage(get_project_settings().get('DATABASE'))

    def process_item(self, item, spider):
        if isinstance(item, DceMemberItem):
            if not self.storage.exist(item):
                self.storage.save(item)
                spider.crawler.stats.inc_value('spiderlog/save_count')
        return item
