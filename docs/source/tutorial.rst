Tutorial
========

Install
-------

Either install the last release::

    pip install django-rules-light

Either install a development version::

    pip install -e git+https://github.com/yourlabs/django-rules-light.git#egg=django-rules-light

That should be enough to work with the registry.

Middleware
``````````

To enable the middleware that processes ``rules_light.Denied``
exception, add to ``setings.MIDDLEWARE_CLASSES``:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        # ...
        'rules_light.middleware.Middleware',
    )

See :doc:`docs on middleware</middleware>` for more details.

Autodiscovery
`````````````

To enable autodiscovery of rules in the various apps installed
in your project, add to ``urls.py`` (as early as possible):

.. code-block:: python

    import rules_light
    rules_light.autodiscover()

See :doc:`docs on registry</registry>` for more details.

Logging
```````

To enable logging, add a ``rules_light`` logger for example:

.. code-block:: python

    LOGGING = {
        # ...
        'handlers': {
            # ...
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
            },
        },
        'loggers': {
            'rules_light': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'DEBUG',
            }
        }
    }

See :doc:`docs on logging</logging>` for more details on logging.

Debug view
``````````

Add to ``settings.INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        'rules_light',
        # ....
    )

Then the view should be usable, install it as such:

.. code-block:: python

    url(r'^rules/', include('rules_light.urls')),

See :doc:`docs on debugging</debug>` for more details on debugging rules.

Creating Rules
--------------

Declare rules
`````````````

Declaring rules consist of filling up the ``rules_light.registry`` dict. This
dict uses rule "names" as keys, ie. ``do_something``,
``some_app.some_model.create``, etc, etc ... For values, it can use booleans:

.. code-block:: python

    # Enable read for everybody
    rules_light.registry['your_app.your_model.read'] = True
    
    # Disable delete for everybody
    rules_light.registry['your_app.your_model.delete'] = False

Optionnaly, use the Python dict method ``setdefault()`` in default rules. For
example:

.. code-block:: python

    # Only allow everybody if another (project-specific) callback was not set
    rules_light.registry.setdefault('your_app.your_model.read', True)

It can also use callbacks:

.. code-block:: python

    def your_custom_rule(user, rule_name, model, *args, **kwargs):
        if user in model.your_custom_stuff:
            return True  # Allow user !

    rules_light.registry['app.model.read'] = your_custom_rule
   
See :doc:`docs on registry</registry>` for more details.

Mix rules, DRY security
```````````````````````

Callbacks may also be used to decorate each other, using
``rules_light.make_decorator()`` will transform a simple rule callback, into a
rule callback that can also be used as decorator for another callback.

Just decorate a callback with ``make_decorator()`` to make it reusable as
decorator:

.. code-block:: python

    @rules_light.make_decorator
    def some_condition(user, rule, *args, **kwargs):
        # do stuff

    rules_light.registry.setdefault('your_app.your_model.create', some_condition)

    @some_condition
    def extra_condition(user, rule, *args, **kwargs):
        # do extra stuff

    rules_light.registry.setdefault('your_app.your_model.update', extra_condition)

This will cause ``some_condition()`` to be evaluated first, and if it passes,
``extra_condition()`` will be evaluated to, for the update rule.

See :doc:`docs on decorator</decorator>` for more details.

Using rules
-----------

The rule registry is in charge of using rules, using the ``run()`` method. It
should return True or False.

Run
```

For example with this:

.. code-block:: python

    def some_condition(user, rulename, *args, **kwargs):
        # ...
    
    rules_light.registry['your_app.your_model.create'] = some_condition

Doing:

.. code-block:: python

    rules_light.run(request.user, 'your_app.your_model.create')

Will call:

.. code-block:: python

    some_condition(request.user, 'your_app.your_model.create')

Kwargs are forwarded, for example:

.. code-block:: python

    rules_light.run(request.user, 'your_app.your_model.create',
        with_widget=request.GET['widget'])

Will call:

.. code-block:: python

    some_condition(request.user, 'your_app.your_model.create',
        with_widget=request.GET['widget'])

See :doc:`docs on registry</registry>` for more details.

Require
```````

The ``require()`` method is useful too, it does the same as ``run()`` except
that it will raise ``rules_light.Denied``. This will block the request process
and will be catched by the middleware if installed.

See :doc:`docs on registry</registry>` for more details.

Decorator
`````````

You can decorate a class based view as such:

.. code-block:: python

    @rules_light.class_decorator
    class SomeCreateView(views.CreateView):
        model=SomeModel

This will automatically require ``'some_app.some_model.create'``.

See :doc:`docs on class decorator</class_decorator>` for more usages of the decorator.

Template
````````

In templates, you can run rules using '{% rule %}' templatetag. 

Usage:

.. code-block:: django

    {% rule rule_name [args] [kwargs] as var_name %}

This is an example from the test project:

.. code-block:: django

    {% load rules_light_tags %}

    <ul>
    {% for user in object_list %}
        {% rule 'auth.user.read' user as can_read %}
        {% rule 'auth.user.update' user as can_update %}

        <li>
        <a href="{% url 'auth_user_detail' user.username %}">{{ user }} (has perm: {{ can_read|yesno:'Yes,No' }})</a>
        <a href="{% url 'auth_user_update' user.username %}">update (has perm: {{ can_update|yesno:'Yes,No'}})</a>
        </li>
    {% endfor %}
    </ul>


Tips and tricks
---------------

Override rules
``````````````

If your project wants to change the behaviour of ``your_app`` to allows users
to create models and edit the models they have created, you could add after
``rules_light.autodiscover()``:

.. code-block:: python

    def my_model_or_staff(user, rulename, obj):
        return user.is_staff or user == obj.author

    rules_light.registry['your_app.your_model.create'] = True
    rules_light.registry['your_app.your_model.update'] = my_model_or_staff
    rules_light.registry['your_app.your_model.delete'] = my_model_or_staff

As you can see, a project can **completely** change the security logic of an
app, which should enpower creative django developers hehe ...

See :doc:`docs on registry</registry>` for more details.

Take a shortcut
```````````````

django-rules-light comes with a predefined ``is_staff`` rule which you could
use in ``your_app/rules_light_registry.py``:

.. code-block:: python

    import rules_light

    # Allow all users to see your_model
    rules_light.registry.setdefault('your_app.your_model.read', True)

    # Allow admins to create and edit models
    rules_light.registry.setdefault('your_app.your_model.create', rules_light.is_staff)
    rules_light.registry.setdefault('your_app.your_model.update', rules_light.is_staff)
    rules_light.registry.setdefault('your_app.your_model.delete', rules_light.is_staff)
 
See :doc:`docs on shortcuts</shortcuts>`.

Test security
`````````````

See :doc:`security testing docs</testing>`.
