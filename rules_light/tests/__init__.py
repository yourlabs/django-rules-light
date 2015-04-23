import django


if django.VERSION < (1, 7):
    import rules_light
    rules_light.autodiscover()
