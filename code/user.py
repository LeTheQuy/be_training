import sqlite3

from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(self, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "Select * from users where username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = User(row[0], row[1], row[2])
        else:
            user = None
        connection.commit()
        connection.close()
        return user

    @classmethod
    def find_by_id(self, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "Select * from users where id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = User(row[0], row[1], row[2])
        else:
            user = None

        connection.commit()
        connection.close()
        return user


class UserRegister(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("username", type=str, required=True, help="This field can not be blank!")
    parse.add_argument("password", type=str, required=True, help="This field can not be blank!")

    def post(self):
        data = UserRegister.parse.parse_args()

        if User.find_by_username(data["username"]):
            return {"message": "duplicated username"}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "Insert Into users values(NULL,?,?)"
        cursor.execute(query, (data["username"], data["password"]))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201
