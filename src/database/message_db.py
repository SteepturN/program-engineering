#!/usr/bin/env python3

from db import User, Message

from bson.objectid import ObjectId
from session_params import connect_messages_db_table

messages_db = connect_messages_db_table()


def create_message(_id, from_email, to_email, data):
    return Message(
        id=_id,
        from_email=from_email,
        to_email=to_email,
        data=data)

# automatically creates needed indexes
# messages_db.create_index([("_id", pymongo.ASCENDING)], unique=True)


def get_record_messages_db(current_user: User, message_id: str):
    result = messages_db.find_one({'_id': ObjectId(message_id)})
    if not result or result['from_email'] != current_user.email:
        return None
    result['_id'] = message_id
    return create_message(**result)


def add_record_messages_db(current_user: User, to_email: str, message: str):
    message = dict(from_email=current_user.email,
                   to_email=to_email,
                   data=message)
    id = str(messages_db.insert_one(message).inserted_id)
    return Message(**message | dict(id=id))


def delete_record_messages_db(current_user: User, message_id: str):
    if not get_record_messages_db(current_user, message_id):
        return None
    result = messages_db.delete_one({'_id': ObjectId(message_id)})
    return result.deleted_count


def update_record_messages_db(
        current_user: User, message_id: str, message_update: dict):
    if not get_record_messages_db(current_user, message_id):
        return None
    result = messages_db.update_one(
        {'_id': ObjectId(message_id)}, {'$inc': message_update})
    return result.modified_count
