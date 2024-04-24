from itertools import islice, chain
from functools import partial
from collections.abc import Sequence
from collections import deque

names = ['mina', 'bita', 'hossein']
ages = [24, 18, 30]
lastnames = ['jalili', 'nabi', 'rezaei']
_marker = object()


def take(iterable, n):
    return list(islice(iterable, n))


def chunked(iterable, n, strict=False):
    iterator = iter(partial(take, iter(iterable), n), [])
    if strict:
        if n is None:
            raise ValueError("n can't be none!")

        def ret():
            for chunk in iterator:
                if len(chunk) != n:
                    raise ValueError("iterable isn't divisible by n!")
                else:
                    yield chunk

        return iter(ret())
    else:
        return iterator


def first(iterable, default=_marker):
    try:
        return next(iter(iterable))
    except StopIteration as e:
        if default is _marker:
            raise ValueError("first() was called on an empty iterable , no default was provided.") from e
        return default
    except TypeError as e:
        if default is _marker:
            raise TypeError("first() was called on a not iterable object, no default was provided.") from e
        return default


def last(iterable, default=_marker):
    try:
        if isinstance(iterable, Sequence):
            return iterable[-1]
        elif hasattr(iterable, '__reversed__'):
            return next(reversed(iterable))
        else:
            return deque(iterable, maxlen=1)[0]
    except (IndexError, StopIteration):
        if default is _marker:
            raise ValueError("last() was called on an empty iterable , no default was provided.")
        return default
    except TypeError as e:
        if default is _marker:
            raise TypeError("last() was called on a not iterable object , no default was provided.") from e
        return default


def nth_or_last(iterable, n, default=_marker):
    return last(islice(iterable, n + 1), default=default)


def one(iterable, too_short=None, too_long=None):
    iterable = iter(iterable)
    try:
        first_value = next(iterable)
    except StopIteration as e:
        raise (
                too_short or ValueError('too few items in iterable (expected 1).')
        ) from e
    try:
        second_value = next(iterable)
    except StopIteration:
        pass
    else:
        message = 'Expected exactly one item in iterable, but got {!r}, {!r}.'.format(first_value, second_value)
        raise (
                too_long or ValueError(message)
        )
    return first_value


def interleave(*iterable):
    return chain.from_iterable(zip(*iterable))
