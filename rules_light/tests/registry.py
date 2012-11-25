import unittest
from mock import Mock

from django.contrib.auth.models import User

import rules_light


class RegistryTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = rules_light.RuleRegistry()
        self.user, c = User.objects.get_or_create(username='test')

    def test_register_rule(self):
        self.registry.register('x.y.z', False)
        self.assertEqual(self.registry['x.y.z'], False)

    def test_unregister_rule(self):
        self.registry.register('x.y.z', False)
        self.registry.unregister('x.y.z')
        self.registry.register('x.y.z', True)
        self.assertEqual(self.registry['x.y.z'], True)

    def test_reregister_rule(self):
        self.registry.register('x.y.z', False)
        self.registry.reregister('x.y.z', True)
        self.assertEqual(self.registry['x.y.z'], True)

    def test_raises_RuleNotRegistered(self):
        with self.assertRaises(rules_light.RuleNotRegistered) as cm:
            self.registry.unregister('x.y.z')

    def test_run_rule_no_args(self):
        mock = Mock(return_value=True)
        self.registry.register('x.y.z', mock)

        result = self.registry.run(self.user, 'x.y.z')

        self.assertEqual(result, True)
        mock.assert_called_once_with(self.user, 'x.y.z')

    def test_run_rule_with_args(self):
        mock = Mock(return_value=True)
        self.registry.register('x.y.z', mock)

        result = self.registry.run(self.user, 'x.y.z', 'foo', x='bar')

        self.assertEqual(result, True)
        mock.assert_called_once_with(self.user, 'x.y.z', 'foo', x='bar')
