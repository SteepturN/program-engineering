#!/usr/bin/env python3
from passlib.context import CryptContext
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select


from db import User, Password
from session_params import create_passwords_db_engine

engine = create_passwords_db_engine()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def update_password(username, password):
    return update_record_password_db(username, {'hashed_password': get_password_hash(password)})


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
            user = session.execute(select_user).scalar_one()
            for key, val in update_params.items():
                setattr(user, key, val)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    return True


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
    val = Password(username=user.username,
                   hashed_password=get_password_hash(password))
    try:
        with Session(engine) as session:
            session.add(val)
            session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return None
    return True


add_user = add_record_password_db


def authenticate_user(username: str, password: str):
    password_record = get_record_password_db(username)
    # better not to reveal that user is in the db
    if not (password_record and verify_password(password, password_record.hashed_password)):
        return False
    return password_record
