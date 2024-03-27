#!/usr/bin/env python3
"""
create a Cache class that will implement a simple cache using Redis
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Method that returns a count of times the class Cache
    was called """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper for counting calls"""
        self._redis.incr(method.__qualname__, 1)
        result = method(self, *args, **kwargs)
        return result
    return wrapper


def call_history(method: Callable) -> Callable:
    """stores record of method calls"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper for recording calls"""
        self._redis.rpush(method.__qualname__ + ":all_inputs", str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", str(result))
        return result
    return wrapper


def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


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

    @count_calls
    @call_history
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