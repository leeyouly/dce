# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.utils.project import get_project_settings
import os
from zipfile import ZipFile
import re
import shutil
from dce.items import DceChicangItem
import logging
from cStringIO import StringIO
from urllib import urlencode


class ChicangSpider(scrapy.Spider):
    name = "chicang2"
    allowed_domains = ["www.dce.com.cn"]
    start_urls = (
        'http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html',
    )

    settings = get_project_settings()

    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'大商所-持仓排名')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_MT_DCE_POSITION'])

        date = datetime.date.today()
        start_date = datetime.date(2014,1,1)
        end_date = datetime.date(2014,12,31)
        for i in range((end_date-start_date).days+1):
            date = start_date + datetime.timedelta(days=i)
            for variaty_input in response.xpath('//div[@class="selBox"]//input[@type="radio"]'):
                variaty_onclick = variaty_input.xpath('./@onclick').extract_first()
                if variaty_onclick and 'setVariety' in variaty_onclick:
                    m = re.search('setVariety\(\'(\w+)\'\)', variaty_onclick)
                    variaty_code = m.group(1)
                    logging.debug(variaty_code)

                request = scrapy.http.FormRequest.from_response(response=response,
                                                                formdata={'memberDealPosiQuotes.variety':variaty_code,
                                                                          'memberDealPosiQuotes.trade_type':'0',
                                                                          'contract.contract_id': 'all',
                                                                          'contract.variety_id':variaty_code,
                                                                          'year': str(date.year),
                                                                          'month': str(date.month - 1),
                                                                          'day': str(date.day),
                                                                          },
                                                                meta={'date': date},
                                                                callback=self.parse_variaty_page)

                yield request

    def parse_variaty_page(self, response):
        variaty_code = response.xpath('//input[@name="memberDealPosiQuotes.variety"]/@value').extract_first()
        date = response.meta['date']

        for input in response.xpath('//div[@class="selBox"]//input[@type="radio"]'):
            input_onclick = input.xpath('./@onclick').extract_first()

            if input_onclick and 'setContract_id' in input_onclick:
                m = re.search('setContract_id\(\'(\w+)\'\)', input_onclick)
                contract_id = m.group(1)
                logging.debug('%s %s' % (variaty_code, contract_id))
                request = scrapy.http.FormRequest.from_response(response=response,
                                                                formname='exportForm',
                                                                formdata={
                                                                            'contract.contract_id': contract_id,
                                                                            'exportFlag':'txt',
                                                                          'year': str(date.year),
                                                                          'month': str(date.month - 1),
                                                                          'day': str(date.day),
                                                                          },
                                                                callback=self.parse_content)
                yield request

    def parse_content(self, response):
        symbol = None
        datadate = None

        f = StringIO(response.body)
        for title_line in f:
            title_line = title_line.decode('utf8')
            title_pattern = re.compile(u'合约代码：(\w+)\s*Date：(\d{4})(\d{2})(\d{2})')
            m = title_pattern.search(title_line)
            if m:
                symbol = m.group(1)
                datadate = datetime.date(int(m.group(2)), int(m.group(3)), int(m.group(4)))
                break
        if symbol is None or datadate is None:
            logging.warn(u'无法获取合约代码和交易日期')
            return

        current_datatype = None
        for line in f:
            line = line.decode('utf8')
            m_datatype = re.search(u'名次\s+会员简称\s+(成交量|持买单量|持卖单量)', line)
            if m_datatype:
                current_datatype = m_datatype.group(1)
                continue

            m_datarow = re.search('(\d+)\s+(\S+)\s+([\d,]+)\s+([-\d,]+)', line)
            if m_datarow:
                item = DceChicangItem()
                item['datadate'] = datadate
                item['instrumentid'] = symbol
                item['datatype'] = current_datatype
                item['rank'] = m_datarow.group(1)
                item['account'] = m_datarow.group(2)
                item['vol'] = int(m_datarow.group(3).replace(',', ''))
                item['chg'] = int(m_datarow.group(4).replace(',', ''))
                yield item
