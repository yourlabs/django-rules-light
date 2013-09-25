from __future__ import unicode_literals

from django.views import generic

import rules_light


@rules_light.class_decorator('rules_light.rule.read')
class RegistryView(generic.TemplateView):
    """
    Expose the rule registry for debug purposes.

    Install it as such::

        url(r'^rules/$', RegistryView.as_view(), name='rules_light_registry'),

    Or just::

        url(r'^rules/', include('rules_light.urls')),

    Note: view requires ``'rules_light.rule.read'`` which is enabled for admins
    by default.
    """

    template_name = 'rules_light/registry.html'

    def get_context_data(self):
        """ Add the registry to the context. """
        return {'registry': rules_light.registry}
