#!/usr/bin/env python3
from db import User
from cache import Cache
from user_db import get_record_user_db, update_record_user_db, delete_record_user_db


users_cache = Cache('users')


def get_user(username: str):
    if not (result := users_cache.get(username)):
        result = get_record_user_db(username)
        users_cache.set(username, result)
    return result


def add_user(user: User):
    try:
        users_cache.set(user.username, user)
    except Exception as e:
        raise e
    return user


def update_user(username: str, update_params: dict):
    if result := update_record_user_db(username, update_params):
        users_cache.set(username, result)
    return result


def delete_user(user: User):
    delete_record_user_db(user.username)
    users_cache.delete(user.username)
    return True


def is_admin(user: User):
    return user and user.role == 'admin'
