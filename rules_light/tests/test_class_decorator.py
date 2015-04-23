from __future__ import unicode_literals
import unittest
import pytest

from django.views import generic
from django.test.client import RequestFactory
from django.contrib.auth.models import User

import rules_light
from rules_light.views import RegistryView

from .fixtures.class_decorator_classes import *


@pytest.mark.django_db
class ClassDecoratorTestCase(unittest.TestCase):
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
        rules_light.registry['funny'] = False
        # ensure that it would not raise an exception if it tried
        # auth.user.read
        rules_light.registry['auth.user.read'] = True
        view = FunnyUpdateView.as_view()

        with self.assertRaises(rules_light.Denied) as cm:
            view(self.request, pk=1)

        rules_light.registry['funny'] = True
        # it should not raise an exception
        view(self.request, pk=1)

    def test_dispatch_decorator(self):
        rules_light.registry['foo'] = False

        @rules_light.class_decorator('foo')
        class MyView(generic.View):
            pass
        view = MyView.as_view()

        with self.assertRaises(rules_light.Denied) as cm:
            view(self.request)

        rules_light.registry['foo'] = True
        # it should not raise an exception
        view(self.request)

    def test_fail(self):
        with self.assertRaises(rules_light.RulesLightException) as cm:
            @rules_light.class_decorator
            class MyView(generic.View):
                pass
