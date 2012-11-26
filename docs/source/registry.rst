Rule registry
=============

API
---

.. automodule:: rules_light.registry
   :members:

Examples
--------

.. literalinclude:: ../../test_project/auth_rules.py
   :language: python

Even django-rules-light's view uses a permission, it is registered in
``rules_light/rules_light_registry.py`` and thus is picked up by
``rules_light.autodiscover()``:

.. literalinclude:: ../../rules_light/rules_light_registry.py
   :language: python

Of course, you could use any callable instead of the lambda function.
