from django.test import TestCase

from .models import Receipt


class ReceiptTestCase(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        pass

    def test_create_receipt(self):
        pass
