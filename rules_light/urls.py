from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import RegistryView


urlpatterns = patterns('',
    url(r'$', RegistryView.as_view(), name='rules_light_registry'),
)
