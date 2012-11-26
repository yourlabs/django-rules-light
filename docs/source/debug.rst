Debugging
=========

Two tools are provided to debug issues with your registry:

- the logger logs everything,
- the url provides a live rule registry browser.

As usual, resort to ``ipdb``, for example in
``rules_light.RuleRegistry.run()`` place::

    import ipdb; ipdb.set_trace()

The registry browser
--------------------

.. automodule:: rules_light.views
   :members:
