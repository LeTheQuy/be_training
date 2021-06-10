import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_table = "Create table if not Exists users(id integer PRIMARY  key ,username text, password text)"
cursor.execute(create_table)

create_table = "Create table if not Exists items (name text, price real)"
cursor.execute(create_table)

create_table = "insert into items values ( 'item1', 20)"
cursor.execute(create_table)

connection.commit()
connection.close()
