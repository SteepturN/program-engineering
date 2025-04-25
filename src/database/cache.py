#!/usr/bin/env python3
from session_params import connect_cache
from db import User, Password


def write_transform(value):
    if isinstance(value, bool):
        return f'bool:{value}'
    return value


def read_transform(value):
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    if isinstance(value, str) and value.startswith('bool:'):
        return True if value[len('bool:'):] == 'True' else False
    return value


class Cache:
    def __init__(self, cache_type):
        self.cache = connect_cache(cache_type)
        self.return_type = {
            'users': User,
            'passwords': Password,
        }[cache_type]

    def set(self, key, value, expire=1000):
        value = {k: write_transform(v) for k, v in value.asdict().items()}
        # print(value, flush=True)
        return self.cache.hset(key, mapping=value)

    def get(self, key):
        if res := self.cache.hgetall(key):
            res = {k.decode('utf-8'): read_transform(v) for k, v in res.items()}
            return self.return_type(**res)
        else:
            return None

    def delete(self, key):
        return self.cache.delete(key)
