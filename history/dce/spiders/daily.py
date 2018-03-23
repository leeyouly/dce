# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from dce.items import DceDailyItem
import logging
from scrapy.utils.project import get_project_settings


logger = logging.getLogger(__name__)

class DailySpider(scrapy.Spider):
    name = "daily"
    allowed_domains = ["dce.com.cn"]
    start_urls = (
        'http://www.dce.com.cn/PublicWeb/MainServlet?action=Pu00011_search',
    )
    
    def start_requests(self):
        settings = get_project_settings()
            
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
            
    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'大商所-日行情')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_MARKET_DCE_DAY'])
        begin = datetime.date(2012,01,01)
        end = datetime.date(2013,01,01) 
        date = begin  
        delta = datetime.timedelta(days=1)  
        while date <= end:  
            url = 'http://www.dce.com.cn/PublicWeb/MainServlet?action=Pu00011_result&Pu00011_Input.trade_date={0}&Pu00011_Input.variety=all&Pu00011_Input.trade_type=0&Submit=%B2%E9+%D1%AF'.format(date.strftime('%Y%m%d'))
            logging.debug(url)
            request = scrapy.http.Request(url = url, 
                callback = self.parse_content)
            date += delta
            yield request

    def parse_content(self, response):
        #logging.debug(response.body)
        title = response.xpath('//div[@class="title"]/text()').extract_first()
        title2 = response.xpath('//div[@class="title2"]/text()').extract_first()
        logging.debug(title2)
        trading_dt_pattern = re.compile('(\d{8})')
        trading_dt_match = trading_dt_pattern.search(title2)
        if not trading_dt_match:
            logging.warn(u'获取数据日期失败')
            return
        trading_dt = trading_dt_match.group(1)

        data_table = response.xpath('//table[@class="table"]')[0]
        for row in data_table.xpath('./tr')[1:]:
            cells = row.xpath('./td')
            item = DceDailyItem()
            item['title']=title
            item['trade_name'] = cells[0].xpath('./text()').extract_first()
            item['delivery_mon'] = cells[1].xpath('./text()').extract_first().replace(u'\xa0','')
            item['open_price'] = cells[2].xpath('./text()').extract_first().replace(u'\xa0','')
            item['high_price'] = cells[3].xpath('./text()').extract_first().replace(u'\xa0','')
            item['low_price'] = cells[4].xpath('./text()').extract_first().replace(u'\xa0','')
            item['close_price'] = cells[5].xpath('./text()').extract_first().replace(u'\xa0','')
            item['pre_settlement_price'] = cells[6].xpath('./text()').extract_first().replace(u'\xa0','')
            item['settlement_price'] = cells[7].xpath('./text()').extract_first().replace(u'\xa0','')
            item['rise_offset'] = cells[8].xpath('./text()').extract_first().replace(u'\xa0','')
            item['rise_offset_1'] = cells[9].xpath('./text()').extract_first().replace(u'\xa0','')
            item['trading_vol'] = cells[10].xpath('./text()').extract_first()
            item['position_vol'] = cells[11].xpath('./text()').extract_first()
            item['position_chg_vol'] = cells[12].xpath('./text()').extract_first()
            item['trading_amount'] = cells[13].xpath('./text()').extract_first()
            item['trading_dt'] = trading_dt
            item['datetime_stamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item
