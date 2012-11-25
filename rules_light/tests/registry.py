import unittest
from mock import Mock

from django.contrib.auth.models import User

import rules_light


class RegistryTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = rules_light.RuleRegistry()
        self.user, c = User.objects.get_or_create(username='test')

    def test_run_rule_no_args(self):
        mock = Mock(return_value=True)
        self.registry['x.y.z'] = mock

        result = self.registry.run(self.user, 'x.y.z')

        self.assertEqual(result, True)
        mock.assert_called_once_with(self.user, 'x.y.z')

    def test_run_rule_with_args(self):
        mock = Mock(return_value=True)
        self.registry['x.y.z'] = mock

        result = self.registry.run(self.user, 'x.y.z', 'foo', x='bar')

        self.assertEqual(result, True)
        mock.assert_called_once_with(self.user, 'x.y.z', 'foo', x='bar')

    def test_raises_Denied(self):
        mock = Mock(return_value=None)
        self.registry['x.y.z'] = mock

        with self.assertRaises(rules_light.Denied) as cm:
            self.registry.require(self.user, 'x.y.z')

    def test_return_False(self):
        mock = Mock(return_value=None)
        self.registry['x.y.z'] = mock

        self.assertFalse(self.registry.run(self.user, 'x.y.z'))

    def test_raises_RuleDoesNotExist(self):
        with self.assertRaises(rules_light.DoesNotExist) as cm:
            self.registry.run(self.user, 'x')
