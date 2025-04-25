#!/usr/bin/env python3
from passlib.context import CryptContext
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select


from db import User, Password
from session_params import create_passwords_db_engine
from cache import Cache

engine = create_passwords_db_engine()
passwords_cache = Cache('passwords')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def delete_record_password_db(username: str):
    select_user = select(Password).where(Password.username == username)
    try:
        with Session(engine) as session:
            user = session.execute(select_user).scalar_one()
            session.delete(user)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    return True


def update_record_password_db(username: str, update_params: dict):
    select_user = select(Password).where(Password.username == username)
    try:
        with Session(engine) as session:
            session.expire_on_commit = False
            user = session.execute(select_user).scalar_one()
            for key, val in update_params.items():
                setattr(user, key, val)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    return user


def get_record_password_db(username: str):
    req = select(Password).where(Password.username == username)
    try:
        with Session(engine) as session:
            res = session.execute(req).scalar_one()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    return res


def add_record_password_db(user: User, password: str):
    password = get_password_hash(password)
    val = Password(username=user.username,
                   hashed_password=password)
    try:
        with Session(engine) as session:
            session.expire_on_commit = False
            session.add(val)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    return val


def add_user(user: User, password: str):
    if password_record := add_record_password_db(user, password):
        return passwords_cache.set(user.username, password_record)
    return password_record


def get_password(username: str):
    if not (password_record := passwords_cache.get(username)):
        password_record = get_record_password_db(username)
        passwords_cache.set(username, password_record)
    return password_record


def update_password(username, password):
    if result := update_record_password_db(
            username, {'hashed_password': get_password_hash(password)}):
        passwords_cache.set(username, result)
    return result


def delete_password(username):
    passwords_cache.delete(username)
    delete_record_password_db(username)


def authenticate_user(username: str, password: str):
    # better not to reveal that user is in the db
    password_record = get_password(username)
    if not (password_record and verify_password(password, password_record.hashed_password)):
        return False
    return password_record
