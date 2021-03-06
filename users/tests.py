from django.shortcuts import reverse
from rest_framework.test import APIClient, APITestCase

from users.models import User


class TestUserApi(APITestCase):
    def setUp(self):
        self.user = User(username='maxmen', email='max@krivich.com', password='nsaSucks')
        self.user.save()

    def test_user_creation(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse('users:user-list'), {
            'username': 'user2',
            'email': 'asd@asd.com',
            'password': 'eqadcad123',
        })
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, 201)

    def test_getting_users(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(reverse('users:user-list'), format="json")
        self.assertEqual(len(response.data['results']), 1)
        self.assertEquals(response.status_code, 200)

    def test_updating_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.patch(reverse('users:user-detail', kwargs={'user_id': 1}), {
            'username': 'maxkrivich',
            'email': 'asda@asd.asd',
            'password': 'asdasd'
        })
        self.assertEqual('maxkrivich', response.json()['username'])
        self.assertEquals(response.status_code, 200)

    def test_deleting_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.delete(reverse('users:user-detail', kwargs={'user_id': 1}))
        self.assertEqual(User.objects.count(), 0)
        self.assertEquals(response.status_code, 204)
