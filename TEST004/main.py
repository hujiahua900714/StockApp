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
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import plotly.graph_objects as go
from tabulate import tabulate

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
        data = cur.execute("select * from AllFinanceState")
        print("[ID, Name, Num(shares), Current Price, Beginning Value, Current Value]")
        print(tabulate(data))
        for data in cur.execute("select * from AllFinanceState"):
            numData+=1
            # print("     ",tabulate(data))
        
        if numData:
            allBeginningValue = cur.execute("select sum(BeginningValue) from AllFinanceState").fetchone()[0]
            allCurrentValue = cur.execute("select sum(CurrentValue) from AllFinanceState").fetchone()[0]
            # print("all current value: ", allCurrentValue, "\nall beginning value: ", allBeginningValue)
            profitLost = (allCurrentValue - allBeginningValue) / allBeginningValue
            percentage = "{:.0%}".format(round(profitLost, 4))
            print(f"     損益率: {percentage}")

            stocks = []
            currentValue = []
            currentProfitLost = []
            valuePercentage = []
            maxHeight = 0
            minHeight = 100
            allValue = cur.execute("select sum(CurrentValue) from AllFinanceState").fetchone()[0]
            for data in cur.execute("select * from AllFinanceState"):
                stocks.append(data[1])
                currentValue.append(data[5])
                currentProfitLost.append(round((data[5] - data[4])/data[4]*100, 2))
                valuePercentage.append(data[5]/allValue)
            # print("        ",stocks)
            # print("        ",currentProfitLost)
            fig, ax1 = plt.subplots(2)
            fig.suptitle('All Finance State')
            ax1[0].pie(valuePercentage, labels=stocks, autopct='%1.1f%%', shadow=True, startangle=90)
            ax1[0].axis('equal')
            ax1[0].set_title('the percentage of all stocks')
            ax1[1].bar(stocks, currentProfitLost, 0.5)
            """
            x = np.arange(len(stocks))
            ax1[1].bar(x, currentProfitLost)
            ax1[1].set_xticks(x)
            ax1[1].set_xticklabels(stocks)
            """
            # add the percentage on the bar chart
            for p in ax1[1].patches:
                width = p.get_width()
                height = p.get_height()
                if height > maxHeight:
                    maxHeight = height
                if height < minHeight:
                    minHeight = height
                x, y = p.get_xy()
                if height >= 15:
                    ax1[1].annotate(f'{height}%', (x + width/2, y + height*0.8), ha='center', color='white')
                elif height <= -15:
                    ax1[1].annotate(f'{height}%', (x + width/2, y + height*0.2), ha='center', color='white')
                elif (height >= 0) and (height < 15):
                    ax1[1].annotate(f'{height}%', (x + width/2, y), ha='center', color='white')
                elif (height <= 0) and (height > -15):
                    ax1[1].annotate(f'{height}%', (x + width/2, y), ha='center', color='white')

            # set the height of bar chart
            # ax1[1].set_ylim(minHeight - 0.3, maxHeight + 0.3)
            ax1[1].set_xlabel('stock name')
            ax1[1].set_ylabel('current growth in percentage')
            ax1[1].set_title('growth of all stocks')

            plt.show()
        else:
            print("     you have no stock to show")

def showStockBuyingRecord():
    stockName=str(input("     input the name of Stock: "))
    updateCurrentPrice()
    print("[ID, Date, Num(shares), Beginning Price, Beginning Value, Current Value]")
    with conn:
        data=cur.execute(f"select * from TW{stockName}")
        print(tabulate(data))

def addStockRecord():
    stockName = str(input("     Please input the name of the stock: "))
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
            print("     this stock does not exist")
            stockList.append(f"{stockName}")
        cur.execute(f"insert or ignore into AllFinanceState (Name, NumberOfShares) values ('{stockName}', 0)")
        stockInfo = cur.execute(f"select * from AllFinanceState where Name = '{stockName}'").fetchone()
        
        # print("info: ",stockInfo)
        stockID = int(stockInfo[0]) # get the stockID, then we can update the stock state in AllFinanceState
        # print("this stock already exists")
        stockNumShares = stockInfo[2]

        print("     shares: ", stockNumShares)

    # add new record into the table of this stock
    with conn:
        numShares = int(input("     Please input the number of shares: "))
        beginningPrice = float(input("     Please input the beginning price: "))
        currentPrice = yf.Ticker(f"{stockName}.TW").history()['Close'][0]
        currentValue = currentPrice * numShares

        beginningValue = beginningPrice * numShares
        cur.execute(f"insert into TW{stockName} "
                    "(Date, NumberOfShares, BeginningPrice, BeginningValue, CurrentValue) "
                    f"values (datetime('now'), {numShares}, round({beginningPrice}, 3), round({beginningValue}, 3), round({currentValue}, 3))")
    # update the stock state in AllFinanceState
    with conn:
        stockNumShares = stockNumShares + numShares
        stockCurrentPrice = yf.Ticker(f"{stockName}.TW").history(period="1d")['Close'][0]
        stockBeginningValue = cur.execute("select sum(BeginningValue)"
                                        f"from TW{stockName}").fetchone()[0]
        stockCurentValue = stockCurrentPrice * stockNumShares
        print("     price: ", stockCurrentPrice, "\n     value: ", stockBeginningValue, "\n")
        cur.execute(f"update AllFinanceState set NumberOfShares = {stockNumShares}, "
                    f"CurrentPrice =  round({stockCurrentPrice}, 3), "
                    f"BeginningValue =  round({stockBeginningValue}, 3), "
                    f"CurrentValue = round({stockCurentValue}, 3) "
                    f"where ID = {stockID}")

def deletStockRecord():
    stockName = str(input("     Please input the name of the stock: "))
    id = int(input("     Please input the id of the record: "))
    with conn:
        cur.execute(f"delete from TW{stockName} where ID = {id}")
        # update the stock state in AllFinanceState
        stockID = cur.execute(f"select ID from AllFinanceState where Name = '{stockName}'").fetchone()[0]
        stockNumShares = cur.execute("select sum(NumberOfShares)"
                                        f"from TW{stockName}").fetchone()[0]
        stockCurrentPrice = yf.Ticker(f"{stockName}.TW").history(period="1d")['Close'][0]
        stockBeginningValue = cur.execute("select sum(BeginningValue)"
                                        f"from TW{stockName}").fetchone()[0]
        stockCurentValue = stockCurrentPrice * stockNumShares
        print("     price: ", stockCurrentPrice, "\n     value: ", stockBeginningValue, "\n")
        cur.execute(f"update AllFinanceState set NumberOfShares = {stockNumShares}, "
                    f"CurrentPrice = round({stockCurrentPrice}, 3), "
                    f"BeginningValue = round({stockBeginningValue}, 3), "
                    f"CurrentValue = round({stockCurentValue}, 3) "
                    f"where ID = {stockID}")
    

def showGrowthOfValueOfSpecificStock():
    #date = yf.Ticker("0050.TW").history(period='1mo')["Date"]
    stockName=str(input("     Please input the number of the stock you want to watch: "))
    print("     Please input the Start Time:")
    year=int(input("     Enter the Year: "))
    month=int(input("     Enter the Month: "))
    date=int(input("     Enter the Date: "))
    priceData = yf.Ticker(f"{stockName}.TW").history(start=datetime.datetime(year, month, date), end=datetime.datetime.now())
    priceData.to_csv(f'{stockName}.csv')
    with open(f'{stockName}.csv', newline='') as csvfile:
        priceData=pd.read_csv(f'{stockName}.csv')
        fig = go.Figure(data=go.Ohlc(x=priceData['Date'],
                    open=priceData['Open'],
                    high=priceData['High'],
                    low=priceData['Low'],
                    close=priceData['Close']))
    fig.show()

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
conn = sqlite3.connect('yourFinance.db')
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
print("options(1, 2, 3, 4, 5, 8, 9)\n",
        "  =(Show all your finance state,\n",
        "  Show a specific stock buying record,\n",
        "  Show the growth of a specific stock,\n",
        "  Add new Stock Buying Record,\n",
        "  Delete specific Stock Buying Record,\n",
        "  Deleting all data,\n",
        "  Leaving this application)\n")
op = int(input("select your option at Mainmenu: "))
while op >= 1:
    
    if op == 1:
        showAllFinanceState()
    elif op == 2:
        showStockBuyingRecord()
    elif op == 3:
        showGrowthOfValueOfSpecificStock()
    elif op == 4:
        addStockRecord()
    elif op == 5:
        deletStockRecord()
    elif op == 8:
        print("     Deleting Data...")
        deleteAllRecord()
    elif op == 9:
        print("     Leaving...")
        break
    print("####################")
    op = int(input("select your option at Mainmenu: "))
###############End of Main Code###############