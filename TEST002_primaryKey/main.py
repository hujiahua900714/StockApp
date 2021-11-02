import sqlite3

conn = sqlite3.connect('test002.db')
cur = conn.cursor()
name1 = str(input())
conn.execute(f"""create table if not exists {name1}
         (ID integer primary key,
         name character(20))""")

with conn:
    name = input()
    cur.execute(f"insert into {name1} (name) values ('{name}')")
    name = input()
    cur.execute(f"insert into {name1} (name) values ('{name}')")
    name = input()
    cur.execute(f"insert into {name1} (name) values ('{name}')")

conn.commit()