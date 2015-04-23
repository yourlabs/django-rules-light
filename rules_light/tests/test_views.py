from __future__ import unicode_literals
import pytest
import unittest

from django.test.client import RequestFactory
from django.contrib.auth.models import User, AnonymousUser

import rules_light
from rules_light.views import RegistryView


@pytest.mark.django_db
class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        """
        Note that URL doesn't matter here because the tests excute the views
        directly.
        """
        User.objects.all().delete()

        self.anonymous_request = RequestFactory().get('/')
        self.anonymous_request.user = AnonymousUser()

        self.user_request = RequestFactory().get('/')
        self.user_request.user, c = User.objects.get_or_create(
            username='foo', is_staff=False)

        self.admin_request = RequestFactory().get('/')
        self.admin_request.user, c = User.objects.get_or_create(
            username='bar', is_staff=True)

    def test_registry_view(self):
        view = RegistryView.as_view()

        with self.assertRaises(rules_light.Denied) as cm:
            view(self.anonymous_request)

        with self.assertRaises(rules_light.Denied) as cm:
            view(self.user_request)

        # it should not raise an exception
        view(self.admin_request)
