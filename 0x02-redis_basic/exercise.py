#!/usr/bin/env python3
"""
Module contains a script that stores strings into the
redis server
"""
import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        """
        Initializes a class that enables writing of a string
        into a redis server
        """
        # store an instance of the Redis client as a private variable
        self._redis = redis.Redis()
        # flush the instance using flushdb.
        self._redis.flushdb

    # Create a store method that takes a data arg andreturns a string
    # data can be a str, bytes, int or float
    def store(self, data: Union[str, int, bytes, float]) -> str:
        # generate a random key (e.g. using uuid
        key = str(uuid.uuid1())

        # store the input data in Redis using the random key
        self._redis.mset({key: data})
        # return the key
        return key
