# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import logging
import pytest
import unittest
from mock import Mock

from django.contrib.auth.models import User

import rules_light


@pytest.mark.django_db
class RegistryTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = rules_light.RuleRegistry()
        self.registry.logger = Mock(spec_set=['debug', 'info', 'warn', 'error'])
        self.user, c = User.objects.get_or_create(username='test')

    def test_run_rule_no_args(self):
        mock = Mock(return_value=True, spec_set=['__call__'])
        self.registry['x.y.z'] = mock

        self.registry.logger.debug.assert_called_once_with(
            u'[rules_light] "x.y.z" registered with: Mock')

        result = self.registry.run(self.user, 'x.y.z')

        self.registry.logger.info.assert_called_once_with(
            u'[rules_light] Mock(test, "x.y.z") passed')

        self.assertEqual(result, True)
        mock.assert_called_once_with(self.user, 'x.y.z')

    def test_run_rule_with_args(self):
        mock = Mock(return_value=True, spec_set=['__call__'])
        self.registry['x.y.z'] = mock

        result = self.registry.run(self.user, 'x.y.z', 'foo', x='bar')

        self.registry.logger.info.assert_called_once_with(
            u'[rules_light] Mock(test, "x.y.z", "foo", x="bar") passed')

        self.assertEqual(result, True)
        mock.assert_called_once_with(self.user, 'x.y.z', 'foo', x='bar')

    def test_raises_Denied(self):
        mock = Mock(return_value=False, spec_set=['__call__'])
        self.registry['x.y.z'] = mock

        with self.assertRaises(rules_light.Denied) as cm:
            self.registry.require(self.user, 'x.y.z')

        self.registry.logger.warn.assert_called_once_with(
            u'[rules_light] Deny Mock(test, "x.y.z")')

    def test_return_False(self):
        mock = Mock(return_value=False, spec_set=['__call__'])
        self.registry['x.y.z'] = mock

        self.assertFalse(self.registry.run(self.user, 'x.y.z'))
        self.registry.logger.info.assert_called_once_with(
            u'[rules_light] Mock(test, "x.y.z") failed')

    def test_raises_RuleDoesNotExist(self):
        with self.assertRaises(rules_light.DoesNotExist) as cm:
            self.registry.run(self.user, 'x')

        self.registry.logger.error.assert_called_once_with(
            u'[rules_light] Rule does not exist "x"')
