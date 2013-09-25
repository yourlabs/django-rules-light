"""
It is trivial to take shortcuts because the rule registry is a simple dict.

You can reuse your rules several times in standard python::

    def my_model_or_is_staff(user, rule, model, obj=None):
        return user.is_staff or (obj and obj.author == user)

    rules_light.registry.setdefault('your_app.your_model.create',
        my_model_or_is_staff)
    rules_light.registry.setdefault('your_app.your_model.update',
        my_model_or_is_staff)
    rules_light.registry.setdefault('your_app.your_model.delete',
        my_model_or_is_staff)

This module provides some shortcut(s). Shortcuts are also usable as decorators
too (see ``make_decorator``)::

    @rules_light.is_authenticated
    def my_book(user, rule, book):
        return book.author == user

    rules_light.registry.setdefault('your_app.your_model.update', my_book)
"""
from __future__ import unicode_literals

from .decorators import make_decorator

__all__ = ['is_staff', 'is_authenticated']


@make_decorator
def is_staff(user, rulename, *args, **kwargs):
    """
    Return True if user.is_staff.

    For example, in ``your_app/rules_light_registry.py``::

        rules_light.registry.setdefault('your_app.your_model.create',
            rules_light.is_staff)

    Is equivalent to::

        rules_light.registry.setdefault('your_app.your_model.create',
            lambda: user, rulename, *args, **kwargs: user.is_staff)

    Also::

        rules_light.registry.setdefault('your_app.your_model.create',
            rules_light.is_staff(your_rule_callback))

    Is equivalent to::

        def staff_and_stuff(user, rule, *args, **kwargs):
            if not rules_light.is_staff(user, rule, *args, **kwargs):
                return False

            if your_stuff():
                return True

        rules_light.registry.setdefault('your_app.your_model.create',
            rules_light.is_staff(your_rule_callback))
    """
    return user and user.is_staff


@make_decorator
def is_authenticated(user, rulename, *args, **kwargs):
    """
    Return user.is_authenticated().
    """
    return user and user.is_authenticated()
