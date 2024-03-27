#!/usr/bin/env python3
"""
Module contains a script that stores strings into the
redis server
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """ Stores data in a data key """

    def __init__(self) -> None:
        """
        Initializes a class that enables writing of a string
        into a redis server or client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, int, bytes, float]) -> str:
        """Method that generates a key randomly to store data"""
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
