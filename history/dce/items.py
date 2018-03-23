# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DceDailyItem(scrapy.Item):
    title = scrapy.Field()
    trade_name = scrapy.Field()
    delivery_mon = scrapy.Field()
    open_price = scrapy.Field()
    high_price = scrapy.Field()
    low_price = scrapy.Field()
    close_price = scrapy.Field()
    pre_settlement_price = scrapy.Field()
    settlement_price = scrapy.Field()
    rise_offset = scrapy.Field()
    rise_offset_1 = scrapy.Field()
    trading_vol = scrapy.Field()
    position_vol = scrapy.Field()
    position_chg_vol = scrapy.Field()
    trading_amount = scrapy.Field()
    trading_dt = scrapy.Field()
    datetime_stamp = scrapy.Field()

class DceCangdanItem(scrapy.Item):
    product_name = scrapy.Field()
    release_date = scrapy.Field()
    warehouse = scrapy.Field()
    last_bill = scrapy.Field()
    today_open_bill = scrapy.Field()
    today_close_bill = scrapy.Field()
    today_total_bill = scrapy.Field()
    bill_change = scrapy.Field()
    data_date = scrapy.Field()
    datetime_stamp = scrapy.Field()
    title = scrapy.Field()

class DceChicangItem(scrapy.Item):
    datadate = scrapy.Field()
    instrumentid = scrapy.Field()
    datatype = scrapy.Field()
    rank = scrapy.Field()
    account = scrapy.Field()
    vol = scrapy.Field()
    chg = scrapy.Field()

class DceMemberItem(scrapy.Item):
    datadate = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    short_name = scrapy.Field()
    address = scrapy.Field()
    website = scrapy.Field()
    phone = scrapy.Field()
