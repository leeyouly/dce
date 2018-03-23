# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.utils.project import get_project_settings
import os
from zipfile import ZipFile
import re
import shutil
from dce.items import DcePinzhongChicangItem
import logging
from cStringIO import StringIO
from urllib import urlencode


class ChicangSpider(scrapy.Spider):
    name = "pinzhong_chicang2"
    allowed_domains = ["www.dce.com.cn"]
    start_urls = (
        'http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html',
    )

    settings = get_project_settings()

    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'品种持仓')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_MT_DCE_POSITION_PZ'])
#         for i in range(0,22,1):
#             date = datetime.date.today()-datetime.timedelta(days=i)
        date = datetime.date.today()
        #date = date.replace(year=2016, month=12, day=5)
        for variaty_input in response.xpath('//div[@class="selBox"]//input[@type="radio"]'):
            variaty_onclick = variaty_input.xpath('./@onclick').extract_first()
            if variaty_onclick and 'setVariety' in variaty_onclick:
                m = re.search('setVariety\(\'(\w+)\'\)', variaty_onclick)
                variaty_code = m.group(1)
                logging.debug(variaty_code)

                request = scrapy.http.FormRequest.from_response(response=response,
                                                            formname='exportForm',
                                                            formdata={'memberDealPosiQuotes.variety':variaty_code,
                                                                      'memberDealPosiQuotes.trade_type':'0',
                                                                      'contract.contract_id': 'all',
                                                                      'contract.variety_id':variaty_code,
                                                                      'year': str(date.year),
                                                                      'month': str(date.month - 1),
                                                                      'day': str(date.day),
                                                                      'exportFlag':'txt',
                                                                      },
                                                            meta={'date': date},
                                                            callback=self.parse_content)

                yield request

    def parse_content(self, response):
        symbol = None
        datadate = None

        f = StringIO(response.body)
        for title_line in f:
            title_line = title_line.decode('utf8')
            title_pattern = re.compile(u'品种代码：(\w+)\s*Date：(\d{4})(\d{2})(\d{2})')
            m = title_pattern.search(title_line)
            if m:
                symbol = m.group(1)
                datadate = datetime.date(int(m.group(2)), int(m.group(3)), int(m.group(4)))
                break
        if symbol is None or datadate is None:
            logging.warn(u'无法获取品种代码和交易日期')
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
                item = DcePinzhongChicangItem()
                item['datadate'] = datadate
                item['pinzhongid'] = symbol
                item['datatype'] = current_datatype
                item['rank'] = m_datarow.group(1)
                item['account'] = m_datarow.group(2)
                item['vol'] = int(m_datarow.group(3).replace(',', ''))
                item['chg'] = int(m_datarow.group(4).replace(',', ''))
                yield item
