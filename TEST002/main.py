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
5. BeginningValue >> the value of all stock
    BeginningPrice * NumberOfShares
"""

import sqlite3
import yfinance as yf



def addStockRecord():
    print("test")
    stockName = str(input("Please input the name of the stock: "))
    cmd = f"""create table if not exists TW{stockName} 
            (ID  integer primary key,
            Date text,
            NumberOfShares integer,
            BeginningPrice float,
            BeginningValue float,
            unique(ID)
            )"""
    conn.execute(cmd)
    # testing
    with conn:
        stockInfo = cur.execute(f"select * from AllFinanceState where Name = '{stockName}'").fetchone()
        
        print("info: ",stockInfo)
        stockID = stockInfo[0] # get the stockID, then we can update the stock state in AllFinanceState
        print("id: ", stockID)
        if stockID == None:
            print("this is a new stock")
            cur.execute(f"insert into AllFinanceState (Name, NumberOfShares) values ('{stockName}', 0)")
            # update the info. of stock
            stockInfo = cur.execute(f"select * from AllFinanceState where Name = '{stockName}'") 
            stockID = stockInfo[0]
            stockNumShares = 0
            print(f"the ID of TW{stockName} is {stockID}")
        else:
            print("this stock already exists")
            stockNumShares = stockInfo[2]

        print("shares: ", stockNumShares)

    # add new record into the table of this stock
    with conn:
        numShares = int(input("Please input the number of shares: "))
        beginningPrice = float(input("Please input the beginning price: "))
        
        beginningValue = beginningPrice * numShares
        cur.execute(f"insert into TW{stockName}"
                    "(Date, NumberOfShares, BeginningPrice, BeginningValue)"
                    f"values (datetime('now'), {numShares}, {beginningPrice}, {beginningValue})")
    # update the stock state in AllFinanceState
    with conn:
        stockNumShares = stockNumShares + numShares
        stockCurrentPrice = yf.Ticker(f"{stockName}.TW").history(period="1d")['Close'][0]
        stockBeginningValue = cur.execute("select sum(BeginningValue)"
                                        f"from TW{stockName}").fetchone()[0]
        print("price: ", stockCurrentPrice, "\nvalue: ", stockBeginningValue, "\n")
        # cur.execute("update AllFinanceState set ")


def updateCurrentPrice():
    print()

############## Main Code ##############
stocks = ["none"]
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

with conn:
    print("test")
    cur.execute("insert or ignore into AllFinanceState (Name, NumberOfShares) values ('0050', 0)")
    cur.execute("insert or ignore into AllFinanceState (Name, NumberOfShares) values ('2330', 0)")

for row in cur.execute("select Name from AllFinanceState where Name = '0050'"):
    print(row)
    print(row[0])
    # stocks.append(row[0])
"""
for list in stocks:
    print(list)
"""
op = int(input("select your option at Mainmenu: "))
while op >= 1:
    
    if op == 1:
        addStockRecord()
    elif op == 2:
        addStockRecord()
    elif op == 9:
        print("none")
        break
    op = int(input("select your option at Mainmenu: "))
