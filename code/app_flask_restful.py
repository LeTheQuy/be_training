import os

from flask import Flask
from flask_jwt_extended import JWTManager

from flask_restful import Api

from code.res.item import Item, ItemList
from code.res.store import StoreList, Store
from code.res.user import UserRegister, User, UserLogin

app = Flask(__name__)
uri = os.environ.get("DATABASE_URL", "sqlite:///../data.db")

if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = "quydz"
app.secret_key = "quydz"
api = Api(app)

jwt = JWTManager(app)

api.add_resource(Item, "/items/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/stores/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/users/<int:user_id>")
api.add_resource(UserLogin, "/login")

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
