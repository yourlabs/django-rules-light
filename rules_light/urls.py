from __future__ import unicode_literals

from django.urls import re_path

from .views import RegistryView


urlpatterns = [
    re_path(r'$', RegistryView.as_view(), name='rules_light_registry'),
]
