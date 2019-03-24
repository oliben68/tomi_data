import functools
from typing import Iterable

from neo4j import BoltStatementResult
from tomi_base.collections import flatten_lists


def before_operations(*methods):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            # running the decorator method(s) first
            for method in methods:
                result = method(*args, **kwargs)
                if isinstance(result, Iterable):
                    results += list(result)
                else:
                    results.append(result)

            result = func(*args, **kwargs)
            if isinstance(result, Iterable):
                results += list(result)
            else:
                results.append(result)
            return [result for result in flatten_lists(results) if type(result) == BoltStatementResult]

        return wrapper

    return decorator


def after_operations(*methods):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # running the decorated method first
            results = []
            result = func(*args, **kwargs)
            if isinstance(result, Iterable):
                results += list(result)
            else:
                results.append(result)

            for method in methods:
                result = method(*args, **kwargs)
                if isinstance(result, Iterable):
                    results += list(result)
                else:
                    results.append(result)
            return [result for result in flatten_lists(results) if type(result) == BoltStatementResult]

        return wrapper

    return decorator