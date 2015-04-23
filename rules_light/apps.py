from django.apps import AppConfig


class RulesLightConfig(AppConfig):
    name = 'rules_light'

    def ready(self):
        from rules_light.registry import autodiscover
        autodiscover()
