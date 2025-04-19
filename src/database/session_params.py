#!/usr/bin/env python3
import os

def create_db_engine(database, host, port):
    import sqlalchemy
    users_db_address = os.environ.get('USERS_DB_ADDRESS', None)
    users_db_port = os.environ.get('USERS_DB_PORT', None)

    host = (host if host else
            users_db_address if users_db_address
            else "127.0.0.1")

    port = (port if port else
            users_db_port if users_db_port
            else 5432)

    user = 'postgres'
    password = 'postgres'

    return sqlalchemy.create_engine(
        url=f"postgresql://{user}:{password}@{host}:{port}/{database}"
    )


def create_users_db_engine(host=None, port=None):
    return create_db_engine('users', host, port)


def create_passwords_db_engine(host=None, port=None):
    return create_db_engine('passwords', host, port)


def connect_messages_db_table():
    import pymongo
    from urllib.parse import quote_plus

    username = quote_plus(os.environ.get('MESSAGES_DB_USERNAME', 'root'))
    password = quote_plus(os.environ.get('MESSAGES_DB_PASSWORD', 'root'))
    host = os.environ.get('MESSAGES_DB_HOST', '127.0.0.1')
    port = os.environ.get('MESSAGES_DB_PORT', '27017')

    client = pymongo.MongoClient(f'mongodb://{username}:{password}@{host}:{port}')
    return client['messages-database']["messages"]
