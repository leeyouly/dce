# -*- coding: utf-8 -*-
import scrapy
from dce.items import DceMemberItem
import datetime

class HuiyuanSpider(scrapy.Spider):
    name = "huiyuan"
    allowed_domains = ["dce.com.cn"]
    start_urls = (
        'http://www.dce.com.cn/dalianshangpin/gywm7/jyshy/index.html',
    )
    ignore_page_incremental = True

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'大商所-会员')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_MT_DCE_MEMBERS'])

        request = scrapy.Request('http://www.dce.com.cn/publicweb/member/memberQuotes.html',
                                 callback=self.parse_content)
        return [request]

    def parse_content(self, response):
        datatable = response.xpath('//div[@class="dataArea"]/table')[0]
        datadate = datetime.date.today()
        for row in datatable.xpath('./tr')[1:]:
            cells = row.xpath('./td')
            item =DceMemberItem()
            item['datadate'] = datadate
            item['id'] = ''.join(cells[0].xpath('.//text()').extract()).strip()
            item['name'] = ''.join(cells[1].xpath('.//text()').extract()).strip()
            if cells[1].xpath('.//a'):
                item['website'] = cells[1].xpath('.//a/@href').extract_first()
            item['short_name'] = ''.join(cells[2].xpath('.//text()').extract()).strip()
            item['address'] = ''.join(cells[3].xpath('.//text()').extract()).strip()
            item['phone'] = ''.join(cells[4].xpath('.//text()').extract()).strip()
            yield item
