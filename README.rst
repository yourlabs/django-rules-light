.. image:: https://secure.travis-ci.org/jpic/django-rules-light.png?branch=master

This is a simple alternative to django-rules. The core difference is that
it uses as registry that can be modified on runtime, instead of database
models.

One of the goal is to enable developpers of external apps to make rules, depend
on it, while allowing a project to override rules.

That's all folks !

What's the catch ?
------------------

The catch is that this approach does not offer any feature to get secure
querysets.

This means that the developper has to:

- think about security when making querysets,
- `override
  <http://blog.yourlabs.org/post/19777151073/how-to-override-a-view-from-an-external-django-app>`_
  eventual external app ListViews,

Requirements
------------

- Maintained against Python 2.7
- and Django 1.4+

Install
-------

- Install module: ``pip install django-rules-light``,
- Add to ``settings.INSTALLED_APPS``: ``rules_light``,
- Add in ``settings.MIDDLEWARE_CLASSES``: ``rules_light.middleware.Middleware``,
- Add in ``urls.py``: ``rules_light.autodiscover()``,

Usage
-----

Declaring rules
>>>>>>>>>>>>>>>

In your app, create ``rules_light_registry.py``, simple example::

    import rules_light

    # Allow all users to create a form by default, the point of having that is
    # to allow a project that uses form_designer to change this rule.
    rules_light.registry.setdefault('form_designer.form.create', True)

    # The callback takes the user as first argument, permission as second, then
    # args and kwargs which leaves you completely free:
    rules_light.registry.setdefault('form_designer.form.update', 
        lambda u, n, f: user == f.author)

The first thing you should note is that ``rules_light.registry`` is a simple
python dictionnary. This keeps everything simple and lightweight.

Overriding rules
>>>>>>>>>>>>>>>>

Also note that we're using the standard dictionnary ``setdefault()`` method.
This allows your app to set the default condition for a rule, which can be
easily overridden at project level before or after this code is ran by
``autodiscover()`` as such::

    def user_in_app_maitainers(user, rule, form):
        return user in form.appform.app.maintainers

    rules_light.registry['form_designer.form.update'] = user_in_app_maitainers

Using rules
>>>>>>>>>>>

Decorator
<<<<<<<<<

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

Require
<<<<<<<

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

Manifesto
---------

Sorry if this is too simple or stupid but I'm pretty sure it's better to use
this rather than to hardcode security constraints in my apps ``django-apstore``
and ``django-form-designer`` which will be open sourced in a little while.

One day, I asked for help on IRC on a crappy piece of code. Some hacker "hurt
my feelings" about it and I decided that my days writing crappy code were over.

One of the decisions I took was that my private projects should never be a
dependency for an app. Every app that I code should be of open-source-able
quality, and make sense on it's own.

This is how django-cities-light and django-autocomplete-light were born.

Then, I was asked to code an appstore which allows admin to create apps, where
one app=one form. So I coded django-appstore and django-form-designer (still
closed source) apart, each with it's own test_project.

Of course, I started with simple security:

- in django-form-designer, check if ``request.user == form.author`` in
  ``FormUpdateView``,
- in django-appstore, check something like ``request.user == app.author``,

When I came to code ``appstore.contrib.form_designer_appeditor``, the app that
couples django-appstore and django-form-designer, I figured that this would
require to add code to sync ``app.author`` and ``form.author``. Which seemed
ugly. Also, considering the number of security rules that my project require,
it was time to factor out the security constraints.

django-rules-light is born.

Resources
---------

You could subscribe to the mailing list ask questions or just be informed of
package updates.

- `Mailing list graciously hosted
  <http://groups.google.com/group/yourlabs>`_ by `Google
  <http://groups.google.com>`_
- `Git graciously hosted
  <https://github.com/jpic/django-rules-light/>`_ by `GitHub
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
