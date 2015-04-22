from __future__ import unicode_literals
from django.test import TestCase

import rules_light


class AutodiscoverTestCase(TestCase):
    def test_autodiscover(self):
        self.assertEqual(list(rules_light.registry.keys()), [])
        rules_light.autodiscover()
        self.assertTrue('rules_light.rule.read' in rules_light.registry.keys())
        self.assertFalse('Foo bar' in rules_light.registry.keys())
