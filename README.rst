.. image:: https://secure.travis-ci.org/yourlabs/django-rules-light.png?branch=master
    :target: http://travis-ci.org/yourlabs/django-rules-light
.. image:: https://pypip.in/d/django-rules-light/badge.png
    :target: https://crate.io/packages/django-rules-light
.. image:: https://pypip.in/v/django-rules-light/badge.png   
    :target: https://crate.io/packages/django-rules-light

This is a simple alternative to django-rules. The core difference is that
it uses as registry that can be modified on runtime, instead of database
models.

One of the goal is to enable developpers of external apps to make rules, depend
on it, while allowing a project to override rules.

Example ``your_app/rules_light_registry.py``:

.. code-block:: python

    # Everybody can read a blog post (for now!):
    rules_light.registry['blog.post.read'] = True

    # Require authentication to create a blog post, using a shortcut:
    rules_light.registry['blog.post.create'] = rules_light.is_authenticated

    def is_staff_or_mine(user, rule, obj):
        return user.is_staff or obj.author == user
    
    # But others shouldn't mess with my posts !
    rules_light.registry['blog.post.update'] = is_staff_or_mine
    rules_light.registry['blog.post.delete'] = is_staff_or_mine

Example ``your_app/views.py``:

.. code-block:: python

    @rules_light.class_decorator
    class PostDetailView(generic.DetailView):
        model = Post
     
    @rules_light.class_decorator
    class PostCreateView(generic.CreateView):
        model = Post
     
    @rules_light.class_decorator
    class PostUpdateView(generic.UpdateView):
        model = Post
   
    @rules_light.class_decorator
    class PostDeleteView(generic.DeleteView):
        model = Post

You might want to read the `tutorial
<https://django-rules-light.readthedocs.org/en/latest/tutorial.html>`_ for
more.

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

- Python 2.7+ (Python 3 supported)
- Django 1.4+

Quick Install
-------------

- Install module: ``pip install django-rules-light``,
- Add to ``settings.INSTALLED_APPS``: ``rules_light``,
- Add in ``settings.MIDDLEWARE_CLASSES``: ``rules_light.middleware.Middleware``,
- Add in ``urls.py``: ``rules_light.autodiscover()``,

You might want to read the `tutorial
<https://django-rules-light.readthedocs.org/en/latest/tutorial.html>`_.

There is also a lot of documentation, from the core to the tools, including
pointers to debug, log and test your security.

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
  <http://rtfd.org>`_,
- `Package graciously hosted
  <http://pypi.python.org/pypi/django-rules-light/>`_ by `PyPi
  <http://pypi.python.org/pypi>`_,
- `Continuous integration graciously hosted
  <http://travis-ci.org/yourlabs/django-rules-light>`_ by `Travis-ci
  <http://travis-ci.org>`_
