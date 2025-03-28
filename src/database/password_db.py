#!/usr/bin/env python3
from pydantic import BaseModel
from passlib.context import CryptContext
from db import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

class RecordPasswordDB(BaseModel):
    hashed_password: str

password_db = {
    "admin": get_password_hash('secret'),
}
def get_record_password_db(username: str):
    password = password_db.get(username, None)
    return RecordPasswordDB(hashed_password=password) if password else None

def add_record_password_db(user: User, password: str):
    password_db[user.username] = get_password_hash(password)


def authenticate_user(username: str, password: str):
    user = get_record_password_db(username)
    # better not to reveal that user is in the db
    if not (user and verify_password(password, user.hashed_password)):
        return False
    return user
