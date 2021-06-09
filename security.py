from werkzeug.security import safe_str_cmp

from user import User

users = [
    User(1, "Quydz", "123456")
]

username_mapping = {
    u.username for u in users
}

userid_mapping = {
    u.id for u in users
}


def authentication(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user["password"], password):
        return user


def identify(payload):
    user_id = payload["identify"]
    return userid_mapping.get(user_id, None)
