from datetime import datetime as dt
import yfinance as yf
import calendar
import pytickersymbols as pyt
from datetime import datetime, timedelta
import pandas as pd
from peewee import fn
import peewee
from playhouse.sqlite_ext import SqliteExtDatabase

#python -m pwiz -e sqlite backtest.db > models.py
backtest_db = SqliteExtDatabase(
    r"C:\Users\akoca\Desktop\AK\00_Projekte\Python\Einfuerung_Weiterbildung\fork\Python\Ahmet\backtest.db",
    pragmas={
        "journal_mode": "wal",  # WAL-mode.
        "cache_size": -64 * 1000,  # 64MB cache.
        "synchronous": 0,
    },
)  

# url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies' 
# tabelle_url=pd.read_html(url)[0]

ticker_URL= ['MSFT'] #tabelle_url['Symbol'].tolist()

class TestAhmTemp2(peewee.Model):
    adj__close = peewee.FloatField(column_name='Adj Close', null=True)
    close = peewee.FloatField(column_name='Close', null=True)
    date = peewee.DateTimeField(column_name='Date', null=True)  # TIMESTAMP
    high = peewee.FloatField(column_name='High', null=True)
    low = peewee.FloatField(column_name='Low', null=True)
    open = peewee.FloatField(column_name='Open', null=True)
    volume = peewee.FloatField(column_name='Volume', null=True)
    symbol = peewee.TextField(null=True)

    class Meta:
        database = backtest_db
        table_name = 'test_ahm_temp_2'
        primary_key = False# Let the OS manage syncing.


def check_data(check_start, check_end):

    def add_days(n, d = datetime.today()):
        return d + timedelta(n)

    # print('Enter start (yyyy-mm-dd):')
    # start = input()

    # print('Enter end (yyyy-mm-dd):')
    # end = input()


    #check_start = "2024-08-06"
    #check_end =  "2024-08-21"
    format_data = "%Y-%m-%d"
    working_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    holidays_fix = ["01-01", "05-01", "10-03", "12-25", "12-26"]
    holidays_flex = ["2025-04-18", "2025-04-21", "2025-05-29", "2025-06-09",
                    "2024-03-29", "2024-04-01", "2024-05-09", "2024-05-20",
                    "2023-04-07", "2023-04-10", "2023-05-18", "2023-05-29",
                    "2022-04-15", "2022-04-18", "2022-05-26", "2022-06-06",
                    "2021-04-02", "2021-04-05", "2021-05-13", "2021-05-24"
                    ]

    count_working_days = 0
    start_search = 0

    check_data = True

    check_start_day = dt.strptime(check_start, format_data).date()
    check_end_day = dt.strptime(check_end, format_data).date()

    while start_search == 0:
    
        if check_start_day == check_end_day:
                start_search = 1
        
        is_holidays_fix = check_start_day.strftime("%m-%d") in holidays_fix
        is_holidays_flex  = check_start_day.strftime("%Y-%m-%d") in holidays_flex
        is_weekday =calendar.day_name[check_start_day.weekday()] in working_days

        if is_weekday and not is_holidays_fix and not is_holidays_flex:
            count_working_days += 1  

        check_start_day= add_days(1, check_start_day)

    ####### Deutschlandweite
    ####### Neujahr 01.01.
    ####### Karfreitag flexibel
    ####### Ostermontag flexibel
    ####### Christi Himmelfahrt flexibel
    ####### Pfingstmontag flexibel
    ####### 1. Mai
    ####### 03.10.
    ####### 25.12. + 26.12.
    ####### andere Feiertage + was ist mit 24.12. und 31.12.

    #Check 7 Einträge pro Tag
    
    query=(
        TestAhmTemp2
        .select(
            fn.date(TestAhmTemp2.date), 
            TestAhmTemp2.symbol, 
            fn.count(TestAhmTemp2.symbol). alias("Count")
        )
        .where(
            (fn.date(TestAhmTemp2.date) <= check_end) & 
            (fn.date(TestAhmTemp2.date) >=check_start)
        )
        .group_by(TestAhmTemp2.date,TestAhmTemp2.symbol)
        .having(fn.count(TestAhmTemp2.symbol) != 7)
    )
    
    for x in query:
        check_data = False
        return check_data

    # sql = "SELECT date(tag), symbol, count(*) "\
    #     "FROM crypto_tseries t1 "\
    #     "where date(tag) <= date('"+ check_end +"') "\
    #     "and date(tag) >= date('" + check_start +"') "\
    #     "group by date(tag), symbol "\
    #     "having count(*) <> 7 "
    # cursor = backtest_db.cursor()
    # cursor.execute(sql)

    # for x in cursor:
    #     check_data = False
    #     return check_data
    # cursor.close()

    #Check 7 verschiede Einträge pro Tag

    query=(
        TestAhmTemp2
        .select(
            fn.Date(TestAhmTemp2.date),
            TestAhmTemp2.symbol,
            fn.Count(fn.distinct(TestAhmTemp2.date))
        )
        .where(
            (fn.Date(TestAhmTemp2.date) <= check_end) &
            (fn.Date(TestAhmTemp2.date) >= check_start)
        )
        .group_by(TestAhmTemp2.date,TestAhmTemp2.symbol)
        .having(fn.Count(fn.distinct(TestAhmTemp2.date))) != 7  
        )    
    
    for x in query:
        check_data = False
        return check_data

    # sql = "SELECT date(tag), symbol, count(distinct tag) "\
    #     "FROM crypto_tseries t1 "\
    #     "where date(tag) <= date('"+ check_end +"') "\
    #     "and date(tag) >= date('" + check_start +"') "\
    #     "group by date(tag), symbol "\
    #     "having count(distinct tag) <> 7 "
    # cursor = backtest_db.cursor()
    # cursor.execute(sql)

    # for x in cursor:
    #     check_data = False
    #     return check_data
    # cursor.close()

    #Check alle Tage da
    query=(
        TestAhmTemp2.select(
            fn.count(fn.distinct(fn.date(TestAhmTemp2.date))),
            TestAhmTemp2.symbol
        )
        .where(
            (fn.date(TestAhmTemp2.date) <= check_end) &
            (fn.date(TestAhmTemp2.date) >= check_start)
        )
        .group_by(TestAhmTemp2.symbol)
        .having(fn.count(fn.distinct(fn.date(TestAhmTemp2.date))) != count_working_days
        )
    )

    for x in query:
        check_data = False
        return check_data
    # sql = "SELECT  count(distinct(date(tag))), symbol "\
    #     "from crypto_tseries "\
    #     "where date(tag) <= date('"+ check_end +"') "\
    #     "and date(tag) >= date('" + check_start +"') "\
    #     "group by symbol "\
    #     "having count(distinct(date(tag))) <>  " + str(count_working_days)
    # cursor = backtest_db.cursor()
    # cursor.execute(sql)

    # for x in cursor:
    #     check_data = False
    #     return check_data
    # cursor.close()

    #Check mindestens ein Eintrag im Zeitraum da
    # for ticker in ["MSFT", "AAPL", "DDDD"]:
    #     sql1 = "SELECT count(*) "+\
    #       "from crypto_tseries "+\
    #       "where date(tag) <= date('"+ check_end +"') "+\
    #       "and date(tag) >= date('" + check_start +"') "
    #     sql2 = "and symbol = \"" + ticker + "\" "+\
    #       "having count(*) = 0 "
    #     sql = sql1 + sql2
    #     cursor = backtest_db.cursor()
    #     cursor.execute(sql)
    #     cursor.fetchone()

    #     for x in cursor:
    #         print(ticker)
    #     cursor.close()   


    # for ticker in ["MSFT", "AAPL", "DDDD"]:
    #     sql1 = "SELECT count(*) "+\
    #       "from crypto_tseries "+\
    #       "where date(tag) <= date('"+ check_end +"') "+\
    #       "and date(tag) >= date('" + check_start +"') "
    #     sql2 = " and symbol = ':sym'  "+\
    #       "having count(*) = 0 "




    if count_working_days > 0:
        for ticker in ticker_URL:
            count_query=(
                TestAhmTemp2.select(
                    fn.count(TestAhmTemp2.symbol).alias("count")
                )
                .where(
                    (fn.date(TestAhmTemp2.date) <= check_end) &
                    (fn.date(TestAhmTemp2.date) >= check_start)&
                    (TestAhmTemp2.symbol == ticker)
                )
            )

            result= count_query.scalar()
            if result == 0:
                print(f"keine Daten im Zeitaum für: {ticker}" )
                return False
    
    return check_data
    # if count_working_days > 0:
    #     for ticker in ["MSFT", "AAPL"]:

    #         sql1 = (
    #                 "SELECT count(*) as Anz "
    #                 + "from crypto_tseries "
    #                 + "where date(tag) <= date('"
    #                 + check_end
    #                 + "') "
    #                 + "and date(tag) >= date('"
    #                 + check_start
    #                 + "') "
    #                 )
    #         sql2 = " and symbol = '" + ticker + "'  " + "having count(*) = 0 "
    #         sql = sql1 + sql2
        
    #         # param={'sym':ticker}
    #         cursor = backtest_db.cursor()
    #         cursor.execute(sql)

    #         for x in cursor:
    #             #print("Fehler Daten in Zeitraum für Ticker nicht da: " + ticker)
    #             check_data = False
    #             return check_data
    #         cursor.close


    #         temp = cursor.fetchone()

    #         cursor.close

    # return check_data

    # if count_working_days > 0:
    #     for ticker in ["MSFT", "AAPL", "PSTS"]:

    #         start_search = 0
    #         check_start_day = dt.strptime(check_start, format_data).date()
    #         check_end_day = dt.strptime(check_end, format_data).date()

    #         while start_search == 0:
    #             if check_start_day == check_end_day:
    #                     start_search = 1

    #             is_holidays_fix = check_start_day.strftime("%m-%d") in holidays_fix
    #             is_holidays_flex  = check_start_day.strftime("%Y-%m-%d") in holidays_flex
    #             is_weekday =calendar.day_name[check_start_day.weekday()] in working_days

    #             if is_weekday and not is_holidays_fix and not is_holidays_flex:
    #                 akt_tag = check_start_day.strftime("%Y-%m-%d") 

    #                 sql1 = (
    #                     "SELECT count(*) as Anz "
    #                     + "from crypto_tseries "
    #                     + "where date(tag) = date('"
    #                     + akt_tag
    #                     + "') "
    #                     )
    #                 sql2 = " and symbol = '" + ticker + "'  " + "having count(*) = 0 "
    #                 sql = sql1 + sql2
            
    #                 # param={'sym':ticker}
    #                 cursor = backtest_db.cursor()
    #                 cursor.execute(sql)

    #                 for x in cursor:
    #                     missing_day =  check_start_day.strftime("%Y-%m-%d")
    #                     print("Fehler Daten in Zeitraum für Ticker nicht da: " + ticker + ' Tag: ' + missing_day)
    #                 cursor.close


    #                 temp = cursor.fetchone()

    #                 cursor.close
                    
    #             check_start_day= add_days(1, check_start_day)


    # sql = "select * from crypto_tseries"
    # cursor = backtest_db.cursor()
    # df = pd.read_sql()

    # cursor.close


        # if temp is not None and temp[0] == 0:
        #        print("Fehler Daten in Zeitraum für Tock nicht da" + ticker)


    #"and symbol = %s "+\

    # check_day= check_start
    # do_loop = True

    # while do_loop or check_end==check_day:
    #     # Wochenende auschließen
    #     # Was ist mit Feiertagen
    #     print(check_day)

    #     #Daten in Tabelle prüfen 

    #     startdate = dt.strptime(check_day, format_data).date()
    #     startdate= add_days(1, startdate)
    #     check_day = dt.strftime(startdate, format_data)
        
    #     if check_day == check_end:
    #        do_loop = False 