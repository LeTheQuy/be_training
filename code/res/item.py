from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from code.models.item import ItemModel


class Item(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("price", type=float, required=True, help="This field can not be blank!")
    parse.add_argument("store_id", type=int, required=True, help="Every Item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name=name)
        if item:
            return item.json()
        else:
            return {"message": "item not found"}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exits"}, 400

        data = Item.parse.parse_args()

        item = ItemModel(name, **data)
        try:
            item.insert_item()
        except:
            return {"message": "An error while inserting item"}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_on_db()
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parse.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]

        item.insert_item()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.find_all()]}
