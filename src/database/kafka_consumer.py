#!/usr/bin/env python3
import time
import json
from session_params import kafka_consumer
from user_db import add_record_user_db, User
consumer = kafka_consumer()


def consume_messages(times=1):
    for _ in range(times):
        for message in consumer:
            message_value = message.value.decode('utf-8')
            user = User(**json.loads(message_value))
            add_record_user_db(user)


if __name__ == "__main__":
    try:
        while True:
            time.sleep(5)
            consume_messages()
    except Exception as e:
        consumer.close()
        raise e
