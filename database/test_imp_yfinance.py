from database.get_yfinance_data import get_yfinance_data
from datetime import datetime as dt
import yfinance as yf
import sqlite3
import pytickersymbols as pyt
from database.db import backtest_db, Timeseries

from datetime import datetime, timedelta

from database.insert_db import ins_data

def  imp_yfinance(start_d, end_d):
  def add_days(n, d = datetime.today()):
    return d + timedelta(n)

  #start = "2024-08-01"
  #end = "2024-08-02"
  #format_data = "%d.%m.%Y"
  #startdate = dt.strptime(startPoint, format_data)
  #enddate = dt.strptime(endPoint, format_data)
  #get_yfinance_data(symbol, interval= interval, period= period)
  #start = dt.strptime(f"{startPoint}";, "%Y-%m-%d")  # Avoids leap year bug.
  #end  = dt.strptime(f"{endPoint}";, "%Y-%m-%d")  # Avoids leap year bug.

  format_data = "%Y-%m-%d"

  interval= "60m"
  period= "1d"
  tabellen_name = 'yfinance_any3'
  #db_aktion = 'append'
  db_aktion = 'replace'

  stock_data = pyt.PyTickerSymbols()
  german_stocks = stock_data.get_stocks_by_index('DAX')

  transfer_start = start_d

  conn=sqlite3.connect('backtest.db')

  check_start_t =  dt.strptime(start_d, format_data).date()
  check_end_t =  dt.strptime(end_d, format_data).date()

  diff =  (check_end_t - check_start_t).days

  # for stock in german_stocks: #BNR und DTG ausschließen
  #   ticker = stock['symbol']
  for ticker in ["MSFT", "AAPL"]:
    start = transfer_start
    end = end_d
  
    data = yf.download(ticker, interval=interval, period=period, start=start, end=end)
    data['SYMBOL'] = ticker
    
    #ins_data(data, ticker)

    #data = data.transpose().reset_index(drop=True).transpose()

    # columns = ['Close', 'Open']
    # new_df = DataFrame()

    data.columns=data.columns.get_level_values(0)

    if data.empty is False:
      data.to_sql(tabellen_name, conn, if_exists=db_aktion)
      db_aktion = 'append'

    for i  in range(diff):
          start = end
          startdate = dt.strptime(end, format_data).date()
          startdate= add_days(1, startdate)
          end= dt.strftime(startdate, format_data)
          data = yf.download(ticker, interval=interval, period=period, start=start, end=end)
          data['SYMBOL'] = ticker

          #data = data.transpose().reset_index(drop=True).transpose()
          
          data.columns=data.columns.get_level_values(0)

          if data.empty is False:    
            data.to_sql(tabellen_name, conn, if_exists=db_aktion)
            db_aktion = 'append'

  conn.close

  transfer_end = end

  sql="Insert into crypto_tseries (symbol, tag,  close, high, low, open, volume) "\
      "select t1.\"SYMBOL\", t1.\"Datetime\", t1.\"Close\", t1.\"High\", t1.\"Low\", t1.\"Open\", t1.\"Volume\" "\
      "FROM yfinance_any3 t1 "\
      "where not exists (select t2.symbol "\
                        "from crypto_tseries t2 "\
                        "where t1.\"SYMBOL\" = t2.symbol "\
                        "and t1.\"Datetime\" = t2.tag)"
  cursor = backtest_db.cursor()
  cursor.execute(sql)
  cursor.close()


  # cursor = backtest_db.cursor()
  # sql="delete from test_ahm where symbol in (""MSFT"", ""AAPL"")"
  # cursor.execute(sql)
  # sql="insert into test_ahm select * from yfinance_any3"
  # cursor.execute(sql)
  # cursor.close()