from decimal import Decimal
from functools import partial
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User


from .models import Receipt
from .views import CategoryViewSet, ReceiptViewSet


class BaseTestCase(APITestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.factory = APIRequestFactory()
        self.post = partial(self.factory.post, format='json')
        self.user = User.objects.get(username='crchemist')
        self.force_authenticate = partial(force_authenticate, user=self.user)
        self.client.force_login(self.user)

    def tearDown(self):
        self.client.logout()
        return super().tearDown()

    def list_action(self, vs, path):
        response = self.call_vs_get(vs, path, {'get': 'list'})
        return response.data

    def call_vs_get(self, vs, path, action, pk=None):
        request = self.factory.get(path)
        self.force_authenticate(request)
        response = vs.as_view(action)(request, pk=pk)
        self.assertEqual(response.status_code, 200)
        return response


class ReceiptTestCase(BaseTestCase):

    def test_empty_receipt_creation(self):
        response = self.client.post(
            reverse('receipt-list'),
            data={
                'product_items': [],
                'place': 1,
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_receipt_happy_path(self):
        # create receipts
        response = self.client.post(
            reverse('receipt-list'),
            data={'place': 1,
                  'product_items': [{'product_type': 8, 'amount': 2}],
                  },
            format='json'
        )
        receipt_id = response.data['id']
        self.assertEqual(response.data['place_name'], 'Зал 1, Стіл 2')

        # list receipts
        self.list_action(ReceiptViewSet, '/order/receipts')

        # receipt update payment method
        request = self.factory.patch(
            f'/order/receipts/{receipt_id}',
            {'payment_method': 'CASH'},
            format='json')
        self.force_authenticate(request)
        response = ReceiptViewSet.as_view(
            {'patch': 'partial_update'})(request, pk=receipt_id)
        self.assertEqual(response.data['payment_method'], 'CASH')

        # update receipt product items
        request = self.factory.patch(
            f'/order/receipts/{receipt_id}',
            {'product_items':
                [
                    {'product_type': 8, 'amount': 3},
                    {'product_type': 9, 'amount': 1}
                ],
             'place': 1
             },
            format='json')
        self.force_authenticate(request)
        response = ReceiptViewSet.as_view(
            {'patch': 'partial_update'})(request, pk=receipt_id)
        self.assertListEqual(
            response.data['product_items'],
            [{'product_type': 8, 'amount': 3, 'name': 'Овочевий', 'price': Decimal('70.00'), },
             {'product_type': 9, 'amount': 1, 'name': 'Курячий бульйон з лапшою', 'price': Decimal('65.00'), }])

        self.assertEqual(response.status_code, 200)

    def test_categories(self):
        # list categories
        url = reverse('category-list')
        response = self.client.get(url)
        cat, *_ = response.data
        self.assertSetEqual(set(cat.keys()), {'id', 'name', 'image', 'parent'})

        # get product list by category
        cat_id = cat['id']
        url = reverse('category-detail', kwargs={'pk': cat_id})
        response = self.client.get(url)
        self.assertSetEqual(set(response.data.keys()), {
                            'id', 'products', 'name', 'image', 'parent'})

    def test_create_new_receipt(self):
        pass
