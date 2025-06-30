from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

backtest_db = SqliteExtDatabase(
    r"C:\Users\akoca\Desktop\AK\00_Projekte\Python\Einfuerung_Weiterbildung\fork\Python\Ahmet\backtest.db",
    pragmas={
        "journal_mode": "wal",  # WAL-mode.
        "cache_size": -64 * 1000,  # 64MB cache.
        "synchronous": 0,
    },
)  

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = backtest_db

class Anzahl(BaseModel):
    adj__close = IntegerField(column_name='Adj Close', null=True)
    close = IntegerField(column_name='Close', null=True)
    date = IntegerField(column_name='Date', null=True)
    high = IntegerField(column_name='High', null=True)
    low = IntegerField(column_name='Low', null=True)
    open = IntegerField(column_name='Open', null=True)
    volume = IntegerField(column_name='Volume', null=True)

    class Meta:
        table_name = 'Anzahl'
        primary_key = False

class CryptoTseries(BaseModel):
    close = FloatField()
    date = DateTimeField()
    high = FloatField()
    low = FloatField()
    open = FloatField()
    symbol = CharField()
    volume = FloatField()

    class Meta:
        table_name = 'crypto_tseries'
        indexes = (
            (('symbol', 'date'), True),
        )
        primary_key = CompositeKey('date', 'symbol')

class TestAhm(BaseModel):
    __close_msft_ = FloatField(column_name=('Close', 'MSFT'), null=True)
    _symbol_ = TextField(column_name=('SYMBOL', ''), null=True)
    __volume_msft_ = IntegerField(column_name=('Volume', 'MSFT'), null=True)
    high = FloatField(column_name='High', null=True)
    low = FloatField(column_name='Low', null=True)
    open = FloatField(column_name='Open', null=True)
    date = UnknownField(index=True, null=True)  # TIMESTAMP

    class Meta:
        table_name = 'test_ahm'
        primary_key = False

class TestAhmTemp2(BaseModel):
    adj__close = FloatField(column_name='Adj Close', null=True)
    close = FloatField(column_name='Close', null=True)
    datetime = DateTimeField(column_name='Datetime', null=True)  # TIMESTAMP
    high = FloatField(column_name='High', null=True)
    low = FloatField(column_name='Low', null=True)
    open = FloatField(column_name='Open', null=True)
    volume = FloatField(column_name='Volume', null=True)
    symbol = TextField(null=True)

    class Meta:
        table_name = 'test_ahm_temp_2'
        primary_key = False

class YfinanceAny3(BaseModel):
    close = FloatField(column_name='Close', null=True)
    datetime = UnknownField(column_name='Datetime', index=True, null=True)  # TIMESTAMP
    high = FloatField(column_name='High', null=True)
    low = FloatField(column_name='Low', null=True)
    open = FloatField(column_name='Open', null=True)
    symbol = TextField(column_name='SYMBOL', null=True)
    volume = IntegerField(column_name='Volume', null=True)

    class Meta:
        table_name = 'yfinance_any3'
        primary_key = False

