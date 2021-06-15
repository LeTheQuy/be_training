from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource, reqparse

from code.models.item import ItemModel


def get_paginated_list(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        return {"message": "invalid param"}, 400
    res = {}
    res["start"] = start
    res["limit"] = limit
    res["count"] = count
    if start == 1:
        res['previous'] = ""
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        res['previous'] = url + f'?start={start_copy}&limit={limit_copy}'

    if start + limit > count:
        res['next'] = ''
    else:
        start_copy = start + limit
        limit_copy = min(limit, count - start_copy)
        res['next'] = url + f'?start={start_copy}&limit={limit_copy}'
        # finally extract result according to bounds
    res['items'] = results[(start - 1):(start - 1 + limit)]
    return res


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

    @jwt_required(fresh=True)
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

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "Admin role required"}, 401

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
    parse = reqparse.RequestParser()
    parse.add_argument("start", type=int, required=False, default=1)
    parse.add_argument("limit", type=int, required=False, default=20)

    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        data = ItemList.parse.parse_args()

        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            items = [item.json() for item in ItemModel.find_all()]
            return get_paginated_list(items, "/items", **data)
        else:
            return {"items": [item["name"] for item in items],
                    "message": "More data available if you log in."}, 200
