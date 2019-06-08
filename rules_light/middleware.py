"""
The role of the middleware is to present a user friendly error page when a rule
denied process of the request by raising ``Denied``.
"""
from __future__ import unicode_literals

from django import template, http, VERSION

from django.conf import settings

from .exceptions import RulesLightException


class Middleware(object):
    """
    Install this middleware by adding `rules_light.middleware.Middleware`` to
    ``settings.MIDDLEWARE_CLASSES`` or ``settings.MIDDLEWARE`` for Django1.10+
    """
    def process_exception(self, request, exception):
        """
        Render ``rules_light/exception.html`` when a ``Denied`` exception was
        raised.
        """
        if not isinstance(exception, RulesLightException):
            return

        if VERSION > (1, 8):
            ctx = dict(request=request, exception=exception, settings=settings)
        else:
            ctx = template.RequestContext(request, dict(exception=exception,
                settings=settings))
        return http.HttpResponseForbidden(template.loader.render_to_string(
            'rules_light/exception.html', ctx))

    def __init__(self, get_response=None):
        super(Middleware, self).__init__()
        # Support Django 1.10 middleware.
        if get_response is not None:
            self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
