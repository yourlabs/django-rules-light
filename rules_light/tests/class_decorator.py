import unittest

from django.views import generic
from django.test.client import RequestFactory
from django.contrib.auth.models import User

import rules_light


@rules_light.class_decorator
class CreateView(generic.CreateView):
    model = User


@rules_light.class_decorator
class UpdateView(generic.UpdateView):
    model = User


@rules_light.class_decorator
class DetailView(generic.DetailView):
    model = User


@rules_light.class_decorator
class DeleteView(generic.DeleteView):
    model = User


@rules_light.class_decorator
class ListView(generic.ListView):
    model = User


@rules_light.class_decorator('auth.user.update')
class FunnyUpdateView(generic.UpdateView):
    model = User


class DecoratorTestCase(unittest.TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.request.user, c = User.objects.get_or_create(username='foo')

    def test_create_view_decorator(self):
        rules_light.registry['auth.user.create'] = False
        view = CreateView.as_view()

        with self.assertRaises(rules_light.Denied) as cm:
            view(self.request)

        rules_light.registry['auth.user.create'] = True
        # it should not raise an exception
        view(self.request)

    def test_update_view_decorator(self):
        rules_light.registry['auth.user.update'] = False
        view = UpdateView.as_view()

        with self.assertRaises(rules_light.Denied) as cm:
            view(self.request, pk=1)

        rules_light.registry['auth.user.update'] = True
        # it should not raise an exception
        view(self.request, pk=1)

    def test_detail_view_decorator(self):
        rules_light.registry['auth.user.read'] = False
        view = DetailView.as_view()

        with self.assertRaises(rules_light.Denied) as cm:
            view(self.request, pk=1)

        rules_light.registry['auth.user.read'] = True
        # it should not raise an exception
        view(self.request, pk=1)

    def test_delete_view_decorator(self):
        rules_light.registry['auth.user.delete'] = False
        view = DeleteView.as_view()

        with self.assertRaises(rules_light.Denied) as cm:
            view(self.request, pk=1)

        rules_light.registry['auth.user.delete'] = True
        # it should not raise an exception
        view(self.request, pk=1)

    def test_funny_view_decorator(self):
        rules_light.registry['auth.user.update'] = False
        # ensure that it would not raise an exception if it tried
        # auth.user.read
        rules_light.registry['auth.user.read'] = True
        view = FunnyUpdateView.as_view()

        with self.assertRaises(rules_light.Denied) as cm:
            view(self.request, pk=1)

        rules_light.registry['auth.user.update'] = True
        # it should not raise an exception
        view(self.request, pk=1)
