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

class ChicangSpider(scrapy.Spider):
    ignore_page_incremental = True
    name = "pinzhong_chicang"
    allowed_domains = ["www.dce.com.cn"]
    start_urls = (
        'http://www.dce.com.cn/PublicWeb/MainServlet?action=Pu00021_search',
    )

    settings = get_project_settings()

    def parse(self, response):
        self.crawler.stats.set_value('spiderlog/source_name', u'品种持仓')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_MT_DCE_POSITION_PZ'])
        pinzhongListBackup=[u'a',u'b',u'bb',u'c',u'cs',u'fb',u'i',u'j',u'jd',u'jm',u'l',u'm',u'p',u'pp',u'v',u'y',u's']
        pinzhongListOrigin=response.xpath('//*[@id="variety"]/option/@value').extract()
        
        if len(pinzhongListOrigin)<10:
            pinzhongList=pinzhongListBackup
            logging.error("pingzhong_chicang----get pinzhong id need to be changed!")
        else:
            pinzhongList=pinzhongListOrigin
            
        enddate = datetime.date.today() 
        
#         for i in range(len(pinzhongList)):
        datatypeList=[u'成交量',u'持买单量',u'持卖单量']
        for i in range(len(pinzhongList)):
            
#             '查询'b='查询'
#             unicodeData=b.decode('utf8')
#             gbkData ='查询'.decode('utf8').encode('gbk')
            url="http://www.dce.com.cn/PublicWeb/MainServlet"   
              
            for daysdelta in range(600):            
                
                querydate=enddate-datetime.timedelta(days=daysdelta)
                querydateStr=str(querydate).replace('-', '')
                for j in range(3):
                    query_post_data = {
                        'action':'Pu00021_result',
                        'Pu00021_Input.prefix':'',
                        'Pu00021_Input.trade_date':querydateStr,
                        'Pu00021_Input.content':str(j),
                        'Pu00021_Input.variety':pinzhongList[i],
                        'Pu00021_Input.trade_type':'0',
                        'Pu00021_Input.contract_id':'',
                        'Submit':'查询'.decode('utf8').encode('gbk')
                        }
                    request = scrapy.http.FormRequest(url, 
                        callback = self.getContent, 
                        formdata = query_post_data,
                        meta={'datadate':querydateStr,'datatype':datatypeList[j],'pinzhongid':pinzhongList[i]})
                            
                    yield request



    def getContent(self, response):
            try:
                datadate=response.meta['datadate']
                chichangItemTable=response.xpath('//table//table[1]//tr')
                item = DcePinzhongChicangItem()
                item['datadate']=datetime.datetime.strptime(datadate, "%Y%m%d").date()
                item['datatype']=response.meta['datatype']
                item['pinzhongid']=response.meta['pinzhongid']
                for i in range(1,len(chichangItemTable)):
                    item['rank']=0
                    datalist=chichangItemTable[i].xpath('./td/text()').extract()
                    item['account']=datalist[0].strip().replace(',','')
                    item['vol'] = int(datalist[1].strip().replace(',',''))
                    item['chg'] = int(datalist[2].strip().replace(',',''))
                    yield item
                
                    
                chichangItemTable=response.xpath('//table//table[2]//tr')
                for i in range(1,len(chichangItemTable)-1):
                    item['rank']=i
                    datalist=chichangItemTable[i].xpath('./td/text()').extract()
                    item['account']=datalist[1].strip().replace(',','')
                    item['vol'] = int(datalist[2].strip().replace(',',''))
                    item['chg'] = int(datalist[3].strip().replace(',',''))
                    yield item
            except:
                print 'pingzhong_chicang----datadate is'+item['datadate'].strftime("%Y-%m-%d")
                logging.error('pingzhong_chicang----datadate is'+item['datadate'].strftime("%Y-%m-%d"))
                return
          