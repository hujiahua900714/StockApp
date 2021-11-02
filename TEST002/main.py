import sqlite3

def addStockRecord():
    print("test")
    name = str(input("input the name of new stock: "))
    cmd = f"""create table if not exists TW{name} 
            (ID  integer primary key dec,
            Date text,
            Price float,
            NumberOfStock integer,
            TotalValue float,
            )"""
    conn.execute(cmd)

    with conn:
        cur.execute(f"insert into TW{name} (ID, Date, Price, NumberOfStock, TotalValue) values ()")

    

############## Main Code ##############
conn = sqlite3.connect('test003.db')
cur = conn.cursor()
conn.execute("""create table if not exists AllFinanceState 
                (ID integer primary key,
                Name character(20),
                NumberOfStock integer,
                Value float
                )""")
op = int(input("select your option at Mainmenu: "))

while op > 1:
    
    if op == 1:
        addStockRecord()
    if op == 2:
        print()
    else:
        print("none")
    op = int(input("select your option at Mainmenu: "))
