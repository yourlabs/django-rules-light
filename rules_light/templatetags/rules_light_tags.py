import inspect

from django import template

register = template.Library()


@register.filter
def rule_code(registry, name):
    rule = registry[name]

    if hasattr(rule, '__call__'):
        return inspect.getsource(rule)

    return repr(rule)
