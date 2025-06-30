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
    openname="open"
    highname="high"
    lowname="low"
    closename="close"
    volumename="volume"
    date=pd.DataFrame(df2,columns=["date"])
    close=pd.DataFrame()
    close=pd.DataFrame(df2[closename])
    open=pd.DataFrame()
    open=pd.DataFrame(df2[openname])
    volume=pd.DataFrame()
    volume=pd.DataFrame(df2[volumename])
    high=pd.DataFrame()
    high=pd.DataFrame(df2[highname])
    low=pd.DataFrame()
    low=pd.DataFrame(df2[lowname])
    date=date.reset_index(drop=True)
    open=open.reset_index(drop=True)
    high=high.reset_index(drop=True)
    low=low.reset_index(drop=True)
    close=close.reset_index(drop=True)
    volume=volume.reset_index(drop=True)
    df=pd.concat([date,open,high,low,close, volume],axis=1)
    print(df)
    #df = df2.drop('symbol', axis=1)

    df.index = pd.DatetimeIndex(df["date"])
    

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
            source= df['close'],
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

    
    

    # lc.data.head()

    # from sklearn.preprocessing import StandardScaler
    # scaler = StandardScaler()
    # scaler.fit(lc.data)
    # scaled_data = scaler.transform(lc.data)

    # scaled_data_df = pd.DataFrame(scaled_data, columns=lc.data.columns)

    # scaled_data_df.head()

    # lc.dump('C:\BckUp\Python/result.csv')
    lc.plot('C:\BckUp\Python/result.jpg')
    