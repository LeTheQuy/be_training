from flask_jwt import jwt_required
from flask_restful import Resource

from models.store import StoreModel


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

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_on_db()
        return {"message": "Store deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": list(map(lambda x: x.json(), StoreModel.query.all()))}