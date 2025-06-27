import yfinance as yf
import sqlite3 
import pandas as pd
from datetime import datetime, timedelta
from pytickersymbols import PyTickerSymbols



# print(list(nasdaq_tickers))
# ticker= "MSFT"
# interval= "1m"
# period= "5d"

# data = yf.download(ticker, interval=interval, period=period)

# conn=sqlite3.connect('backtest.db')
# data.to_sql('test_ahm', conn, if_exists='replace')

#schleife erstellen jeweils 7 Tage bis ende des Jahres. Eine Tabelle komplette Tabelle erstellen( concat oder extend). Überprüfen, ob SQL light fähig ist eine immense Zahl an Daten aufzunehmen. 

# stock_data = PyTickerSymbols()
# DAX_tickers = stock_data.get_stocks_by_index('DAX')

# for stock in DAX_tickers:
#     ticker =stock["symbol"]
# url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies' 
# tabelle_url=pd.read_html(url)[0]

def imp_yfinance():


    ticker= ['MSFT']     #tabelle_url['Symbol'].tolist()
    interval= "1h"
    days_periode= 7
    total_days= 30
    enddate= datetime.today()
    startdate= enddate - timedelta(days = total_days)  #datetime - ein genauer Zeitstempel (Datum), timedelta – eine Zeitspanne, z. B. "7 Tage" oder "3 Stunden"




# startdate_temp= datetime.strptime(startdatestr,"%Y-%m-%d").date()
# enddate_temp= datetime.strptime(enddatestr,"%Y-%m-%d").date()

    tabstart= [startdate + timedelta(days=days_interval)
                for days_interval in range(0,(enddate - startdate).days,days_periode)] 


    tabrahmen=[]
    for symbol in ticker:
        for tabstartzeit in tabstart:
            tabendzeit= min(tabstartzeit + timedelta(days=days_periode),enddate)
    
            # startdatestr= tabstartzeit.strftime("%Y-%m-%d")
            # enddatestr= tabendzeit.strftime("%Y-%m-%d")


            data = yf.download(symbol, interval=interval, start=tabstartzeit, end=tabendzeit)
        # if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0) #MultiIndex flatten

            data=data.reset_index() #Hier wird der Index (Datetime) zu einer normalen Spalte 'Datetime'
    
            data['symbol'] = symbol
    # data_temp= data.index
    # date_temo_0= data.index[0] #.strptime("%Y-%m-&d")'
    # data["Datum"] = data.index
            tabrahmen.append(data)
    

# print(data.head())
# print(data.columns)
# print(type(data))

    volletab=pd.concat(tabrahmen, ignore_index=True) #index datetimeindex wird von pandas nicht als normale Spalte mitgenommen.
#volletab.columns = volletab.columns.get_level_values(0) #MultiIndex flatten

# print(volletab.head())
# print(volletab.columns)
# print(type(volletab))
    db_path=r"C:\Users\akoca\Desktop\AK\00_Projekte\Python\Einfuerung_Weiterbildung\fork\Python\Ahmet\backtest.db"
    conn=sqlite3.connect(db_path)
    volletab.to_sql('test_ahm_temp_2', conn, if_exists='replace', index=False)

if __name__ == "__main__":
    imp_yfinance()

#qualität der daten prüfen.



# range(start, stop, step)

# stock_data = PyTickerSymbols()
# countries = stock_data.get_all_countries()
# indices = stock_data.get_all_indices()
# industries = stock_data.get_all_industries()


# datetime.today()	Jetzt (lokal)
# datetime.now()	Wie today() (auch mit Zeitzone)
# datetime(2024, 1, 1)	Manuell erstelltes Datum
# datetime.strptime(...)	String → Datum umwandeln
# datetime.strftime(...)	Datum → String formatieren

# min() function returns the item with the lowest value


# concat (https://www.geeksforgeeks.org/python/pandas-concat-function-in-python/)
# Syntax: concat(objs, axis, join, ignore_index, keys, levels, names, verify_integrity, sort, copy)


# Parameters:


# objs: Series or DataFrame objects
# axis: axis to concatenate along; default = 0
# join: way to handle indexes on other axis; default = ‘outer’
# ignore_index: if True, do not use the index values along the concatenation axis; default = False
# keys: sequence to add an identifier to the result indexes; default = None
# levels: specific levels (unique values) to use for constructing a MultiIndex; default = None
# names: names for the levels in the resulting hierarchical index; default = None
# verify_integrity: check whether the new concatenated axis contains duplicates; default = False
# sort: sort non-concatenation axis if it is not already aligned when join is ‘outer’; default = False
# copy: if False, do not copy data unnecessarily; default = True
# Returns: type of objs (Series of DataFrame)