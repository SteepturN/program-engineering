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


def connect_cache(cache_type):
    import redis
    password = os.environ.get('CACHE_PASSWORD', 'redis')
    host = os.environ.get('CACHE_HOST', 'localhost')
    db = {'users': 0, 'passwords': 1}.get(cache_type, 2)
    return redis.Redis(host=host, port=6379, db=db)#, password=password)


kafka_topic = os.getenv('KAFKA_TOPIC', 'some_topic')


def kafka_producer():
    from kafka import KafkaProducer
    host = os.getenv('KAFKA_HOST', 'localhost')
    port = os.getenv('KAFKA_PORT', '9092')
    KAFKA_ADDRESS = f"{host}:{port}"
    return KafkaProducer(bootstrap_servers=KAFKA_ADDRESS)

def kafka_consumer():
    from kafka import KafkaConsumer
    host = os.getenv('KAFKA_HOST', 'localhost')
    port = os.getenv('KAFKA_PORT', '9092')
    return KafkaConsumer(
        kafka_topic,
        bootstrap_servers=[f"{host}:{port}", f"{host}:9092",
                           f"{host}:29092"],
        auto_offset_reset='earliest',
        group_id='my-group',
        session_timeout_ms=30000,  # 30 seconds
        max_poll_interval_ms=300000,  # 5 minutes
        heartbeat_interval_ms=1000,  # 1 second
        consumer_timeout_ms=1000
    )
