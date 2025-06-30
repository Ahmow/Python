import pandas as pd
from peewee import fn
import peewee
from playhouse.sqlite_ext import SqliteExtDatabase

#python -m pwiz -e sqlite backtest.db > models.py
backtest_db = SqliteExtDatabase(
    "backtest.db",
    pragmas={
        "journal_mode": "wal",  # WAL-mode.
        "cache_size": -64 * 1000,  # 64MB cache.
        "synchronous": 0,
    },
)  

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

#database.create_tables([test_ahm_temp_2])
cn= TestAhmTemp2.select(TestAhmTemp2.symbol, fn.count(TestAhmTemp2.symbol).alias('count')).group_by(TestAhmTemp2.symbol)

print (cn.sql())

for c in cn:
    print(c.symbol,getattr(c, 'count'))


class Symbolcount(peewee.Model):
    symbol=peewee.TextField(null=True)
    count= peewee.IntegerField(null=True)
    
    class Meta:
        database = backtest_db
        table_name= 'Symbolcount'
        primary_key = False


backtest_db.create_tables([Symbolcount])


data_to_insert=[{'symbol' : c.symbol, 
                 'count' : getattr(c, 'count')} 
                 for c in cn]

with backtest_db.atomic():
    Symbolcount.insert_many(data_to_insert).execute()


# conn = sqlite3.connect('backtest.db')
# volletab= pd.read_sql_query("Select * from test_ahm_temp_2", conn)

# print(volletab.columns)

# volletab['Date'] = pd.to_datetime(volletab['Date'])
# volletab['Woche']= volletab['Date'].dt.to_period('W')
# anzahl= volletab.groupby(['symbol','Woche']).count()
# print(anzahl)

# conn=sqlite3.connect('backtest.db')
# anzahl.to_sql('Anzahl', conn, if_exists='replace', index=False)
