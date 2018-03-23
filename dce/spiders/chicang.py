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
from urllib import urlencode

class ChicangSpider(scrapy.Spider):
    name = "chicang"
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
        #date = date.replace(year=2016, month=11, day=11)
        url = 'http://www.dce.com.cn/publicweb/quotesdata/exportMemberDealPosiQuotesBatchData.html'
        post_data = {
            'memberDealPosiQuotes.variety':'b',
            'memberDealPosiQuotes.trade_type':'0',
            'contract.contract_id':'all',
            'contract.variety_id':'b',
            'year':date.year,
            'month':date.month-1,
            'day':date.day,
            'batchExportFlag':'batch',
        }
        logging.debug(urlencode(post_data))
        request= scrapy.Request(url,
                                method='POST',
                                body=urlencode(post_data),
                                callback=self.download_package,
                                headers={'Content-Type':'application/x-www-form-urlencoded'},
                                meta={'date': date},
        )

        return [request]

    def download_package(self, response):
        if 'Content-Disposition' not in response.headers:
            logging.info('No Content-Disposition header found.')
            logging.info(response.headers)
            logging.info(response.body)
            return
        logging.debug('Header-Content-Disposition' + response.headers['Content-Disposition'])
        zip_file_path = self.save_file(response)
        extract_dir = self.extract_files(zip_file_path)
        for dirpath, dirnames, filenames in os.walk(extract_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                for item in self.extract_data_from_file(filepath):
                    yield item

    def extract_data_from_file(self, file_path):
        symbol = None
        datadate = None
        f = open(file_path, 'r')
        for title_line in f:
            title_line = title_line.decode('utf8')
            title_pattern = re.compile(u'合约代码：(\w+)\s*Date：(\d{4})-(\d{2})-(\d{2})')
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

            m_datarow = re.search('(\d+)\s+(\S+)\s+(\d+)\s+([-\d]+)', line)
            if m_datarow:
                item = DceChicangItem()
                item['datadate'] = datadate
                item['instrumentid'] = symbol
                item['datatype'] = current_datatype
                item['rank'] = m_datarow.group(1)
                item['account'] = m_datarow.group(2)
                item['vol'] = m_datarow.group(3)
                item['chg'] = m_datarow.group(4)
                yield item





    def save_file(self, response):
        bot_nane = self.settings.get('BOT_NAME')
        spider_name = self.name

        tmp_dir = os.path.join('tmp', bot_nane, spider_name)
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        date = response.meta['date']
        file_name = date.strftime('%Y%m%d.zip')
        file_path = os.path.join(tmp_dir, file_name)
        logging.debug(file_path)

        with open(file_path, 'wb') as f:
            f.write(response.body)

        return file_path

    def extract_files(self, zip_file_path):
        bot_name = self.settings.get('BOT_NAME')
        spider_name = self.name

        file_base_name = os.path.basename(zip_file_path)
        file_root_name = os.path.splitext(file_base_name)[0]
        extract_dir = os.path.join('tmp', bot_name, spider_name, file_root_name)
        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)

        zip_file = ZipFile(zip_file_path)
        #zip_file.extractall(extract_dir)  直接解压中文文件名会报错
        for fileinfo in zip_file.filelist:
            filename = fileinfo.filename
            m = re.search('([a-zA-Z0-9_]+)', filename)
            output_filename = os.path.join(extract_dir, m.group(1) + '.txt')
            outputfile = open(output_filename, "wb")
            shutil.copyfileobj(zip_file.open(fileinfo.filename), outputfile)
            outputfile.close()

        return extract_dir