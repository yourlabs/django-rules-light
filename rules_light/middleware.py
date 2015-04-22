"""
The role of the middleware is to present a user friendly error page when a rule
denied process of the request by raising ``Denied``.
"""
from __future__ import unicode_literals

from django import template
from django import http
from django.conf import settings

from .exceptions import RulesLightException


class Middleware(object):
    """
    Install this middleware by adding `rules_light.middleware.Middleware`` to
    ``settings.MIDDLEWARE_CLASSES``.
    """
    def process_exception(self, request, exception):
        """
        Render ``rules_light/exception.html`` when a ``Denied`` exception was
        raised.
        """
        if not isinstance(exception, RulesLightException):
            return

        ctx = template.RequestContext(request, dict(exception=exception,
            settings=settings))
        return http.HttpResponseForbidden(template.loader.render_to_string(
            'rules_light/exception.html', ctx))
