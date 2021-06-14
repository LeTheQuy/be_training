import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from code.res.item import Item, ItemList
from code.res.store import StoreList, Store
from code.security import authentication, identify
from code.res.user import UserRegister

app = Flask(__name__)
uri = os.environ.get("DATABASE_URL", "sqlite:///../data.db")

if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "quydz"
api = Api(app)

jwt = JWT(app, authentication, identify)

api.add_resource(Item, "/items/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/stores/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
