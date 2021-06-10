import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

# create_table = "Create table users(id int,username text, password text)"

# cursor.execute(create_table)

insert_table = "Insert into users values (? ,? , ?,)"
cursor.execute(insert_table, (1, "quydz", "123456"))
cursor.execute(insert_table, (2, "quydz", "123456"))

select_users = "Select * from users"
for row in cursor.execute(select_users):
    print(row)

connection.commit()
connection.close()
