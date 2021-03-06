from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from res.item import Item, ItemList
from res.store import StoreList, Store
from security import authentication, identify
from res.user import UserRegister

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "quydz"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


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
