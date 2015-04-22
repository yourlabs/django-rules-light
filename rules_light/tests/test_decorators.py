from __future__ import unicode_literals
import unittest

import rules_light

@rules_light.make_decorator
def return_true(*args):
    return True


@rules_light.make_decorator
def return_false(*args):
    return False


class DecoratorsTestCase(unittest.TestCase):
    def test_decorator_return_true(self):
        rule = return_true(lambda x, y: True)
        self.assertTrue(rule('x', 'y'))

        rule = return_true(lambda x, y: False)
        self.assertFalse(rule('x', 'y'))

    def test_decorator_return_false(self):
        rule = return_false(lambda x, y: True)
        self.assertFalse(rule('x', 'y'))

        rule = return_false(lambda x, y: False)
        self.assertFalse(rule('x', 'y'))

    def test_decorator_name(self):
        @return_true
        def foo(*args):
            pass

        self.assertEqual(foo.__name__, 'foo')
