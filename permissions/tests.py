import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from repositories.models import Repository
from users.models import User
from permissions.models import UserPermissions


class TestPermissionApi(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPermissionApi, cls).setUpClass()
        cls.user = User(username='maxmon', email='max@krivich.com', password='nsaSucks')
        cls.user.save()
        cls.user1 = User(username='maxmun', email='max@krivich.com', password='nsaSucks')
        cls.user1.save()
        cls.repository = Repository(name='Project-basic')
        cls.repository.save()
        cls.repository1 = Repository(name='Project-basic1')
        cls.repository1.save()
        cls.permission = UserPermissions(user=cls.user, repository=cls.repository, status='o')
        cls.permission.save()

    def test_create_permission(self):
        """
        Test case for create a permission
        """
        url = reverse('permissions:permission-list')
        data = {'user': '2', 'repository': '2', 'status': 'c'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserPermissions.objects.count(), 2)
        self.assertEqual(UserPermissions.objects.get(id=2).status, 'c')

    def test_list_permissions(self):
        """
        Test case for get all permissions
        """
        url = reverse('permissions:permission-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(UserPermissions.objects.count(), 1)
        self.assertEqual(UserPermissions.objects.get().status, 'o')

    def test_get_permission(self):
        """
        Test case for get a permission
        """
        url = reverse('permissions:permission-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(json.loads(response.content)['status'], 'o')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserPermissions.objects.count(), 1)
        self.assertEqual(UserPermissions.objects.get().status, 'o')

    def test_put_permission(self):
        """
        Test case for update a permission
        """
        url = reverse('permissions:permission-detail', kwargs={'pk': 1})
        data = {'user': '1', 'repository': '1', 'status': 'c'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(json.loads(response.content)['status'], 'c')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserPermissions.objects.count(), 1)
        self.assertEqual(UserPermissions.objects.get().status, 'c')

    def test_delete_permission(self):
        """
        Test case for delete a permission
        """
        url = reverse('permissions:permission-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserPermissions.objects.count(), 0)

