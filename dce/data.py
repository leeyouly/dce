import PyDB
from spiderlib.data import DataStorage


class DceDailyStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_MARKET_DCE_DAY'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField('title', is_key=True),
            PyDB.StringField('trade_name', is_key=True),
            PyDB.StringField('delivery_mon', is_key=True),
            PyDB.StringField('open_price'),
            PyDB.StringField('high_price'),
            PyDB.StringField('low_price'),
            PyDB.StringField('close_price'),
            PyDB.StringField('pre_settlement_price'),
            PyDB.StringField('settlement_price'),
            PyDB.StringField('rise_offset'),
            PyDB.StringField('rise_offset_1'),
            PyDB.StringField('trading_vol'),
            PyDB.StringField('position_vol'),
            PyDB.StringField('position_chg_vol'),
            PyDB.StringField('trading_amount'),
            PyDB.StringField('trading_dt', is_key=True),
            PyDB.StringField('datetime_stamp'),
        ])


class TradingCalendarStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_TRADE_CALENDAR'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField('tradingcalendar', is_key=True),
            PyDB.DateField('tradingday', is_key=True),
            PyDB.IntField('flag'),
        ])


class DceCangdanStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_DCE_BILL_INPUT'
        self.db.set_metadata(self.table_name, [
            PyDB.StringField('product_name', is_key=True),
            PyDB.StringField('release_date'),
            PyDB.StringField('warehouse', is_key=True),
            PyDB.StringField('last_bill'),
            PyDB.StringField('today_open_bill'),
            PyDB.StringField('today_close_bill'),
            PyDB.StringField('today_total_bill'),
            PyDB.StringField('bill_change'),
            PyDB.StringField('data_date', is_key=True),
            PyDB.StringField('datetime_stamp'),
            PyDB.StringField('title'),
        ])

    def save_or_update(self, item):
        self.db.save_or_update(self.table_name, item)
        self.db.commit()


class DceChicangStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_MT_DCE_POSITION'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField('datadate', is_key=True),
            PyDB.StringField('instrumentid', is_key=True),
            PyDB.StringField('datatype', is_key=True),
            PyDB.IntField('rank', is_key=True),
            PyDB.StringField('account'),
            PyDB.IntField('vol'),
            PyDB.IntField('chg'),
        ])


class DcePinzhongChicangStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_MT_DCE_POSITION_PZ'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField('datadate', is_key=True),
            PyDB.StringField('pinzhongid', is_key=True),
            PyDB.StringField('datatype', is_key=True),
            PyDB.IntField('rank', is_key=True),
            PyDB.StringField('account'),
            PyDB.IntField('vol'),
            PyDB.IntField('chg'),
        ])


class DceMemberStorage(DataStorage):
    def __init__(self, db_url):
        self.db = self.build_connection(db_url)
        self.table_name = 'T_MT_DCE_MEMBERS'
        self.db.set_metadata(self.table_name, [
            PyDB.DateField('datadate', is_key=True),
            PyDB.StringField('id', is_key=True),
            PyDB.StringField('name'),
            PyDB.StringField('short_name'),
            PyDB.StringField('address'),
            PyDB.StringField('website'),
            PyDB.StringField('phone'),
        ])
