from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from code.models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "store not found"}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name) is not None:
            return {"message": f"A Store with name {name} already exits"}, 400
        store = StoreModel(name)
        try:
            store.add_to_db()
        except:
            return {"message": "An error while inserting store"}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_on_db()
        return {"message": "Store deleted"}


class StoreList(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("page", type=int, required=False, default=1)
    parse.add_argument("per_page", type=int, required=False, default=20)

    def get(self):
        data = StoreList.parse.parse_args()
        pagination = StoreModel.get_items_per_page(**data)
        stores = pagination.items()
        return {"stores": [item.json() for item in stores]}
