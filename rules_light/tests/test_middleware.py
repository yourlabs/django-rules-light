import pytest
import unittest

from django.test.client import Client


@pytest.mark.django_db
class MiddlewareTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_redirect(self):
        self.client.get('/')
