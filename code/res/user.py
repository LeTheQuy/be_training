from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from code.models.user import UserModel

_user_parse = reqparse.RequestParser()
_user_parse.add_argument("username", type=str, required=True, help="This field can not be blank!")
_user_parse.add_argument("password", type=str, required=True, help="This field can not be blank!")


class UserRegister(Resource):

    def post(self):
        data = _user_parse.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "duplicated username"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully"}, 201


class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()
        pass

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted"}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parse.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user and user.password == data["password"]:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token,
                    "refresh_token": refresh_token}, 200
        else:
            return {"message": "User not found"}, 401


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id, fresh=False)
        return {"access_token": new_token}, 200
