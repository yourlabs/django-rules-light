from django import template
from django import http
from django.conf import settings

from exceptions import RulesLightException, Denied, DoesNotExist


class DenialHandlingMiddleware(object):
    def process_exception(self, request, exception):
        if not isinstance(exception, RulesLightException):
            return

        ctx = template.RequestContext(request, dict(exception=exception,
            settings=settings))
        return http.HttpResponseForbidden(template.loader.render_to_string(
            'rules_light/exception.html', ctx))
