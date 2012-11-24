.. image:: https://secure.travis-ci.org/yourlabs/django-rules-light.png?branch=master

This is a simple alternative to django-rules. The core difference is that
it uses as registry that can be modified on runtime, instead of database
models.

The goal is to enable developpers of external apps to make rules, depend
on it, while allowing a project to override rules.

Requirements
------------

- Maintained against Python 2.7
- and Django 1.4+

Install
-------

- Install module: ``pip install django-rules-light``,
- Add to ``settings.INSTALLED_APPS``: ``rules_light``,
- Add in ``urls.py``: ``rules_light.autodiscover()``,

Usage
-----

In your app, create ``rules_light_registry.py``, simple example::

    import rules_light

    # Allow all users to create a form by default, the point of having that is
    # to allow a project that uses form_designer to change this rule.
    rules_light.register('form_designer.form.create', True)

    # The callback takes the user as first argument, permission as second, then
    # args and kwargs which leaves you completely free:
    rules_light.register('form_designer.form.update',
        lambda user, perm, form: user == form.author)

Note that ``rules_light.autodiscover()`` imports ``rules_light_registry.py`` from
the first to the last app. Suppose that you want to **forbid** users from
creating a form - because forms should be created programatically - then you
could::

    rules_light.unregister()
    rules_light.register('form_designer.form.create', False)

Or use the ``reregistrer()`` shortcut::

    rules_light.reregister('form_designer.form.create', False)

Using a simple decorator to do the obvious thing, check for
``form_designer.form.create`` in a ``CreateView`` that has ``model=Form``, DRY::

    # This decorator is not bulletproof, but will work with common cases
    @rules_light.decorator
    class FormCreateView(generic.CreateView):
        model = Form
        template_name = 'form_designer/form_create.html'
        form_class = FormCreateForm

We can also override the default permission it would check. For example, we're
using a DetailView with ``post()`` for updates, instead of a classic UpdateView.
This allows us to have a nice ajax-ish interface.

Anyway, the decorator would check for ``form_designer.form.read`` (if it has been
defined) by default for a DetailView, let's override that::

    @rules_light.decorator('form_designer.form.update')
    class FormUpdateView(generic.DetailView):
        template_name = 'form_designer/form_update.html'

        def post(self, request, *args, **kwargs):
            # [...] ajax stuff :)

If a user has permission to modify a form, then he should be able to create,
modify and delete widgets of that form. That's kind of indirect so we can't use
a decorator, let's just use ``rules_light.require()`` instead::

    class WidgetSecurity(object):
        """
        Decorate ``get_object()``, to test if user has update permission on the form.
        """
        def get_object(self):
            widget = super(WidgetSecurity, self).get_object()
            rules_light.require(self.request.user, 'form_designer.form.update',
                    widget.tab.form)
            return widget


    class WidgetUpdateView(PkUrlKwarg, WidgetSecurity, WidgetFormMixin,
            AjaxFormMixin, generic.UpdateView):
        form_class = WidgetForm


    class WidgetDeleteView(PkUrlKwarg, WidgetSecurity, AjaxDeleteView):
        pass

Resources
---------

You could subscribe to the mailing list ask questions or just be informed of
package updates.

- `Mailing list graciously hosted
  <http://groups.google.com/group/yourlabs>`_ by `Google
  <http://groups.google.com>`_
- `Git graciously hosted
  <https://github.com/yourlabs/django-rules-light/>`_ by `GitHub
  <http://github.com>`_,
- `Documentation graciously hosted
  <http://django-rules-light.rtfd.org>`_ by `RTFD
  <http://rtfd.org>`_ (not yet operational),
- `Package graciously hosted
  <http://pypi.python.org/pypi/django-rules-light/>`_ by `PyPi
  <http://pypi.python.org/pypi>`_ (not yet),
- `Continuous integration graciously hosted
  <http://travis-ci.org/yourlabs/django-rules-light>`_ by `Travis-ci
  <http://travis-ci.org>`_ (not yet)
