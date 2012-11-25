from django.views import generic

from registry import registry


__all__ = ('class_decorator',)


def patch_get_object(cls, suffix):
    old_get_object = cls.get_object

    def new_get_object(self):
        obj = old_get_object(self)

        rule_name = '%s.%s.%s' % (obj.__class__._meta.app_label,
            obj.__class__._meta.module_name, self.get_object._rule_suffix)

        registry.require(self.request.user, rule_name, obj)

        return obj

    new_get_object._rule_suffix = suffix
    cls.get_object = new_get_object


class class_decorator(object):
    def __new__(self, *args):
        if hasattr(args[0], 'as_view'):
            cls = args[0]
        elif isinstance(args[0], basestring):
            return class_decorator
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
            patch_get_object(cls, 'update')

        elif issubclass(cls, generic.DetailView):
            patch_get_object(cls, 'read')

        elif issubclass(cls, generic.DeleteView):
            patch_get_object(cls, 'delete')

        return cls
