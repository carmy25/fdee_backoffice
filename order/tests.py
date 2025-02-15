from functools import partial
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User


from .models import Receipt
from .views import ReceiptViewSet


class ReceiptTestCase(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.factory = APIRequestFactory()
        self.post = partial(self.factory.post, format='json')
        self.user = User.objects.get(username='crchemist')
        self.force_authenticate = partial(force_authenticate, user=self.user)

    def test_receipt_happy_path(self):
        # create receipts
        request = self.post(
            '/order/receipts/',
            {'place': 1,
             'product_items': [{'product_type': 8, 'amount': 2}],
             })
        self.force_authenticate(request)
        response = ReceiptViewSet.as_view({'post': 'create'})(request)
        receipt_id = response.data['id']
        breakpoint()

        # list receipts
        request = self.factory.get('/order/receipts/')
        self.force_authenticate(request)
        response = ReceiptViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

        # receipt update payment method
        request = self.factory.patch(
            f'/order/receipts/{receipt_id}/',
            {'payment_method': 'CASH'},
            format='json')
        self.force_authenticate(request)
        response = ReceiptViewSet.as_view(
            {'patch': 'partial_update'})(request, pk=receipt_id)
        self.assertEqual(response.data['payment_method'], 'CASH')

        # update receipt product items
        request = self.factory.patch(
            f'/order/receipts/{receipt_id}/',
            {'product_items':
                [
                    {'product_type': 8, 'amount': 3},
                    {'product_type': 9, 'amount': 1}
                ],
             },
            format='json')
        self.force_authenticate(request)
        response = ReceiptViewSet.as_view(
            {'patch': 'partial_update'})(request, pk=receipt_id)
        breakpoint()
        self.assertListEqual(
            response.data['product_items'],
            [{'product_type': 8, 'amount': 3},
             {'product_type': 9, 'amount': 1}])

        self.assertEqual(response.status_code, 200)
