# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from dce.items import DceDailyItem
import logging
from scrapy.utils.project import get_project_settings
from dce.data import TradingCalendarStorage

logger = logging.getLogger(__name__)

class DailySpider(scrapy.Spider):
    name = "daily"
    allowed_domains = ["dce.com.cn"]
    start_urls = (
        'http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html',
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
        self.crawler.stats.set_value('spiderlog/source_name', u'大商所-日行情')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_MARKET_DCE_DAY'])

        date = datetime.datetime.now()
        #date = date.replace(year=2016, month=11, day=14)

        request = scrapy.http.FormRequest.from_response(response,
                                                        formname='dayQuotesForm',
                                                        formdata={
                                                            'year': str(date.year),
                                                            'month': str(date.month - 1),
                                                            'day': str(date.day)
                                                        }, callback=self.parse_content)
        return request



    def parse_content(self, response):
        #logging.debug(response.body)
        title = response.xpath('//div[@class="tradeResult02"]/p/text()').extract_first()
        title2 = response.xpath('//div[@class="tradeResult02"]/p/span/text()').extract_first()
        logging.debug(title)
        logging.debug(title2)

        trading_dt_pattern = re.compile('(\d{8})')
        datestr = response.xpath('//input[@id="currDate"]/@value').extract_first()
        logging.debug(datestr)
        trading_dt_match = trading_dt_pattern.search(datestr)
        if not trading_dt_match:
            logging.warn(u'获取数据日期失败')
            return
        trading_dt = trading_dt_match.group(1)

        data_table = response.xpath('//div[@class="dataArea"]/table')[0]
        for row in data_table.xpath('./tr')[1:]:
            cells = row.xpath('./td')
            item = DceDailyItem()
            item['title']=title
            item['trade_name'] = cells[0].xpath('./text()').extract_first().strip()
            item['delivery_mon'] = cells[1].xpath('./text()').extract_first().replace(u'\xa0','').strip()
            item['open_price'] = cells[2].xpath('./text()').extract_first().replace(u'\xa0','').strip()
            item['high_price'] = cells[3].xpath('./text()').extract_first().replace(u'\xa0','').strip()
            item['low_price'] = cells[4].xpath('./text()').extract_first().replace(u'\xa0','').strip()
            item['close_price'] = cells[5].xpath('./text()').extract_first().replace(u'\xa0','').strip()
            item['pre_settlement_price'] = cells[6].xpath('./text()').extract_first().replace(u'\xa0','').strip()
            item['settlement_price'] = cells[7].xpath('./text()').extract_first().replace(u'\xa0','').strip()
            item['rise_offset'] = cells[8].xpath('./text()').extract_first().replace(u'\xa0','').strip()
            item['rise_offset_1'] = cells[9].xpath('./text()').extract_first().replace(u'\xa0','').strip()
            item['trading_vol'] = cells[10].xpath('./text()').extract_first().strip()
            item['position_vol'] = cells[11].xpath('./text()').extract_first().strip()
            item['position_chg_vol'] = cells[12].xpath('./text()').extract_first().strip()
            item['trading_amount'] = cells[13].xpath('./text()').extract_first().strip()
            item['trading_dt'] = trading_dt
            item['datetime_stamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item
