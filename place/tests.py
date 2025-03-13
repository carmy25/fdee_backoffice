from functools import partial
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase


class PlaceTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', first_name='test', last_name='test', email='test@gmail.com', password='Test1234')
        self.client.force_login(self.user)

    def test_create_place(self):
        response = self.client.post(
            '/api/places/',
            data={'name': 'Test place'},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Test place')
