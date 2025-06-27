import pandas as pd
import numpy as np
import os
from subprocess import check_output
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from pandas.plotting import lag_plot
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm
from advanced_ta import LorentzianClassification
from ta.volume import money_flow_index as MFI

def analyze_data_Lorentzian(df2, time_points):
    # openname="open"
    # date=pd.DataFrame(needed_data,columns=["date"])
    # open=pd.DataFrame()
    # open=pd.DataFrame(needed_data[openname])
    # date=date.reset_index(drop=True)
    # open=open.reset_index(drop=True)
    # df=pd.concat([date,open],axis=1)

    df = df2.drop('symbol', axis=1)


    lc = LorentzianClassification(
        df,
        features=[
            LorentzianClassification.Feature("RSI", 14, 2),  # f1
            LorentzianClassification.Feature("WT", 10, 11),  # f2
            LorentzianClassification.Feature("CCI", 20, 2),  # f3
            LorentzianClassification.Feature("ADX", 20, 2),  # f4
            LorentzianClassification.Feature("RSI", 9, 2),   # f5
            MFI(df['high'], df['low'], df['close'], df['volume'], 14) #f6
        ],
        settings=LorentzianClassification.Settings(
            source='close',
            neighborsCount=8,
            maxBarsBack=2000,
            useDynamicExits=False
        ),
        filterSettings=LorentzianClassification.FilterSettings(
            useVolatilityFilter=True,
            useRegimeFilter=True,
            useAdxFilter=False,
            regimeThreshold=-0.1,
            adxThreshold=20,
            kernelFilter = LorentzianClassification.KernelFilter(
                useKernelSmoothing = False,
                lookbackWindow = 8,
                relativeWeight = 8.0,
                regressionLevel = 25,
                crossoverLag = 2)
        )
    )
    #lc.dump('output/result.csv')
    lc.plot('output/result.jpg')