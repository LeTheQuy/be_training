import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from flask_restful import Api

from code.res.item import Item, ItemList
from code.res.store import StoreList, Store
from code.res.user import UserRegister, User, UserLogin, TokenRefresh, BLACKLIST, UserLogout

app = Flask(__name__)
uri = os.environ.get("DATABASE_URL", "sqlite:///../data.db")

if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = "quydz"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

app.secret_key = "quydz"
api = Api(app)

jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    else:
        return {"is_admin": False}


@jwt.expired_token_loader
def expired_token_callback(jwt_headers, jwt_payload):
    return jsonify({
        "description": "Token has expired",
        "error": "token_expired",
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify(
        {
            "description": "Signature verification failed",
            "error": "invalid token"
        }
    )


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify(
        {
            "description": "The token have been revoked",
            "error": "token_revoked"
        }
    )


api.add_resource(Item, "/items/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/stores/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/users/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
