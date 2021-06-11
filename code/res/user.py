
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("username", type=str, required=True, help="This field can not be blank!")
    parse.add_argument("password", type=str, required=True, help="This field can not be blank!")

    def post(self):
        data = UserRegister.parse.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "duplicated username"}, 400

        user = UserModel(data["username"], data["password"])
        user.save_to_db()
        return {"message": "User created successfully"}, 201
