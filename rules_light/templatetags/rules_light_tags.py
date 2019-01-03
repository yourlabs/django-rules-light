import inspect

from django import template

from classytags.core import Options
from classytags.helpers import AsTag
from classytags.arguments import (Argument, MultiKeywordArgument,
                                  MultiValueArgument)

import rules_light

register = template.Library()


@register.filter
def rule_code(registry, name):
    rule = registry[name]

    if hasattr(rule, '__call__'):
        return inspect.getsource(rule)

    return repr(rule)


class Rule(AsTag):
    options = Options(
        Argument('rule_name'),
        MultiValueArgument('args', required=False),
        MultiKeywordArgument('kwargs', required=False),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, rule_name, args, kwargs):
        return rules_light.run(context.request.user, rule_name, *args,
                               **kwargs)

register.tag(Rule)
