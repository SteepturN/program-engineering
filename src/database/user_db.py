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

