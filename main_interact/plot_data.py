# data_df hat die ganze Info über Open, Close, High, Low, Volume, Tag
import time
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import mplfinance as mpf


def plot_data(symbol, data_df, **time_points):
    start_point = time_points["start"]
    end_point = time_points["end"]
    
    data = {
     'Open': list(data_df['open']),
     'High': list(data_df['high']),
     'Low':  list(data_df['low']),
     'Close':  list(data_df['close'])
    }

    time_index = pd.DatetimeIndex(data_df['date'])

    df2 = pd.DataFrame(data, index=time_index)

    mpf.plot(df2, type='candle', style='yahoo',
         title='Sample Candlestick Chart',
         ylabel='Price')
