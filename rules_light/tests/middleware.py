import unittest

from django.test.client import Client

import rules_light


class MiddlewareTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_redirect(self):
        self.client.go('/')
