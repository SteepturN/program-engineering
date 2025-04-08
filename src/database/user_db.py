#!/usr/bin/env python3
from db import User
from session_params import create_users_db_engine
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

engine = create_users_db_engine()


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
            user = session.execute(get_user).scalar_one()
            for key, val in update_params.items():
                setattr(user, key, val)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    return True


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
    return get_record_user_db(username)


def add_user(user: User):
    return add_record_user_db(user)


def delete_user(user: User):
    try:
        with Session(engine) as session:
            session.delete(user)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    return True


def is_admin(user: User):
    if user:
        return user.role == 'admin'
