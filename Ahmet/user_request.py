
import pandas as pd
from models import TestAhmTemp2
from datetime import datetime, timedelta

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Ahmet.checktime_ah import check_data
from Ahmet.yfinance_ahmet import imp_yfinance
from peewee import fn
import peewee
from playhouse.sqlite_ext import SqliteExtDatabase

backtest_db = SqliteExtDatabase(
    "backtest.db",
    pragmas={
        "journal_mode": "wal",  # WAL-mode.
        "cache_size": -64 * 1000,  # 64MB cache.
        "synchronous": 0,
    },
)  

# class TestAhmTemp2(peewee.Model):
#     adj__close = peewee.FloatField(column_name='Adj Close', null=True)
#     close = peewee.FloatField(column_name='Close', null=True)
#     date = peewee.DateTimeField(column_name='Date', null=True)  # TIMESTAMP
#     high = peewee.FloatField(column_name='High', null=True)
#     low = peewee.FloatField(column_name='Low', null=True)
#     open = peewee.FloatField(column_name='Open', null=True)
#     volume = peewee.FloatField(column_name='Volume', null=True)
#     symbol = peewee.TextField(null=True)

#     class Meta:
#         database = backtest_db
#         table_name = 'test_ahm_temp_2'
#         primary_key = False# Let the OS manage syncing.

# print('Enter start (yyyy-mm-dd):')
# check_start = input()

# print('Enter end (yyyy-mm-dd):')
# check_end = input()


def get_data_from_sql(start_dt, end_dt, symbol='MSFT'):
    format_data = "%Y-%m-%d"
    check_start = start_dt.strftime(format_data)
    check_end = end_dt.strftime(format_data)
    

    if not check_data(check_start, check_end):
        print("Daten unvollständig, versuche Download über yFinance")
        imp_yfinance(check_start, check_end, symbol)

    if not check_data(check_start, check_end, symbol):
            print("Daten konnten nicht vollständig geladen werden.")
            return None

    query = (
        TestAhmTemp2.select(
            TestAhmTemp2.symbol,
            f.date(TestAhmTemp2.date),
            TestAhmTemp2.open,
            TestAhmTemp2.high,
            TestAhmTemp2.low,
            TestAhmTemp2.close,
            TestAhmTemp2.volume
        )
        .where(
            (fn.date(TestAhmTemp2.date) <= check_end) &
            (fn.date(TestAhmTemp2.date) >= check_start)&
            (TestAhmTemp2.symbol == symbol) 
        )
    )

    # "select symbol, tag as date, open, high, low, close, volume from crypto_tseries "
    #     "where date(tag) <= date('" + check_end + "') "
    #     "and date(tag) >= date('" + check_start + "') "
    #     "and symbol = \'MSFT\' "
    # conn = connect("backtest.db")

    df = pd.DataFrame(list(query.dicts()))
    return df
#     else:
#         # If data is not available in the database, fetch from yFinance and insert into the database
        

#         Check_OK = True
#         Check_OK = check_data(check_start, check_end)

#         if Check_OK:
#             df = pd.DataFrame(list(query.dicts()))
#             return df
#         else:
#             print("Daten in yFinance unvollständig")



# # df.plot(kind = 'scatter', x = 'date', y = 'open')
# # plt.show()

# # fig, ax = plt.subplots(figsize=(12, 6))
# # df['close'].plot(kind='line', ax=ax)
# # ax.set_ylabel('Closing Price')
# # ax.set_xlabel('Date')
# # ax.set_title('MSFT')
# # fig.autofmt_xdate()
# # plt.show()

# # df2 = pd.DataFrame(df, index=df['date'])

# # mpf.plot(df2, type='candle', style='yahoo',
# #          title='Sample Candlestick Chart',
# #          ylabel='Price')


# # data = {
# #      'Open': df['open'],
# #      'High':  df['high'],
# #      'Low':  df['low'],
# #      'Close':  df['close']
# # }

# # time_index = pd.DatetimeIndex(df['date'])



# # data = {
# #      'Open': [10, 15, 14, 12, 13],
# #      'High': [15, 16, 15, 14, 14],
# #      'Low': [9, 12, 13, 11, 12],
# #      'Close': [12, 14, 13, 13, 14]
# # }



# # time_index = pd.DatetimeIndex([
# #       datetime(2021, 1, 1),
# #       datetime(2021, 1, 2),
# #       datetime(2021, 1, 3),
# #       datetime(2021, 1, 4),
# #       datetime(2021, 1, 5)
# # ])


# # # Create a DataFrame with the OHLC data and the time index
# # df2 = pd.DataFrame(data, index=time_index)
# # print(df2)

# # # Configure and plot the candlestick chart
# # mpf.plot(df2, type='candle', style='yahoo',
# #          title='Sample Candlestick Chart',
# #          ylabel='Price')