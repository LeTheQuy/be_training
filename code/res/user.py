from flask_restful import Resource, reqparse

from code.models.user import UserModel


class UserRegister(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("username", type=str, required=True, help="This field can not be blank!")
    parse.add_argument("password", type=str, required=True, help="This field can not be blank!")

    def post(self):
        data = UserRegister.parse.parse_args()

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
            return {"messsage": "User not found"}, 404
        return user.json()
        pass

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"messsage": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted"}, 200
