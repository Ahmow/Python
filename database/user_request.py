from database.get_yfinance_data import get_yfinance_data
from datetime import datetime as dt
import yfinance as yf
import calendar
import sqlite3
import pytickersymbols as pyt
from database.db import backtest_db, Timeseries
import pandas as pd
from sqlite3 import connect

from datetime import datetime, timedelta

from database.insert_db import ins_data

from database.check_timeframe import check_data
from database.test_imp_yfinance import imp_yfinance

import matplotlib.pyplot as plt

# print('Enter start (yyyy-mm-dd):')
# check_start = input()

# print('Enter end (yyyy-mm-dd):')
# check_end = input()


def get_data_from_sql(start_dt, end_dt):
    format_data = "%Y-%m-%d"
    check_start = start_dt.strftime(format_data)
    check_end = end_dt.strftime(format_data)
    Check_OK = True

    Check_OK = check_data(check_start, check_end)

    sql = (
        "select symbol, tag as date, open, high, low, close, volume from crypto_tseries "
        "where date(tag) <= date('" + check_end + "') "
        "and date(tag) >= date('" + check_start + "') "
        "and symbol = \'MSFT\' "
    )
    conn = connect("backtest.db")

    if Check_OK:
        df = pd.read_sql(sql, conn)
        conn.close()
        return df
    else:
        # If data is not available in the database, fetch from yFinance and insert into the database
        imp_yfinance(check_start, check_end)

        Check_OK = True
        Check_OK = check_data(check_start, check_end)

        df = pd.read_sql(sql, conn)
        conn.close()
        return df
        
    conn.close()

# df.plot(kind = 'scatter', x = 'date', y = 'open')
# plt.show()

# fig, ax = plt.subplots(figsize=(12, 6))
# df['close'].plot(kind='line', ax=ax)
# ax.set_ylabel('Closing Price')
# ax.set_xlabel('Date')
# ax.set_title('MSFT')
# fig.autofmt_xdate()
# plt.show()

# df2 = pd.DataFrame(df, index=df['date'])

# mpf.plot(df2, type='candle', style='yahoo',
#          title='Sample Candlestick Chart',
#          ylabel='Price')


# data = {
#      'Open': df['open'],
#      'High':  df['high'],
#      'Low':  df['low'],
#      'Close':  df['close']
# }

# time_index = pd.DatetimeIndex(df['date'])



# data = {
#      'Open': [10, 15, 14, 12, 13],
#      'High': [15, 16, 15, 14, 14],
#      'Low': [9, 12, 13, 11, 12],
#      'Close': [12, 14, 13, 13, 14]
# }



# time_index = pd.DatetimeIndex([
#       datetime(2021, 1, 1),
#       datetime(2021, 1, 2),
#       datetime(2021, 1, 3),
#       datetime(2021, 1, 4),
#       datetime(2021, 1, 5)
# ])


# # Create a DataFrame with the OHLC data and the time index
# df2 = pd.DataFrame(data, index=time_index)
# print(df2)

# # Configure and plot the candlestick chart
# mpf.plot(df2, type='candle', style='yahoo',
#          title='Sample Candlestick Chart',
#          ylabel='Price')