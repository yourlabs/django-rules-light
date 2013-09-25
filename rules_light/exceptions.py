from __future__ import unicode_literals


class RulesLightException(Exception):
    """ Base class for all exceptions of this package. """
    pass


class Denied(RulesLightException):
    def __init__(self, rule_text):
        super(Denied, self).__init__(u'%s evaluates to False' % rule_text)


class DoesNotExist(RulesLightException):
    def __init__(self, name):
        super(DoesNotExist, self).__init__(
            u'Rule "%s" is not registered' % name)
