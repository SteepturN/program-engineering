#!/usr/bin/env python3

from db import User
from collections import defaultdict
from pydantic import BaseModel

class Message(BaseModel):
    id: str
    text: str
    to_email: str


messages = defaultdict(lambda: dict())


def get_message(current_user: User, message_id: str):
    return messages.get(current_user.email, {}).get(message_id, None)

def add_message(current_user: User, message: Message):
    messages[current_user.email][message.id] = message
    return message
