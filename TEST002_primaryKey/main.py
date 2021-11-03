import sqlite3

conn = sqlite3.connect('test002.db')
cur = conn.cursor()
name1 = str(input())
conn.execute(f"""create table if not exists {name1}
         (ID integer primary key,
         name character(20) unique,
         age integer
         )""")

with conn:
    name = input()
    age = int(input())
    age2 = cur.execute(f"select age from {name1} where name = '{name}'")
    if age2[0] == None:
        print(age2[0])
        age = age + age2[0]
    else:
        print("none")
    
    cur.execute(f"insert or replace into {name1} (name, age) values ('{name}', {age}))")

    name = input()
    age = int(input())
    age2 = cur.execute(f"select age from {name1} where name = '{name}'")
    age = age + age2
    cur.execute(f"insert or replace into {name1} (name, age) values ('{name}', {age}))")

    age = int(input())
    age2 = cur.execute(f"select age from {name1} where name = '{name}'")
    age = age + age2
    cur.execute(f"insert or replace into {name1} (name, age) values ('{name}', {age}))")

conn.commit()