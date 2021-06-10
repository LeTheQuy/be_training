from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from res.item import Item, ItemList
from security import authentication, identify
from res.user import UserRegister

app = Flask(__name__)

app.secret_key = "quydz"
api = Api(app)

jwt = JWT(app, authentication, identify)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
