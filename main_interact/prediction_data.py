import pandas as pd
import numpy as np
import os
from subprocess import check_output
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from pandas.plotting import lag_plot
from datetime import datetime
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
#import statsmodels.api as sm


def analyze_data(needed_data, time_points):
    stockname="open"
    date=pd.DataFrame(needed_data,columns=["date"])
    stock=pd.DataFrame()
    stock=pd.DataFrame(needed_data[stockname])
    date=date.reset_index(drop=True)
    stock=stock.reset_index(drop=True)
    aapl=pd.concat([date,stock],axis=1)

    aapl.info()

    aapl.date = pd.to_datetime(aapl.date)
    aapl.set_index('date', inplace=True)

    aapl.plot(figsize=(20,10), linewidth=5, fontsize=20)
    plt.xlabel('hour', fontsize=20)
    plt.show()
