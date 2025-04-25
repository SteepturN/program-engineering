#!/usr/bin/env python3
from db import User
from session_params import create_users_db_engine
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from cache import Cache

engine = create_users_db_engine()
users_cache = Cache('users')


def delete_record_user_db(username: str):
    select_user = select(User).where(User.username == username)
    try:
        with Session(engine) as session:
            user = session.execute(select_user).scalar_one()
            session.delete(user)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    return True


def update_record_user_db(username: str, update_params: dict):
    get_user = select(User).where(User.username == username)
    try:
        with Session(engine) as session:
            session.expire_on_commit = False
            user = session.execute(get_user).scalar_one()
            for key, val in update_params.items():
                setattr(user, key, val)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    return user


def get_record_user_db(username: str):
    print("username: ", username)
    req = select(User).where(User.username == username)
    try:
        with Session(engine) as session:
            res = session.execute(req).scalar_one()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    return res


def add_record_user_db(user: User):
    try:
        with Session(engine) as session:
            session.expire_on_commit = False
            session.add(user)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    return user


def get_user(username: str):
    if not (result := users_cache.get(username)):
        result = get_record_user_db(username)
        users_cache.set(username, result)
    return result


def add_user(user: User):
    users_cache.set(user.username, user)
    return add_record_user_db(user)


def update_user(username: str, update_params: dict):
    if result := update_record_user_db(username, update_params):
        users_cache.set(username, result)
    return result


def delete_user(user: User):
    try:
        with Session(engine) as session:
            session.delete(user)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    users_cache.delete(user.username)
    return True


def is_admin(user: User):
    return user and user.role == 'admin'
