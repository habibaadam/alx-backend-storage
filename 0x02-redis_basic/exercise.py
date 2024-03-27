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
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return value

    def get_str(self, key: str) -> str:
        """
        Method that converts the data back into a string
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return data.decode('utf-8')

    def get_int(self, key):
        """Method used to convert data back into an int"""
        data = self._redis.get(key)
        if data is None:
            return None
        return int(data.decode('utf-8'))
