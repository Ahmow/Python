import sqlite3

conn = sqlite3.connect(r"C:\Users\akoca\Desktop\AK\00_Projekte\Python\Einfuerung_Weiterbildung\fork\Python\Ahmet\backtest.db")
cur = conn.cursor()

cur.execute("SELECT Datetime FROM test_ahm_temp_2 LIMIT 5")
rows = cur.fetchall()
for row in rows:
    print(row)

conn.close()