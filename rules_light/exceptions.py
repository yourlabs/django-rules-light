class RulesLightException(Exception):
    """ Base class for all exceptions of this package. """
    pass


class Denied(RulesLightException):
    def __init__(self, rule, user, name, *args, **kwargs):
        if hasattr(rule, '__call__'):
            msg = u'%s(%s, %s, %s, %s) evaluates to False' % (
                rule, user, name, args, kwargs)
        else:
            msg = u'%s is %s' % (name, rule)

        super(Denied, self).__init__(msg)


class DoesNotExist(RulesLightException):
    def __init__(self, name):
        super(DoesNotExist, self).__init__(
            u'Rule "%s" is not registered' % name)
