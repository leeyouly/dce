
# -*- coding: utf-8 -*-
import unittest
from scrapy.http import HtmlResponse
from dce.spiders.cangdan import CangdanSpider
import os
import logging

class CangdanSpiderTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.target = CangdanSpider()
        
    def test_parse(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        data_file_path = os.path.join(dir, 'pages/cangdan_20160314.html')
        f = open(data_file_path)
        html_content = f.read()
        f.close()
        page_url = 'http://www.dce.com.cn/PublicWeb/MainServlet'
        response = HtmlResponse(url=page_url, body=html_content)
        items = self.target.parse_content(response)
        title = u'大连商品交易所 仓单日报'
        items = list(items)
        self.assertEqual(len(items), 30)
        
        self.assertEqual(items[0]['product_name'], u'豆一')
        self.assertEqual(items[0]['release_date'], u'20160314')
        self.assertEqual(items[0]['warehouse'], u'北安直属库')
        self.assertEqual(items[0]['last_bill'], u'1,700')
        self.assertEqual(items[0]['today_open_bill'], u'0')
        self.assertEqual(items[0]['today_close_bill'], u'0')
        self.assertEqual(items[0]['today_total_bill'], u'1,700')
        self.assertEqual(items[0]['bill_change'], u'0')
        self.assertEqual(items[0]['data_date'], u'20160314')
        self.assertEqual(items[0]['title'], title)
        self.assertIsNotNone(items[0]['datetime_stamp'])

        self.assertEqual(items[1]['product_name'], u'豆一')
        self.assertEqual(items[1]['release_date'], u'20160314')
        self.assertEqual(items[1]['warehouse'], u'北良港')
        self.assertEqual(items[1]['last_bill'], u'1,816')
        self.assertEqual(items[1]['today_open_bill'], u'0')
        self.assertEqual(items[1]['today_close_bill'], u'0')
        self.assertEqual(items[1]['today_total_bill'], u'1,816')
        self.assertEqual(items[1]['bill_change'], u'0')
        self.assertEqual(items[1]['data_date'], u'20160314')
        self.assertEqual(items[1]['title'], title)
        self.assertIsNotNone(items[1]['datetime_stamp'])

        self.assertEqual(items[2]['product_name'], u'豆一')
        self.assertEqual(items[2]['release_date'], u'20160314')
        self.assertEqual(items[2]['warehouse'], u'大连直属库')
        self.assertEqual(items[2]['last_bill'], u'1,744')
        self.assertEqual(items[2]['today_open_bill'], u'0')
        self.assertEqual(items[2]['today_close_bill'], u'0')
        self.assertEqual(items[2]['today_total_bill'], u'1,744')
        self.assertEqual(items[2]['bill_change'], u'0')
        self.assertEqual(items[2]['data_date'], u'20160314')
        self.assertEqual(items[2]['title'], title)
        self.assertIsNotNone(items[2]['datetime_stamp'])

        self.assertEqual(items[3]['product_name'], u'豆一')
        self.assertEqual(items[3]['release_date'], u'20160314')
        self.assertEqual(items[3]['warehouse'], u'哈尔滨益海')
        self.assertEqual(items[3]['last_bill'], u'6,009')
        self.assertEqual(items[3]['today_open_bill'], u'0')
        self.assertEqual(items[3]['today_close_bill'], u'0')
        self.assertEqual(items[3]['today_total_bill'], u'6,009')
        self.assertEqual(items[3]['bill_change'], u'0')
        self.assertEqual(items[3]['data_date'], u'20160314')
        self.assertEqual(items[3]['title'], title)
        self.assertIsNotNone(items[3]['datetime_stamp'])

        self.assertEqual(items[4]['product_name'], u'豆一')
        self.assertEqual(items[4]['release_date'], u'20160314')
        self.assertEqual(items[4]['warehouse'], u'哈尔滨直属库')
        self.assertEqual(items[4]['last_bill'], u'2,511')
        self.assertEqual(items[4]['today_open_bill'], u'0')
        self.assertEqual(items[4]['today_close_bill'], u'0')
        self.assertEqual(items[4]['today_total_bill'], u'2,511')
        self.assertEqual(items[4]['bill_change'], u'0')
        self.assertEqual(items[4]['data_date'], u'20160314')
        self.assertEqual(items[4]['title'], title)
        self.assertIsNotNone(items[4]['datetime_stamp'])

        self.assertEqual(items[5]['product_name'], u'豆一')
        self.assertEqual(items[5]['release_date'], u'20160314')
        self.assertEqual(items[5]['warehouse'], u'良运库')
        self.assertEqual(items[5]['last_bill'], u'3,280')
        self.assertEqual(items[5]['today_open_bill'], u'0')
        self.assertEqual(items[5]['today_close_bill'], u'298')
        self.assertEqual(items[5]['today_total_bill'], u'2,982')
        self.assertEqual(items[5]['bill_change'], u'-298')
        self.assertEqual(items[5]['data_date'], u'20160314')
        self.assertEqual(items[5]['title'], title)
        self.assertIsNotNone(items[5]['datetime_stamp'])

        self.assertEqual(items[6]['product_name'], u'豆一')
        self.assertEqual(items[6]['release_date'], u'20160314')
        self.assertEqual(items[6]['warehouse'], u'辽粮库')
        self.assertEqual(items[6]['last_bill'], u'1,735')
        self.assertEqual(items[6]['today_open_bill'], u'0')
        self.assertEqual(items[6]['today_close_bill'], u'0')
        self.assertEqual(items[6]['today_total_bill'], u'1,735')
        self.assertEqual(items[6]['bill_change'], u'0')
        self.assertEqual(items[6]['data_date'], u'20160314')
        self.assertEqual(items[6]['title'], title)
        self.assertIsNotNone(items[6]['datetime_stamp'])

        self.assertEqual(items[7]['product_name'], u'豆一')
        self.assertEqual(items[7]['release_date'], u'20160314')
        self.assertEqual(items[7]['warehouse'], u'绥棱直属库')
        self.assertEqual(items[7]['last_bill'], u'3,892')
        self.assertEqual(items[7]['today_open_bill'], u'0')
        self.assertEqual(items[7]['today_close_bill'], u'0')
        self.assertEqual(items[7]['today_total_bill'], u'3,892')
        self.assertEqual(items[7]['bill_change'], u'0')
        self.assertEqual(items[7]['data_date'], u'20160314')
        self.assertEqual(items[7]['title'], title)
        self.assertIsNotNone(items[7]['datetime_stamp'])

        self.assertEqual(items[8]['product_name'], u'豆一')
        self.assertEqual(items[8]['release_date'], u'20160314')
        self.assertEqual(items[8]['warehouse'], u'维维东北公司')
        self.assertEqual(items[8]['last_bill'], u'800')
        self.assertEqual(items[8]['today_open_bill'], u'0')
        self.assertEqual(items[8]['today_close_bill'], u'0')
        self.assertEqual(items[8]['today_total_bill'], u'800')
        self.assertEqual(items[8]['bill_change'], u'0')
        self.assertEqual(items[8]['data_date'], u'20160314')
        self.assertEqual(items[8]['title'], title)
        self.assertIsNotNone(items[8]['datetime_stamp'])

        self.assertEqual(items[9]['product_name'], u'豆一小计')
        self.assertEqual(items[9]['release_date'], u'')
        self.assertEqual(items[9]['warehouse'], u'')
        self.assertEqual(items[9]['last_bill'], u'23,487')
        self.assertEqual(items[9]['today_open_bill'], u'0')
        self.assertEqual(items[9]['today_close_bill'], u'298')
        self.assertEqual(items[9]['today_total_bill'], u'23,189')
        self.assertEqual(items[9]['bill_change'], u'-298')
        self.assertEqual(items[9]['data_date'], u'20160314')
        self.assertEqual(items[9]['title'], title)
        self.assertIsNotNone(items[9]['datetime_stamp'])

        self.assertEqual(items[10]['product_name'], u'玉米')
        self.assertEqual(items[10]['release_date'], u'20160314')
        self.assertEqual(items[10]['warehouse'], u'大连中船')
        self.assertEqual(items[10]['last_bill'], u'150')
        self.assertEqual(items[10]['today_open_bill'], u'0')
        self.assertEqual(items[10]['today_close_bill'], u'0')
        self.assertEqual(items[10]['today_total_bill'], u'150')
        self.assertEqual(items[10]['bill_change'], u'0')
        self.assertEqual(items[10]['data_date'], u'20160314')
        self.assertEqual(items[10]['title'], title)
        self.assertIsNotNone(items[10]['datetime_stamp'])

        self.assertEqual(items[11]['product_name'], u'玉米小计')
        self.assertEqual(items[11]['release_date'], u'')
        self.assertEqual(items[11]['warehouse'], u'')
        self.assertEqual(items[11]['last_bill'], u'150')
        self.assertEqual(items[11]['today_open_bill'], u'0')
        self.assertEqual(items[11]['today_close_bill'], u'0')
        self.assertEqual(items[11]['today_total_bill'], u'150')
        self.assertEqual(items[11]['bill_change'], u'0')
        self.assertEqual(items[11]['data_date'], u'20160314')
        self.assertEqual(items[11]['title'], title)
        self.assertIsNotNone(items[11]['datetime_stamp'])

        self.assertEqual(items[12]['product_name'], u'玉米淀粉')
        self.assertEqual(items[12]['release_date'], u'20160314')
        self.assertEqual(items[12]['warehouse'], u'德清金玉米')
        self.assertEqual(items[12]['last_bill'], u'0')
        self.assertEqual(items[12]['today_open_bill'], u'18')
        self.assertEqual(items[12]['today_close_bill'], u'0')
        self.assertEqual(items[12]['today_total_bill'], u'18')
        self.assertEqual(items[12]['bill_change'], u'18')
        self.assertEqual(items[12]['data_date'], u'20160314')
        self.assertEqual(items[12]['title'], title)
        self.assertIsNotNone(items[12]['datetime_stamp'])

        self.assertEqual(items[13]['product_name'], u'玉米淀粉小计')
        self.assertEqual(items[13]['release_date'], u'')
        self.assertEqual(items[13]['warehouse'], u'')
        self.assertEqual(items[13]['last_bill'], u'0')
        self.assertEqual(items[13]['today_open_bill'], u'18')
        self.assertEqual(items[13]['today_close_bill'], u'0')
        self.assertEqual(items[13]['today_total_bill'], u'18')
        self.assertEqual(items[13]['bill_change'], u'18')
        self.assertEqual(items[13]['data_date'], u'20160314')
        self.assertEqual(items[13]['title'], title)
        self.assertIsNotNone(items[13]['datetime_stamp'])

        self.assertEqual(items[14]['product_name'], u'纤维板')
        self.assertEqual(items[14]['release_date'], u'20160314')
        self.assertEqual(items[14]['warehouse'], u'常州奔牛港')
        self.assertEqual(items[14]['last_bill'], u'10')
        self.assertEqual(items[14]['today_open_bill'], u'0')
        self.assertEqual(items[14]['today_close_bill'], u'0')
        self.assertEqual(items[14]['today_total_bill'], u'10')
        self.assertEqual(items[14]['bill_change'], u'0')
        self.assertEqual(items[14]['data_date'], u'20160314')
        self.assertEqual(items[14]['title'], title)
        self.assertIsNotNone(items[14]['datetime_stamp'])

        self.assertEqual(items[15]['product_name'], u'纤维板小计')
        self.assertEqual(items[15]['release_date'], u'')
        self.assertEqual(items[15]['warehouse'], u'')
        self.assertEqual(items[15]['last_bill'], u'10')
        self.assertEqual(items[15]['today_open_bill'], u'0')
        self.assertEqual(items[15]['today_close_bill'], u'0')
        self.assertEqual(items[15]['today_total_bill'], u'10')
        self.assertEqual(items[15]['bill_change'], u'0')
        self.assertEqual(items[15]['data_date'], u'20160314')
        self.assertEqual(items[15]['title'], title)
        self.assertIsNotNone(items[15]['datetime_stamp'])

        self.assertEqual(items[16]['product_name'], u'焦炭')
        self.assertEqual(items[16]['release_date'], u'20160314')
        self.assertEqual(items[16]['warehouse'], u'山东铁雄')
        self.assertEqual(items[16]['last_bill'], u'0')
        self.assertEqual(items[16]['today_open_bill'], u'10')
        self.assertEqual(items[16]['today_close_bill'], u'0')
        self.assertEqual(items[16]['today_total_bill'], u'10')
        self.assertEqual(items[16]['bill_change'], u'10')
        self.assertEqual(items[16]['data_date'], u'20160314')
        self.assertEqual(items[16]['title'], title)
        self.assertIsNotNone(items[16]['datetime_stamp'])

        self.assertEqual(items[17]['product_name'], u'焦炭小计')
        self.assertEqual(items[17]['release_date'], u'')
        self.assertEqual(items[17]['warehouse'], u'')
        self.assertEqual(items[17]['last_bill'], u'0')
        self.assertEqual(items[17]['today_open_bill'], u'10')
        self.assertEqual(items[17]['today_close_bill'], u'0')
        self.assertEqual(items[17]['today_total_bill'], u'10')
        self.assertEqual(items[17]['bill_change'], u'10')
        self.assertEqual(items[17]['data_date'], u'20160314')
        self.assertEqual(items[17]['title'], title)
        self.assertIsNotNone(items[17]['datetime_stamp'])

        self.assertEqual(items[18]['product_name'], u'鸡蛋')
        self.assertEqual(items[18]['release_date'], u'20160314')
        self.assertEqual(items[18]['warehouse'], u'德州和膳')
        self.assertEqual(items[18]['last_bill'], u'0')
        self.assertEqual(items[18]['today_open_bill'], u'3')
        self.assertEqual(items[18]['today_close_bill'], u'0')
        self.assertEqual(items[18]['today_total_bill'], u'3')
        self.assertEqual(items[18]['bill_change'], u'3')
        self.assertEqual(items[18]['data_date'], u'20160314')
        self.assertEqual(items[18]['title'], title)
        self.assertIsNotNone(items[18]['datetime_stamp'])

        self.assertEqual(items[19]['product_name'], u'鸡蛋')
        self.assertEqual(items[19]['release_date'], u'20160314')
        self.assertEqual(items[19]['warehouse'], u'石家庄双鸽')
        self.assertEqual(items[19]['last_bill'], u'0')
        self.assertEqual(items[19]['today_open_bill'], u'1')
        self.assertEqual(items[19]['today_close_bill'], u'0')
        self.assertEqual(items[19]['today_total_bill'], u'1')
        self.assertEqual(items[19]['bill_change'], u'1')
        self.assertEqual(items[19]['data_date'], u'20160314')
        self.assertEqual(items[19]['title'], title)
        self.assertIsNotNone(items[19]['datetime_stamp'])

        self.assertEqual(items[20]['product_name'], u'鸡蛋小计')
        self.assertEqual(items[20]['release_date'], u'')
        self.assertEqual(items[20]['warehouse'], u'')
        self.assertEqual(items[20]['last_bill'], u'0')
        self.assertEqual(items[20]['today_open_bill'], u'4')
        self.assertEqual(items[20]['today_close_bill'], u'0')
        self.assertEqual(items[20]['today_total_bill'], u'4')
        self.assertEqual(items[20]['bill_change'], u'4')
        self.assertEqual(items[20]['data_date'], u'20160314')
        self.assertEqual(items[20]['title'], title)
        self.assertIsNotNone(items[20]['datetime_stamp'])

        self.assertEqual(items[21]['product_name'], u'豆粕')
        self.assertEqual(items[21]['release_date'], u'20160314')
        self.assertEqual(items[21]['warehouse'], u'东莞富之源')
        self.assertEqual(items[21]['last_bill'], u'78')
        self.assertEqual(items[21]['today_open_bill'], u'0')
        self.assertEqual(items[21]['today_close_bill'], u'78')
        self.assertEqual(items[21]['today_total_bill'], u'0')
        self.assertEqual(items[21]['bill_change'], u'-78')
        self.assertEqual(items[21]['data_date'], u'20160314')
        self.assertEqual(items[21]['title'], title)
        self.assertIsNotNone(items[21]['datetime_stamp'])

        self.assertEqual(items[22]['product_name'], u'豆粕')
        self.assertEqual(items[22]['release_date'], u'20160314')
        self.assertEqual(items[22]['warehouse'], u'东莞嘉吉')
        self.assertEqual(items[22]['last_bill'], u'451')
        self.assertEqual(items[22]['today_open_bill'], u'0')
        self.assertEqual(items[22]['today_close_bill'], u'0')
        self.assertEqual(items[22]['today_total_bill'], u'451')
        self.assertEqual(items[22]['bill_change'], u'0')
        self.assertEqual(items[22]['data_date'], u'20160314')
        self.assertEqual(items[22]['title'], title)
        self.assertIsNotNone(items[22]['datetime_stamp'])

        self.assertEqual(items[23]['product_name'], u'豆粕')
        self.assertEqual(items[23]['release_date'], u'20160314')
        self.assertEqual(items[23]['warehouse'], u'南通嘉吉')
        self.assertEqual(items[23]['last_bill'], u'3,750')
        self.assertEqual(items[23]['today_open_bill'], u'0')
        self.assertEqual(items[23]['today_close_bill'], u'0')
        self.assertEqual(items[23]['today_total_bill'], u'3,750')
        self.assertEqual(items[23]['bill_change'], u'0')
        self.assertEqual(items[23]['data_date'], u'20160314')
        self.assertEqual(items[23]['title'], title)
        self.assertIsNotNone(items[23]['datetime_stamp'])

        self.assertEqual(items[24]['product_name'], u'豆粕')
        self.assertEqual(items[24]['release_date'], u'20160314')
        self.assertEqual(items[24]['warehouse'], u'南通来宝')
        self.assertEqual(items[24]['last_bill'], u'2,829')
        self.assertEqual(items[24]['today_open_bill'], u'0')
        self.assertEqual(items[24]['today_close_bill'], u'0')
        self.assertEqual(items[24]['today_total_bill'], u'2,829')
        self.assertEqual(items[24]['bill_change'], u'0')
        self.assertEqual(items[24]['data_date'], u'20160314')
        self.assertEqual(items[24]['title'], title)
        self.assertIsNotNone(items[24]['datetime_stamp'])

        self.assertEqual(items[25]['product_name'], u'豆粕小计')
        self.assertEqual(items[25]['release_date'], u'')
        self.assertEqual(items[25]['warehouse'], u'')
        self.assertEqual(items[25]['last_bill'], u'7,108')
        self.assertEqual(items[25]['today_open_bill'], u'0')
        self.assertEqual(items[25]['today_close_bill'], u'78')
        self.assertEqual(items[25]['today_total_bill'], u'7,030')
        self.assertEqual(items[25]['bill_change'], u'-78')
        self.assertEqual(items[25]['data_date'], u'20160314')
        self.assertEqual(items[25]['title'], title)
        self.assertIsNotNone(items[25]['datetime_stamp'])

        self.assertEqual(items[26]['product_name'], u'豆油')
        self.assertEqual(items[26]['release_date'], u'20160314')
        self.assertEqual(items[26]['warehouse'], u'连云港益海')
        self.assertEqual(items[26]['last_bill'], u'142')
        self.assertEqual(items[26]['today_open_bill'], u'0')
        self.assertEqual(items[26]['today_close_bill'], u'0')
        self.assertEqual(items[26]['today_total_bill'], u'142')
        self.assertEqual(items[26]['bill_change'], u'0')
        self.assertEqual(items[26]['data_date'], u'20160314')
        self.assertEqual(items[26]['title'], title)
        self.assertIsNotNone(items[26]['datetime_stamp'])

        self.assertEqual(items[27]['product_name'], u'豆油')
        self.assertEqual(items[27]['release_date'], u'20160314')
        self.assertEqual(items[27]['warehouse'], u'南通来宝')
        self.assertEqual(items[27]['last_bill'], u'723')
        self.assertEqual(items[27]['today_open_bill'], u'0')
        self.assertEqual(items[27]['today_close_bill'], u'0')
        self.assertEqual(items[27]['today_total_bill'], u'723')
        self.assertEqual(items[27]['bill_change'], u'0')
        self.assertEqual(items[27]['data_date'], u'20160314')
        self.assertEqual(items[27]['title'], title)
        self.assertIsNotNone(items[27]['datetime_stamp'])

        self.assertEqual(items[28]['product_name'], u'豆油小计')
        self.assertEqual(items[28]['release_date'], u'')
        self.assertEqual(items[28]['warehouse'], u'')
        self.assertEqual(items[28]['last_bill'], u'865')
        self.assertEqual(items[28]['today_open_bill'], u'0')
        self.assertEqual(items[28]['today_close_bill'], u'0')
        self.assertEqual(items[28]['today_total_bill'], u'865')
        self.assertEqual(items[28]['bill_change'], u'0')
        self.assertEqual(items[28]['data_date'], u'20160314')
        self.assertEqual(items[28]['title'], title)
        self.assertIsNotNone(items[28]['datetime_stamp'])

        self.assertEqual(items[29]['product_name'], u'总计')
        self.assertEqual(items[29]['release_date'], u'')
        self.assertEqual(items[29]['warehouse'], u'')
        self.assertEqual(items[29]['last_bill'], u'31,620')
        self.assertEqual(items[29]['today_open_bill'], u'32')
        self.assertEqual(items[29]['today_close_bill'], u'376')
        self.assertEqual(items[29]['today_total_bill'], u'31,276')
        self.assertEqual(items[29]['bill_change'], u'-344')
        self.assertEqual(items[29]['data_date'], u'20160314')
        self.assertEqual(items[29]['title'], title)
        self.assertIsNotNone(items[29]['datetime_stamp'])

