import yfinance as yf
import sqlite3

def MainMenu():
    #1: add new stock
    print("select your option(1,2,3)")



MainMenu()
print("123")
conn = sqlite3.connect('test001.db')
cur = conn.cursor()
conn.execute('''create table Stock001 (SID INT PRIMARY KEY     NOT NULL,
                                    Price integer)''')
with conn:
    cur.execute('insert into Stock001 values (0050, 10)')

conn.commit()