from functools import partial
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase

from place.models import Place


class PlaceTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', first_name='test', last_name='test', email='test@gmail.com', password='Test1234')
        self.client.force_login(self.user)

    def test_create_place(self):
        response = self.client.post(
            '/place/places/',
            data={'name': 'Test place'},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Test place')

    def test_retrieve_places(self):
        place1 = Place.objects.create(name='Place 1')
        place2 = Place.objects.create(name='Place 2')
        response = self.client.get('/place/places/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 2)
        expected_data = [
            {'id': place1.id, 'name': 'Place 1'},
            {'id': place2.id, 'name': 'Place 2'}
        ]
        self.assertListEqual(response.data, expected_data)
