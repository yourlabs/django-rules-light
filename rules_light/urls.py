from __future__ import unicode_literals

from django.conf.urls import url

from .views import RegistryView


urlpatterns = [
    url(r'$', RegistryView.as_view(), name='rules_light_registry'),
]
