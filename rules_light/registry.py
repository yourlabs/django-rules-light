"""
The rule registry is in charge of keeping and executing security rules.

It is the core of this app, everything else is optionnal.

This module provides a variable, ``registry``, which is just a module-level,
default RuleRegistry instance.

A rule can be a callback or a variable that will be evaluated as bool.
"""
import logging

from exceptions import Denied, DoesNotExist

__all__ = ('RuleRegistry', 'registry', 'require', 'run', 'autodiscover')


class RuleRegistry(dict):
    """
    Dict subclass to manage rules.

    logger
        The standard logging logger instance to use.
    """
    def __init__(self):
        self.logger = logging.getLogger('rules_light')

    def __setitem__(self, key, value):
        """
        Adds a debug-level log on registration.
        """
        super(RuleRegistry, self).__setitem__(key, value)
        self.logger.debug(u'[rules_light] "%s" registered with: %s' % (
            key, value))

    def run(self, user, name, *args, **kwargs):
        """
        Run a rule, return True if whatever it returns evaluates to True.

        Also logs calls with the info-level.
        """
        if name not in self:
            self.logger.error(u'[rules_light] Rule does not exist "%s"' % name)
            raise DoesNotExist(name)

        rule = self[name]

        if hasattr(rule, '__call__'):
            result = self[name](user, name, *args, **kwargs)
        else:
            result = rule

        text = self.as_text(user, name, *args, **kwargs)
        if result:
            self.logger.info(u'[rules_light] %s passed' % text)
            return True
        else:
            self.logger.info(u'[rules_light] %s failed' % text)
            return False

    def require(self, user, name, *args, **kwargs):
        """
        Run a rule, raise ``rules_light.Denied`` if returned False.

        Log denials with warn-level.
        """
        result = self.run(user, name, *args, **kwargs)

        if not result:
            text = self.as_text(user, name, *args, **kwargs)
            self.logger.warn(u'[rules_light] Deny %s' % text)
            raise Denied(text)

    def as_text(self, user, name, *args, **kwargs):
        """ Format a rule to be human readable for logging """
        if name not in self:
            raise DoesNotExist(name)

        if hasattr(self[name], '__call__'):
            if not args and not kwargs:
                return u'%s(%s, "%s")' % (
                    self[name], user, name)
            elif args and kwargs:
                return u'%s(%s, "%s", *%s, **%s)' % (
                    self[name], user, name, args, kwargs)
            elif args:
                return u'%s(%s, "%s", *%s)' % (
                    self[name], user, name, args)
            elif kwargs:
                return u'%s(%s, "%s", **%s)' % (
                    self[name], user, name, kwargs)
        else:
            return u'%s is %s' % (name, self[name])


registry = RuleRegistry()


def run(user, name, *args, **kwargs):
    """ Proxy ``rules_light.registry.run()``. """
    return registry.run(user, name, *args, **kwargs)


def require(user, name, *args, **kwargs):
    """ Proxy ``rules_light.registry.require()``. """
    registry.require(user, name, *args, **kwargs)


def _autodiscover(registry):
    """See documentation for autodiscover (without the underscore)"""
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            before_import_registry = copy.copy(registry)
            import_module('%s.rules_light_registry' % app)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'rules_light_registry'):
                raise


def autodiscover():
    """
    Check all apps in INSTALLED_APPS for stuff related to rules_light.

    For each app, autodiscover imports ``app.rules_light_registry`` if
    available, resulting in execution of ``rules_light.registry[...] = ...``
    statements in that module, filling registry.

    Consider a standard app called 'cities_light' with such a structure::

        cities_light/
            __init__.py
            models.py
            urls.py
            views.py
            rules_light_registry.py

    With such a rules_light_registry.py::

        import rules_light

        rules_light.register('cities_light.city.read', True)
        rules_light.register('cities_light.city.update',
            lambda user, rulename, country: user.is_staff)

    When autodiscover() imports cities_light.rules_light_registry, both
    `'cities_light.city.read'` and `'cities_light.city.update'` will be
    registered.
    """
    _autodiscover(registry)
