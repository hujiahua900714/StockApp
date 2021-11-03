"""
<< AllFinanceState >>
1. ID >> increasing primary key
2. Name >> the number of stock in Taiwan
3. NumberOfShares >> the number of shares of a specific stock
    ### we don't need BeginningPrice because every shares of the stock may be different
4. CurrentPrice >> the value of one share now
5. BeginningValue >> the value of all stock when buying in
    BeginningPrice * NumberOfShares
6. CurrentValue >> the value of all stock now
    CurrentPrice * NumberOfShares

<<TW0050>>
1. ID  >> increasing primary key
2. Date >> the date of buying stock
3. NumberOfShares >> the number of shares of a specific stock
4. BeginningPrice >> the value of one share when buying in
5. BeginningValue >> the value of all shares
    BeginningPrice * NumberOfShares
6. CurrentValue >> the current value of all shares
"""

import sqlite3
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

def updateCurrentPrice():
    with conn:
        curs = cur.fetchall()
        for data in curs:
            id = data[0]
            numShares = data[2]
            currentPrice = yf.Ticker(f"{data[1]}.TW").history(period='1d')['Close'][0]
            currentValue = currentPrice * numShares
            cur.execute("update AllFinanceState set "
                        f"CurrentPrice = {currentPrice}, "
                        f"CurrentValue = {currentValue} "
                        f"where ID = {id}")
            

def showAllFinanceState():
    with conn:
        updateCurrentPrice()
        numData = 0
        for data in cur.execute("select * from AllFinanceState"):
            numData+=1
            print(data)
        
        if numData:
            allBeginningValue = cur.execute("select sum(BeginningValue) from AllFinanceState").fetchone()[0]
            allCurrentValue = cur.execute("select sum(CurrentValue) from AllFinanceState").fetchone()[0]
            profitLost = (allBeginningValue - allCurrentValue) / allBeginningValue
            print(f"損益率: {profitLost:.2f}%")

            stocks = []
            for data in cur.execute("select Name from AllFinanceState"):
                stocks.append(str(data[0]))
            allValue = cur.execute("select sum(CurrentValue) from AllFinanceState").fetchone()[0]
            sizes = []
            for data in cur.execute("select CurrentValue from AllFinanceState"):
                sizes.append(data[0]/allValue)
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=stocks, autopct='%1.1f%%', shadow=True, startangle=90)
            ax1.axis('equal')
            plt.show()
        else:
            print("you have no stock to show")


def addStockRecord():
    stockName = str(input("Please input the name of the stock: "))
    cmd = f"""create table if not exists TW{stockName} 
            (ID  integer primary key,
            Date text,
            NumberOfShares integer,
            BeginningPrice float,
            BeginningValue float,
            CurrentValue float,
            unique(ID)
            )"""
    conn.execute(cmd)
    # testing
    with conn:
        if cur.execute(f"select * from AllFinanceState where Name = '{stockName}'") != 1:
            print("this stock does not exist")
            stockList.append(f"{stockName}")
        cur.execute(f"insert or ignore into AllFinanceState (Name, NumberOfShares) values ('{stockName}', 0)")
        stockInfo = cur.execute(f"select * from AllFinanceState where Name = '{stockName}'").fetchone()
        
        # print("info: ",stockInfo)
        stockID = int(stockInfo[0]) # get the stockID, then we can update the stock state in AllFinanceState
        # print("this stock already exists")
        stockNumShares = stockInfo[2]

        print("shares: ", stockNumShares)

    # add new record into the table of this stock
    with conn:
        numShares = int(input("Please input the number of shares: "))
        beginningPrice = float(input("Please input the beginning price: "))
        currentPrice = yf.Ticker(f"{stockName}.TW").history()['Close'][0]
        currentValue = currentPrice * numShares

        beginningValue = beginningPrice * numShares
        cur.execute(f"insert into TW{stockName}"
                    "(Date, NumberOfShares, BeginningPrice, BeginningValue, CurrentValue)"
                    f"values (datetime('now'), {numShares}, round({beginningPrice}, 3), round({beginningValue}, 3), round({currentValue, 3}))")
    # update the stock state in AllFinanceState
    with conn:
        stockNumShares = stockNumShares + numShares
        stockCurrentPrice = yf.Ticker(f"{stockName}.TW").history(period="1d")['Close'][0]
        stockBeginningValue = cur.execute("select sum(BeginningValue)"
                                        f"from TW{stockName}").fetchone()[0]
        stockCurentValue = stockCurrentPrice * stockNumShares
        print("price: ", stockCurrentPrice, "\nvalue: ", stockBeginningValue, "\n")
        cur.execute(f"update AllFinanceState set NumberOfShares = {stockNumShares}, "
                    f"CurrentPrice =  round({stockCurrentPrice}, 3), "
                    f"BeginningValue =  round({stockBeginningValue}, 3), "
                    f"CurrentValue = round({stockCurentValue}, 3) "
                    f"where ID = {stockID}")

def showGrowthOfValueOfSpecificStock():
    #date = yf.Ticker("0050.TW").history(period='1mo')["Date"]
    priceData = yf.Ticker("0050.TW").history(period='1mo')["Close"]
    #sns.lineplot(data=priceData)
    #sns.set_theme()
    plt.plot(priceData)
    plt.xticks(rotation=30)
    plt.show()
    print()

def deleteAllRecord():
    with conn:
        for stock in stockList:
            cur.execute(f"drop table TW{stock}")
        cur.execute("drop table AllFinanceState")
    conn.execute("""create table if not exists AllFinanceState 
                (ID integer primary key,
                Name character(20) unique,
                NumberOfShares integer,
                CurrentPrice float,
                BeginningValue float,
                CurrentValue float,
                unique(ID, Name)
                )""")


############## Main Code ##############
stockList = [] # this list used for delete all records
conn = sqlite3.connect('test002.db')
cur = conn.cursor()
conn.execute("""create table if not exists AllFinanceState 
                (ID integer primary key,
                Name character(20) unique,
                NumberOfShares integer,
                CurrentPrice float,
                BeginningValue float,
                CurrentValue float,
                unique(ID, Name)
                )""")

op = int(input("select your option at Mainmenu: "))
while op >= 1:
    
    if op == 1:
        showAllFinanceState()
    elif op == 2:
        addStockRecord()
    elif op == 3:
        showGrowthOfValueOfSpecificStock()
    elif op == 8:
        deleteAllRecord()
    elif op == 9:
        print("leaving")
        break
    print("####################")
    op = int(input("select your option at Mainmenu: "))
###############End of Main Code###############