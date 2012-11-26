from django.views import generic

from exceptions import RulesLightException
from registry import registry


__all__ = ('class_decorator',)


def patch_get_object(cls, suffix, override):
    old_get_object = cls.get_object

    def new_get_object(self):
        obj = old_get_object(self)

        if self.get_object._rule_override:
            rule_name = self.get_object._rule_override
        else:
            rule_name = '%s.%s.%s' % (obj.__class__._meta.app_label,
                obj.__class__._meta.module_name, self.get_object._rule_suffix)

        registry.require(self.request.user, rule_name, obj)

        return obj

    new_get_object._rule_suffix = suffix
    new_get_object._rule_override = override
    cls.get_object = new_get_object


class class_decorator(object):
    rule = None

    def __new__(self, *args):
        if hasattr(args[0], 'as_view'):
            cls = args[0]
        elif isinstance(args[0], basestring):
            new_class_decorator = type('new_class_decorator',
                (class_decorator,), {'rule': args[0]})
            return new_class_decorator
        elif hasattr(args[0], '__call__'):
            raise Exception("No function support")
        else:
            raise Exception("What?")

        if issubclass(cls, generic.CreateView):
            old_get_form = cls.get_form

            def new_get_form(self, form_class):
                model = form_class.Meta.model
                rule_name = '%s.%s.create' % (model._meta.app_label,
                    model._meta.module_name)

                registry.require(self.request.user, rule_name)

                return old_get_form(self, form_class)

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
