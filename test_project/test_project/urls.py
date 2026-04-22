from django.urls import re_path, include
from django.views import generic
from django.contrib.auth.models import User

import rules_light
# not need in this particular project ... oh well it'll serve as example
rules_light.autodiscover()
# import our project specific rules
import auth_rules
from django.contrib import admin

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^auth/', include('django.contrib.auth.urls')),
    re_path(r'^rules/', include('rules_light.urls')),

    re_path(r'^$', generic.ListView.as_view(model=User,
        template_name='auth/new_user_list.html'), name='auth_user_list'),
    re_path(r'user/(?P<username>[\w_-]+)/$',
        rules_light.class_decorator(generic.DetailView).as_view(
            slug_field='username', slug_url_kwarg='username', model=User),
        name='auth_user_detail'),
    re_path(r'user/(?P<username>[\w_-]+)/update/$',
        rules_light.class_decorator(generic.UpdateView).as_view(
            slug_field='username', slug_url_kwarg='username', model=User,
            fields=('first_name', 'last_name', 'email'),
            success_url='/'),
        name='auth_user_update'),
]
