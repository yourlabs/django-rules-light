"""
This module enables piling rules on each others.

Consider this simple rule::

    def is_authenticated(user, *args, **kwargs):
        return user and user.is_authenticated()

It can of course be used directly::

    rules_light.registry['do_something'] = is_authenticated

But if defined using ``make_decorator`` as such::

    @rules_light.make_decorator
    def is_authenticated(user, *args, **kwargs):
        return user and user.is_authenticated()

Then you can use it to decorate other rules too::

    @is_authenticated
    def my_book(user, rule, book):
        return user == book.author

    rules_light.registry['do_something'] = my_book

"""
from __future__ import unicode_literals


def make_decorator(_rule):
    def _decorator(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            func = args[0]

            def _decorated(user, rule, *args, **kwargs):
                if not _rule(user, rule, *args, **kwargs):
                    return False
                return func(user, rule, *args, **kwargs)
            _decorated.__name__ = func.__name__
            return _decorated
        else:  # rule
            return _rule(*args, **kwargs)
    _decorator.__name__ = _rule.__name__
    return _decorator
