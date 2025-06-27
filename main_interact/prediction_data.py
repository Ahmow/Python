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

def smape_kun(y_true, y_pred):
    return np.mean((np.abs(y_pred - y_true) * 200/ (np.abs(y_pred) + np.abs(y_true))))


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

    aapl.diff().plot(figsize=(20,10), linewidth=5, fontsize=20)
    plt.xlabel('Year', fontsize=20)

    dr = aapl.cumsum()
    dr.plot()
    plt.title('Cumulative Returns')

    plt.figure(figsize=(10,10))
    lag_plot(aapl[stockname], lag=5)
    plt.title('Autocorrelation plot')

    plot_acf(aapl[stockname], lags=5)
    plot_pacf(aapl[stockname], lags=5)

    train_data, test_data = aapl[0:int(len(aapl)*0.8)], aapl[int(len(aapl)*0.8):]
    plt.figure(figsize=(12,7))
    plt.title('AAPL Prices')
    plt.xlabel('Dates')
    plt.ylabel('Prices')
    plt.plot(aapl[stockname], 'blue', label='Training Data')
    plt.plot(test_data[stockname], 'green', label='Testing Data')
    plt.legend()

    train_ar = train_data[stockname].values
    test_ar = test_data[stockname].values

    history = [x for x in train_ar]
    print(type(history))
    predictions = list()
    for t in range(len(test_ar)):
        model = ARIMA(history, order=(5,1,2))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test_ar[t]
        history.append(obs)
        #print('predicted=%f, expected=%f' % (yhat, obs))
    error = mean_squared_error(test_ar, predictions)
    print('Testing Mean Squared Error: %.3f' % error)
    error2 = smape_kun(test_ar, predictions)
    print('Symmetric mean absolute percentage error: %.3f' % error2)

    plt.figure(figsize=(12,7))
    plt.plot(aapl[stockname],'green', color='blue', label='Training Data')
    plt.plot(test_data.index, predictions, color='green', marker='o', linestyle='dashed', 
            label='Predicted Price')
    plt.plot(test_data.index, test_data[stockname], color='red', label='Actual Price')
    plt.title('AAPL Prices Prediction')
    plt.xlabel('Dates')
    plt.ylabel('Prices')
    plt.legend()
    plt.show()

    plt.figure(figsize=(12,7))
    plt.plot(test_data.index, predictions, color='green', marker='o', linestyle='dashed', 
            label='Predicted Price')
    plt.plot(test_data.index, test_data[stockname], color='red', label='Actual Price')
    plt.title('AAPL Prices Prediction')
    plt.xlabel('Dates')
    plt.ylabel('Prices')
    plt.legend()

    actual=pd.DataFrame()
    actual=pd.DataFrame(test_ar,columns=["Actual"])
    predicted=pd.DataFrame(list(predictions),columns=["Predicted"])
    actual=actual.reset_index(drop=True)
    predicted=predicted.reset_index(drop=True)
    output=pd.concat([actual,predicted],axis=1)
    print(output.head(10))
