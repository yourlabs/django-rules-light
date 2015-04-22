from __future__ import unicode_literals

from django.views import generic
from django.contrib.auth.models import User

import rules_light

@rules_light.class_decorator
class CreateView(generic.CreateView):
    model = User
    fields = [f.name for f in User._meta.fields]


@rules_light.class_decorator
class UpdateView(generic.UpdateView):
    model = User
    fields = [f.name for f in User._meta.fields]


@rules_light.class_decorator
class DetailView(generic.DetailView):
    model = User
    fields = [f.name for f in User._meta.fields]


@rules_light.class_decorator
class DeleteView(generic.DeleteView):
    model = User
    fields = [f.name for f in User._meta.fields]


@rules_light.class_decorator('funny')
class FunnyUpdateView(generic.UpdateView):
    model = User
    fields = [f.name for f in User._meta.fields]



