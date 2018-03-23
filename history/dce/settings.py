# -*- coding: utf-8 -*-

# Scrapy settings for dce project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'dce'

SPIDER_MODULES = ['dce.spiders']
NEWSPIDER_MODULE = 'dce.spiders'


ITEM_PIPELINES = {

}
LOG_LEVEL = 'INFO'


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
SPIDER_MIDDLEWARES = {
}
EXTENSIONS = {
}
DOWNLOAD_DELAY=1
