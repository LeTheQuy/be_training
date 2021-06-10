import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("price", type=float, required=True, help="This field can not be blank!")

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
            return {"item": {"name": row[0], "price": row[1]}}

    @classmethod
    def insert_item(cls, name, price):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "Insert into items values (?, ?)"
        cursor.execute(query, (name, price))
        connection.commit()
        connection.close()

    @classmethod
    def delete_item(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "Delete from items where name =?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls, name, price):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "update items set price=? where name =?"
        cursor.execute(query, (price, name))
        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        else:
            return {"message": "item not found"}, 404

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"messsae": f"An item with name {name} already exits"}, 400

        data = Item.parse.parse_args()

        item = {
            "name": name,
            "price": data["price"]
        }
        try:
            self.insert_item(name, data["price"])
        except:
            return {"message": "An error while inserting item"}, 500
        return item, 201

    def delete(self, name):
        self.delete_item(name)
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parse.parse_args()
        item = self.find_by_name(name)

        new_item = {
            "name": name,
            "price": data["price"]
        }

        if item:
            try:
                self.update_item(name, data["price"])
            except:
                return {"message": "An error while inserting item"}, 500
        else:
            try:
                self.insert_item(name, data["price"])
            except:
                return {"message": "An error while update item"}, 500
        return new_item


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "Select * from items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({
                "name": row[0],
                "price": row[1],
            })
        connection.commit()
        connection.close()
        return {"items": items}
