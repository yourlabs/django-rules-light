"""

"""
from __future__ import unicode_literals
import six

import django
from django.views import generic

from .exceptions import RulesLightException
from .registry import registry


__all__ = ('class_decorator',)


def patch_get_object(cls, suffix, override):
    old_get_object = cls.get_object

    def new_get_object(self, *args, **kwargs):
        obj = old_get_object(self, *args, **kwargs)

        if self.get_object._rule_override:
            rule_name = self.get_object._rule_override
        else:
            try:
                model_name = obj.__class__._meta.model_name
            except AttributeError:
                model_name = obj.__class__._meta.module_name
            rule_name = '%s.%s.%s' % (obj.__class__._meta.app_label,
                model_name, self.get_object._rule_suffix)

        registry.require(self.request.user, rule_name, obj)

        return obj

    new_get_object._rule_suffix = suffix
    new_get_object._rule_override = override
    cls.get_object = new_get_object


class class_decorator(object):
    """
    Can be used to secure class based views.

    If the view has ``model=YourModel``, it will support:

    - ``CreateView``, it will decorate ``get_form()``, to run
      ``rules_light.require('yourapp.yourmodel.create')``,
    - ``UpdateView``, it will decorate ``get_object()``, to run
      ``rules_light.require('yourapp.yourmodel.update', obj)``,
    - ``DeleteView``, it will decorate ``get_object()``, to run
      ``rules_light.require('yourapp.yourmodel.delete', obj)``,
    - ``DetailView``, it will decorate ``get_object()``, to run
      ``rules_light.require('yourapp.yourmodel.read', obj)``,
    - others views, if the rule name is specified in the decorator for example
      ``@class_decorator('some_rule')``, then it will decorate ``dispatch()``,
    - Else it raises an exception.
    """
    rule = None

    def __new__(self, *args):
        if hasattr(args[0], 'as_view'):
            cls = args[0]
        elif isinstance(args[0], six.string_types):
            if six.PY2:
                decorator_name = b'new_class_decorator'
            elif six.PY3:
                decorator_name = 'new_class_decorator'

            new_class_decorator = type(decorator_name,
                (class_decorator,), {'rule': args[0]})
            return new_class_decorator
        elif hasattr(args[0], '__call__'):
            raise Exception("No function support")
        else:
            raise Exception("What?")

        if issubclass(cls, generic.CreateView):
            old_get_form = cls.get_form

            if django.VERSION >= (1, 8):
                def new_get_form(self, *args, **kwargs):
                    model = self.get_form_class().Meta.model
                    try:
                        model_name = model._meta.model_name
                    except AttributeError:
                        model_name = model._meta.module_name
                    rule_name = '%s.%s.create' % (model._meta.app_label,
                        model_name)

                    registry.require(self.request.user, rule_name)

                    return old_get_form(self, *args, **kwargs)

            else:
                def new_get_form(self, form_class, *args, **kwargs):
                    model = form_class.Meta.model
                    try:
                        model_name = model._meta.model_name
                    except AttributeError:
                        model_name = model._meta.module_name
                    rule_name = '%s.%s.create' % (model._meta.app_label,
                        model_name)

                    registry.require(self.request.user, rule_name)

                    return old_get_form(self, form_class, *args, **kwargs)

            cls.get_form = new_get_form

        elif issubclass(cls, generic.UpdateView):
            patch_get_object(cls, 'update', self.rule)

        elif issubclass(cls, generic.DetailView):
            patch_get_object(cls, 'read', self.rule)

        elif issubclass(cls, generic.DeleteView):
            patch_get_object(cls, 'delete', self.rule)

        elif self.rule:
            old_dispatch = cls.dispatch

            def new_dispatch(self, request, *args, **kwargs):
                registry.require(request.user, self.dispatch._rule)
                return old_dispatch(self, request, *args, **kwargs)
            new_dispatch._rule = self.rule
            cls.dispatch = new_dispatch

        else:
            raise RulesLightException('Dont understand what to do')

        return cls
