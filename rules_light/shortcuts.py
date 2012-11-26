"""
It is trivial to take shortcuts because the rule registry is a simple dict.

You can reuse your rules several times in standard python::

    def my_model_or_is_staff(user, rulename, model, obj=None):
        return user.is_staff or (obj and obj.author == user)

    rules_light.registry.setdefault('your_app.your_model.create',
        my_model_or_is_staff)
    rules_light.registry.setdefault('your_app.your_model.update',
        my_model_or_is_staff)
    rules_light.registry.setdefault('your_app.your_model.delete',
        my_model_or_is_staff)

This module provides some shortcut(s).
"""


def is_staff(user, rulename, *args, **kwargs):
    """
    Return True if user.is_staff.

    For example, in ``your_app/rules_light_registry.py``::

        rules_light.registry.setdefault('your_app.your_model.create',
            rules_light.is_staff)

    Is equivalent to::

        rules_light.registry.setdefault('your_app.your_model.create',
            lambda: user, rulename, *args, **kwargs: user.is_staff)
    """
    return user.is_staff


def is_authenticated(user, rulename, *args, **kwargs):
    """
    Return user.is_authenticated().
    """
    return user.is_authenticated()
