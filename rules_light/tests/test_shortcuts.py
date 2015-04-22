from __future__ import unicode_literals
import unittest
import pytest

from django.contrib.auth.models import User

import rules_light


@pytest.mark.django_db
class ShortcutsTestCase(unittest.TestCase):
    def setUp(self):
        self.user, c = User.objects.get_or_create(username='foo')
        self.admin, c = User.objects.get_or_create(username='bar',
                is_staff=True)

    def test_is_authenticated_decorator(self):
        return_true = rules_light.is_authenticated(lambda u, r: True)

        self.assertFalse(return_true(None, 'foo'))
        self.assertTrue(return_true(self.user, 'foo'))

    def test_is_authenticated_rule(self):
        self.assertFalse(rules_light.is_authenticated(None, 'foo'))
        self.assertTrue(rules_light.is_authenticated(self.user, 'foo'))

    def test_is_staff_decorator(self):
        return_true = rules_light.is_staff(lambda u, r: True)

        self.assertFalse(return_true(None, 'foo'))
        self.assertFalse(return_true(self.user, 'foo'))
        self.assertTrue(return_true(self.admin, 'foo'))

    def test_is_staff_rule(self):
        self.assertFalse(rules_light.is_staff(None, 'foo'))
        self.assertFalse(rules_light.is_staff(self.user, 'foo'))
        self.assertTrue(rules_light.is_staff(self.admin, 'foo'))
