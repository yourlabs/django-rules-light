import logging

from exceptions import Denied, DoesNotExist

__all__ = ('RuleRegistry', 'registry', 'require', 'run')


class RuleRegistry(dict):
    def __init__(self):
        self.logger = logging.getLogger('rules_light')

    def __setitem__(self, key, value):
        super(RuleRegistry, self).__setitem__(key, value)
        self.logger.debug(u'[rules_light] "%s" registered with: %s' % (
            key, value))

    def run(self, user, name, *args, **kwargs):
        if name not in self:
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
        result = self.run(user, name, *args, **kwargs)

        if not result:
            text = self.as_text(user, name, *args, **kwargs)
            self.logger.warn(u'[rules_light] Deny %s' % text)
            raise Denied(text)

    def as_text(self, user, name, *args, **kwargs):
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
    return registry.run(user, name, *args, **kwargs)


def require(user, name, *args, **kwargs):
    registry.require(user, name, *args, **kwargs)
