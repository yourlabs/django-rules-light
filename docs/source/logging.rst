Logging
=======

Everything is logged in the ``rules_light`` logger:

- rule registered is logged with ``DEBUG`` level,
- rule ``run()`` is logged with ``INFO`` level,
- ``require()`` failure is logged with ``WARN`` level.

Install
-------

Example ``settings.LOGGING`` that will display all logged events in the
console, as well as denials in malicious.log.

See http://docs.djangoproject.com/en/dev/topics/logging for
more details on how to customize your logging configuration.


.. literalinclude:: ../../test_project/test_project/rules_logging.py
   :language: python
