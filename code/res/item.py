import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("price", type=float, required=True, help="This field can not be blank!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {"message": "item not found"}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"messsae": f"An item with name {name} already exits"}, 400

        data = Item.parse.parse_args()

        item = ItemModel(name, data["price"])
        try:
            item.insert_item()
        except:
            return {"message": "An error while inserting item"}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel(name, 0)
        item.delete_item()
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parse.parse_args()
        item = ItemModel.find_by_name(name)

        new_item = ItemModel(name, data["price"])
        if item:
            try:
                new_item.update_item()
            except:
                return {"message": "An error while inserting item"}, 500
        else:
            try:
                new_item.insert_item()
            except:
                return {"message": "An error while update item"}, 500
        return new_item.json()


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
