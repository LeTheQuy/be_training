import sqlite3


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {
            "name": self.name,
            "price": self.price
        }

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "Select * from items where  name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.commit()
        connection.close()

        if row:
            return cls(*row)

    def insert_item(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "Insert into items values (?, ?)"
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()

    def delete_item(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "Delete from items where name =?"
        cursor.execute(query, (self.name,))
        connection.commit()
        connection.close()

    def update_item(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "update items set price=? where name =?"
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()
