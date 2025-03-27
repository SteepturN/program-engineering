#!/usr/bin/env python3
import password_db
from db import User

user_db = {
    "admin": User(username="admin", email='admin@admin.com', disabled=False),
}
admin_db = {
    "admin": {}
}





def get_record_user_db(username: str):
    return user_db.get(username, None)

def add_record_user_db(user: User):
    if user.username in user_db:
        return None
    user_db[user.username] = user
    return user




def get_user(type: str, username: str):
    if type == "username":
        return get_record_user_db(username)

def add_user(user: User, password: str):
    if res := add_record_user_db(user):
        password_db.add_record_password_db(user, password)
    return res

def is_admin(user: User):
    return user.username in admin_db
