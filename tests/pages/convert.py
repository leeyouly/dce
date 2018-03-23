# -*- coding: utf8 -*-
import csv

filename = 'data.csv'
output = 'data.py.txt'
f = open(filename, 'rb')
fw = open(output, 'wb')
reader = csv.reader(f)
row_index = 0
for row in reader:
    rowdata = {
        'title' : u'大连商品交易所 日行情表'.encode('utf8'),
        'trade_name' : unicode(row[0], 'utf8').encode('utf8'),
        'delivery_mon' : row[1],
        'open_price': row[2],
        'high_price': row[3],
        'low_price': row[4],
        'close_price': row[5],
        'pre_settlement_price' : row[6],
        'settlement_price' : row[7],
        'rise_offset' : row[8],
        'rise_offset_1' : row[9],
        'trading_vol' : row[10],
        'position_vol' : row[11],
        'position_chg_vol' : row[12],
        'trading_amount': row[13],
        'trading_dt' : '20160308',
        'row_index': row_index,
    }
    print rowdata
    fw.write('''
        self.assertEqual(items[%(row_index)s]['title'], u'%(title)s')
        self.assertEqual(items[%(row_index)s]['trade_name'], u'%(trade_name)s')
        self.assertEqual(items[%(row_index)s]['delivery_mon'], u'%(delivery_mon)s')
        self.assertEqual(items[%(row_index)s]['open_price'], u'%(open_price)s')
        self.assertEqual(items[%(row_index)s]['high_price'], u'%(high_price)s')
        self.assertEqual(items[%(row_index)s]['low_price'], u'%(low_price)s')
        self.assertEqual(items[%(row_index)s]['close_price'], u'%(close_price)s')
        self.assertEqual(items[%(row_index)s]['pre_settlement_price'], u'%(pre_settlement_price)s')
        self.assertEqual(items[%(row_index)s]['settlement_price'], u'%(settlement_price)s')
        self.assertEqual(items[%(row_index)s]['rise_offset'], u'%(rise_offset)s')
        self.assertEqual(items[%(row_index)s]['rise_offset_1'], u'%(rise_offset_1)s')
        self.assertEqual(items[%(row_index)s]['trading_vol'], u'%(trading_vol)s')
        self.assertEqual(items[%(row_index)s]['position_vol'], u'%(position_vol)s')
        self.assertEqual(items[%(row_index)s]['trading_dt'], u'%(trading_dt)s')

        ''' % rowdata)
    
    
    row_index += 1
f.close()
fw.close()