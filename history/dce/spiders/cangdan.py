# -*- coding: utf-8 -*-
import scrapy
from dce.items import DceCangdanItem
import re
import datetime
from scrapy.utils.project import get_project_settings
import logging
import urllib

logger = logging.getLogger(__name__)
class CangdanSpider(scrapy.Spider):
    name = "cangdan"
    allowed_domains = ["dce.com.cn"]
    start_urls = (
        'http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html',
    )

    ignore_page_incremental = True

    def start_requests(self):
        settings = get_project_settings()
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
            
    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'大商所-仓单日报')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_DCE_BILL_INPUT'])        
        url = 'http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html'

        date = datetime.date.today()
        while date > datetime.date(2016,11,11):
            logger.info(date)

            post_data = {
                'wbillWeeklyQuotes.variety': 'all',
                'year': str(date.year),
                'month': str(date.month-1),
                'day': str(date.day),
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
            yield request
            date = date - datetime.timedelta(days=1)

    def extract_cell_text(self, cell):
        return cell.xpath('./text()').extract_first().replace(u'\xa0', '').strip()

    def parse_content(self, response):
        data_table = response.xpath('//div[@class="dataArea"]/table')[0]
        data_date_pattern = re.compile('(\d{4}\d{2}\d{2})')
        curr_date_str = response.xpath('//input[@id="currDate"]/@value').extract_first()
        logger.info(curr_date_str)
        data_date = data_date_pattern.search(curr_date_str).group(1)
        title = '大连商品交易所 仓单日报'

        data_rows = data_table.xpath('./tr')[1:]
        if len(data_rows) <=1:
            logger.info('没有数据')
            return

        for row in data_rows:
            cells = row.xpath('./td')
            item = DceCangdanItem()

            product_name = self.extract_cell_text(cells[0])
            warehouse = self.extract_cell_text(cells[1])
            last_bill = self.extract_cell_text(cells[2])
            today_open_bill = self.extract_cell_text(cells[3])
            today_close_bill = self.extract_cell_text(cells[4])
            today_total_bill = self.extract_cell_text(cells[5])
            bill_change = self.extract_cell_text(cells[6])

            item['product_name'] = product_name
            item['release_date'] = data_date
            item['warehouse'] = warehouse
            item['last_bill'] = last_bill
            item['today_open_bill'] = today_open_bill
            item['today_close_bill'] = today_close_bill
            item['today_total_bill'] = today_total_bill
            item['bill_change'] = bill_change
            item['data_date'] = data_date
            item['datetime_stamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['title'] = title
            yield item

