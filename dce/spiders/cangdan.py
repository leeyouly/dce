# -*- coding: utf-8 -*-
import scrapy
from dce.items import DceCangdanItem
import re
import datetime
from scrapy.utils.project import get_project_settings
from dce.data import TradingCalendarStorage
import logging
from dce.table import table_to_list

import urllib

logger = logging.getLogger(__name__)

last_update_date = datetime.datetime.now() - datetime.timedelta(days=100)
class CangdanSpider(scrapy.Spider):
    name = "cangdan"
    allowed_domains = ["dce.com.cn"]
    start_urls = (
        'http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html',
    )

    ignore_page_incremental = True

    def start_requests(self):
        settings = get_project_settings()
        tradingcalendarstorage = TradingCalendarStorage(settings.get('DATABASE'))
        
        tradingdaterecord = tradingcalendarstorage.get({
            'tradingcalendar': 'SSE', 
            'tradingday': datetime.date.today()
            })
        if not tradingdaterecord or tradingdaterecord['flag'] != 1:
            logger.info(u'非交易日，正在退出')
            return

        for url in self.start_urls:
            yield self.make_requests_from_url(url)
            
    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'大商所-仓单日报')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_DCE_BILL_INPUT'])        
        url = 'http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html'

        today = datetime.datetime.now()
        delta = datetime.timedelta(days=1)
        cal_date = today
        while cal_date > last_update_date:

            # str_cal_date = cal_date.strftime("%Y-%m-%d")

            # cal_date = datetime.date.today()
            logger.info(cal_date)

            post_data = {
                'wbillWeeklyQuotes.variety': 'all',
                'year': str(cal_date.year),
                'month': str(cal_date.month-1),
                'day': str(cal_date.day),
            }
            headers = {
                'Content-Type' : 'application/x-www-form-urlencoded',
            }
            request = scrapy.http.FormRequest.from_response(response=response,
                                            formname='wbillWeeklyQuotesForm',
                                            method='POST',
                                            formdata=post_data,
                                            headers = headers,
                                            callback = self.parse_content)
            cal_date = cal_date - delta
            yield request
            # return [request]

    def extract_cell_text(self, cell):
        return cell.xpath('./text()').extract_first().replace(u'\xa0', '').strip()

    def parse_content(self, response):
        data_table = response.xpath('//div[@class="dataArea"]/table')[0]
        data_date_pattern = re.compile('(\d{4}\d{2}\d{2})')
        curr_date_str = response.xpath('//input[@id="currDate"]/@value').extract_first()
        logger.info(curr_date_str)
        data_date = data_date_pattern.search(curr_date_str).group(1)
        title = '大连商品交易所 仓单日报'

        data_table = response.xpath('//div[@class="main"]/table')
        data_table = response.xpath('//*[@id="printData"]/div/table')
        data_list = table_to_list(data_table)

        index = 1
        for data in data_list[1:]:

            item = DceCangdanItem()
            item['release_date'] = data_date
            item['data_date'] = data_date
            item['last_bill'] = data[2].replace(',','')
            item['today_total_bill'] = data[3].replace(',','')
            item['bill_change'] = data[4].replace(',','')
            item['datetime_stamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['title'] = title
            item['product_name'] = data[0]
            item['warehouse'] = data[1]
            if u'总计' in data[0] or  u'小计' in data[0]:
                item['warehouse'] = data[0]
            elif '' == data[0]:
                item['product_name'] = data_list[index-1][0]
                if '' == data_list[index-1][0]:
                    item['product_name'] = data_list[index - 2][0]
            index = index + 1
            yield item

