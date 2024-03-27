#!/usr/bin/env python3
"""
create a Cache class that will implement a simple cache using Redis
"""

import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """
    a class that stores redis instance as a private variable
    """

    def __init__(self):
        """
        constructor for Cache class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store the input data in redis using a random key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[callable] = None) -> Union[str, bytes,
                                                    int, float]:
        """
        method that take a key string argument and an
        optional Callable argument named fn. This callable will be used
        to convert the data back to the desired format
        """
        if not self._redis.exists(key):
            return None
        if fn is None:
            return self._redis.get(key)
        else:
            return fn(self._redis.get(key))

    def get_str(self, key: str) -> str:
        """
        Method that converts the data back into a string
        """
        if not self._redis.exists(key):
            return None
        return str(self._redis.get(key))

    def get_int(self, key):
        """Method used to convert data back into an int"""
        if not self._redis.exists(key):
            return None
        return int.from_bytes(self._redis.get(key), "big")
