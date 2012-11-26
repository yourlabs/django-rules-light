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
  <https://github.com/jpic/django-rules-light/>`_ by `GitHub
  <http://github.com>`_,
- `Documentation graciously hosted
  <http://django-rules-light.rtfd.org>`_ by `RTFD
  <http://rtfd.org>`_,
- `Package graciously hosted
  <http://pypi.python.org/pypi/django-rules-light/>`_ by `PyPi
  <http://pypi.python.org/pypi>`_ (not yet),
- `Continuous integration graciously hosted
  <http://travis-ci.org/jpic/django-rules-light>`_ by `Travis-ci
  <http://travis-ci.org>`_
