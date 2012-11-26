from django.views import generic

import rules_light


@rules_light.class_decorator('rules_light.rule.read')
class RegistryView(generic.TemplateView):
    template_name = 'rules_light/registry.html'

    def get_context_data(self):
        return {'registry': rules_light.registry}
